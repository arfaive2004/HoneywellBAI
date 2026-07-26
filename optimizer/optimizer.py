import json

from energyplus.simulator import EnergyPlusSimulator
from energyplus.idf_editor import IDFEditor
from energyplus.evaluator import Evaluator


class HVACOptimizer:

    def __init__(self):
        self.simulator = EnergyPlusSimulator()
        self.editor = IDFEditor()
        self.evaluator = Evaluator()

    def optimize(self, candidate_setpoints):

        results = []

        for setpoint in candidate_setpoints:

            print(f"\nTesting HVAC Setpoint: {setpoint}°C")

            # Create fresh modified IDF
            self.editor.create_copy()
            self.editor.update_cooling_setpoint(setpoint)

            folder = f"optimization_{str(setpoint).replace('.', '_')}"

            self.simulator.run(
                "SmallOffice_modified.idf",
                folder
            )

            metrics = self.evaluator._read_results(folder)

            score = self.calculate_score(metrics)

            results.append({
                "setpoint": setpoint,
                "energy": float(metrics["energy"]),
                "average_temp": float(metrics["average_temp"]),
                "comfort_ok": bool(metrics["comfort_ok"]),
                "score": score
            })

        results.sort(key=lambda x: x["score"])

        return {
            "best": results[0],
            "all_results": results
        }

    def calculate_score(self, metrics):

        energy = metrics["energy"]

        comfort_penalty = 0

        avg = metrics["average_temp"]

        if avg > 24:
            comfort_penalty += (avg - 24) * 100000

        if avg < 22:
            comfort_penalty += (22 - avg) * 100000

        return energy + comfort_penalty