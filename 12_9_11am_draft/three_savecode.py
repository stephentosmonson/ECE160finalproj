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
            "used": False,
            "player_x": 400,
            "player_y": 400,
            "current_map": 1,
            "health": 5,
            "score": 0,
            "enemies": []
        }

    def save(self, slot, data):
        module_name = self.savefiles[slot]
        filename = module_name + '.py'

        json_text = json.dumps(data, indent=4)

        safe_text = (
            json_text
            .replace("true", "True")
            .replace("false", "False")
        )

        with open(filename, "w") as f:
            f.write("gamedata = ")
            f.write(safe_text)

        if module_name in sys.modules:
            del sys.modules[module_name]

    def load(self, slot):
        module_name = self.savefiles[slot]

        if module_name in sys.modules:
            del sys.modules[module_name]

        imported = importlib.import_module(module_name)
        data = imported.gamedata

        if "used" not in data or data["used"] is False:
            return self.default_data.copy()

        for key, value in self.default_data.items():
            if key not in data:
                data[key] = value

        return data