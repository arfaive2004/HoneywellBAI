import json

from energyplus.simulator import EnergyPlusSimulator
from energyplus.sensor_manager import SensorManager
from energyplus.idf_editor import IDFEditor
from energyplus.evaluator import Evaluator
from agent.llm import BuildingAI


class BuildingController:

    def __init__(self):
        self.simulator = EnergyPlusSimulator()
        self.sensor = SensorManager("baseline_output")
        self.ai = BuildingAI()
        self.editor = IDFEditor()
        self.evaluator = Evaluator()

    def run(self):

        print("\n==============================")
        print(" HONEYWELL BUILDING AI")
        print("==============================")

        # ----------------------------------
        # Step 1: Run Baseline Simulation
        # ----------------------------------
        print("\nRunning baseline simulation...")

        baseline_folder = self.simulator.run(
            "SmallOffice.idf",
            "baseline_output"
        )

        # ----------------------------------
        # Step 2: Read Baseline State
        # ----------------------------------
        print("\nReading baseline building state...")

        state = self.sensor.get_latest_state()

        print("\nCurrent Building State")
        for key, value in state.items():
            print(f"{key}: {value}")

        # ----------------------------------
        # Step 3: AI Decision
        # ----------------------------------
        print("\nSending data to Gemini...")

        response = self.ai.analyze(state)

        cleaned = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        decision = json.loads(cleaned)

        print("\nAI Decision")
        print(json.dumps(decision, indent=4))

        # ----------------------------------
        # Step 4: Modify Building
        # ----------------------------------
        print("\nUpdating EnergyPlus model...")

        self.editor.create_copy()

        self.editor.update_cooling_setpoint(
            decision["hvac_setpoint"]
        )

        # ----------------------------------
        # Step 5: Optimized Simulation
        # ----------------------------------
        print("\nRunning optimized simulation...")

        optimized_folder = self.simulator.run(
            "SmallOffice_modified.idf",
            "optimized_output"
        )

        # ----------------------------------
        # Step 6: Compare Results
        # ----------------------------------
        print("\nEvaluating performance...")

        results = self.evaluator.compare(
            baseline_folder,
            optimized_folder
        )

        print("\n========== RESULTS ==========")
        print(json.dumps(results, indent=4))

        print("\nOptimization Summary")
        print(f"HVAC Setpoint : {decision['hvac_setpoint']} °C")

        if "lighting_level" in decision:
            print(f"Lighting      : {decision['lighting_level']} %")

        if "reason" in decision:
            print(f"Reason        : {decision['reason']}")

        print(
            f"\nEnergy Saving : "
            f"{results['energy_saving_percent']} %"
        )

        print(
            f"Comfort Maintained : "
            f"{results['comfort_maintained']}"
        )

        print("\nOptimization completed successfully.")

        return {
            "building_state": state,
            "decision": decision,
            "results": results,
        }