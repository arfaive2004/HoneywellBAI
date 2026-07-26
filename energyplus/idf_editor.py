from pathlib import Path
import shutil
import re


class IDFEditor:

    def __init__(self):
        self.original = Path("data/SmallOffice.idf")
        self.modified = Path("data/SmallOffice_modified.idf")

    def create_copy(self):
        shutil.copy(self.original, self.modified)

    def update_cooling_setpoint(self, temperature):

        with open(self.modified, "r") as f:
            text = f.read()

        pattern = (
            r"(Schedule:Compact,\s*"
            r"Dual Cooling Setpoints,.*?"
            r"Until:\s*17:00,)([\d.]+)"
        )

        new_text = re.sub(
            pattern,
            rf"\g<1>{temperature}",
            text,
            flags=re.DOTALL,
        )

        with open(self.modified, "w") as f:
            f.write(new_text)

        print(f"Cooling setpoint updated to {temperature}°C")