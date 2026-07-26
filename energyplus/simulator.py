import sys
import shutil
from pathlib import Path

ENERGYPLUS_PATH = r"C:\EnergyPlusV26-1-0"
sys.path.insert(0, ENERGYPLUS_PATH)

from pyenergyplus.api import EnergyPlusAPI

ROOT = Path(__file__).resolve().parent.parent


class EnergyPlusSimulator:

    def __init__(self):
        self.api = EnergyPlusAPI()

    def run(self, idf_name="SmallOffice.idf", output_folder="output"):

        state = self.api.state_manager.new_state()

        idf_file = ROOT / "data" / idf_name
        weather_file = ROOT / "data" / "weather.epw"

        output_path = ROOT / output_folder

        # Remove previous output folder if it exists
        if output_path.exists():
            shutil.rmtree(output_path)

        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\nRunning simulation with {idf_name}...")
        print(f"Saving results to: {output_path}")

        self.api.runtime.run_energyplus(
            state,
            [
                "-r",
                "-d",
                str(output_path),
                "-w",
                str(weather_file),
                str(idf_file),
            ],
        )

        print("Simulation Finished!")

        return output_path