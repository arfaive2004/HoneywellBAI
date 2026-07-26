from pathlib import Path
import pandas as pd


class SensorManager:

    def __init__(self, output_folder="output"):
        self.output_folder = Path(output_folder)

    def get_latest_state(self):

        csv = self.output_folder / "eplusout.csv"

        if not csv.exists():
            raise FileNotFoundError(f"Could not find simulation output: {csv}")

        df = pd.read_csv(csv)

        latest = df.iloc[-1]

        return {
            "time": latest["Date/Time"],

            "west_temp":
                latest["WEST ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)"],

            "east_temp":
                latest["EAST ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)"],

            "north_temp":
                latest["NORTH ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)"],

            "attic_temp":
                latest["ATTIC ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)"],

            "cooling_power":
                latest["ACDXCOIL 1:Cooling Coil Electricity Rate [W](TimeStep:REPORTSCH) "]
        }