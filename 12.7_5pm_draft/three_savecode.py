import importlib
import json
import sys


class SaveManager:
    def __init__(self):
        self.savefiles = {
            'save1':'three_save1data',
            'save2':'three_save2data'
        }
        self.default_data = {
            "used": False,  # ← the new flag
            "player_x": 400,
            "player_y": 400,
            "current_map": 1,
            "health": 5,
            "score": 0,
            "enemies": []  # no enemies until you save
        }

    def save(self, slot, data):
        module_name = self.savefiles[slot]
        filename = module_name + '.py'

        # Make JSON-formatted text
        json_text = json.dumps(data, indent=4)

        # Convert JSON booleans to Python booleans
        safe_text = (
            json_text
            .replace("true", "True")
            .replace("false", "False")
        )

        with open(filename, "w") as f:
            f.write("gamedata = ")
            f.write(safe_text)

        # Clear import cache
        if module_name in sys.modules:
            del sys.modules[module_name]

    def load(self, slot):
        module_name = self.savefiles[slot]

        # Remove from cache to force fresh import
        if module_name in sys.modules:
            del sys.modules[module_name]

        imported = importlib.import_module(module_name)
        data = imported.gamedata

        # If never saved → new game
        if "used" not in data or data["used"] is False:
            return self.default_data.copy()

        # Fill missing values (simple compatibility)
        for key, value in self.default_data.items():
            if key not in data:
                data[key] = value

        return data