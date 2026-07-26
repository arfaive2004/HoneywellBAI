import pandas as pd
from pathlib import Path


class Evaluator:

    def __init__(self):
        self.energy_column = (
            "ACDXCOIL 1:Cooling Coil Electricity Rate [W](TimeStep:REPORTSCH) "
        )

        self.temperature_columns = [
            "WEST ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)",
            "EAST ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)",
            "NORTH ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)",
            "ATTIC ZONE:Zone Air Temperature [C](TimeStep:REPORTSCH)",
        ]

    def _read_results(self, folder):

        csv_path = Path(folder) / "eplusout.csv"

        df = pd.read_csv(csv_path)

        latest = df.iloc[-1]

        temperatures = {
            "west_temp": latest[self.temperature_columns[0]],
            "east_temp": latest[self.temperature_columns[1]],
            "north_temp": latest[self.temperature_columns[2]],
            "attic_temp": latest[self.temperature_columns[3]],
        }

        total_energy = df[self.energy_column].sum()

        average_temp = (
            latest[self.temperature_columns[0]]
            + latest[self.temperature_columns[1]]
            + latest[self.temperature_columns[2]]
        ) / 3

        comfort_ok = bool(22 <= average_temp <= 24)

        return {
            "temperatures": temperatures,
            "energy": total_energy,
            "average_temp": average_temp,
            "comfort_ok": comfort_ok,
        }

    def compare(self, baseline_folder, optimized_folder):

        baseline = self._read_results(baseline_folder)
        optimized = self._read_results(optimized_folder)

        saving = (
            (baseline["energy"] - optimized["energy"])
            / baseline["energy"]
            * 100
        )

        return {
    "baseline_energy": float(baseline["energy"]),
    "optimized_energy": float(optimized["energy"]),
    "energy_saving_percent": float(round(saving, 2)),
    "baseline_average_temp": float(round(baseline["average_temp"], 2)),
    "optimized_average_temp": float(round(optimized["average_temp"], 2)),
    "comfort_maintained": bool(optimized["comfort_ok"]),
    "baseline_temperatures": {
        k: float(v) for k, v in baseline["temperatures"].items()
    },
    "optimized_temperatures": {
        k: float(v) for k, v in optimized["temperatures"].items()
    },
}