import os
import re
from game_data.zdata.utils import ensure_dict
from game_data.zdata.parse import ParsedZdataFile, parse_zdata_file

DLC_PATTERN = re.compile("_(DLC[0-9])")


class GameCoreDataLoader:
    def __init__(self, game_core_data_path: str):
        self.game_core_data_path = game_core_data_path
        self.base_path = os.path.dirname(self.game_core_data_path)
        self.zdata_cache: dict[str, ParsedZdataFile] = {}

    def load(self):
        game_core_zdata = parse_zdata_file(self.game_core_data_path)
        game_data = {}

        for group_key, group_info in game_core_zdata.exports["Root"]["Groups"].items():
            group_entries = {}

            for filename in group_info.get("FromFiles", []):
                zdata = self.load_zdata_file(os.path.join(self.base_path, filename))
                group_entries.update(zdata.exports)

            for entry_key, (entry_zdata_path, entry_export_key) in ensure_dict(
                group_info.get("Entries", {})
            ).items():
                zdata = self.load_zdata_file(
                    os.path.join(self.base_path, entry_zdata_path)
                )
                group_entries[entry_key] = zdata.exports[entry_export_key]

            game_data[group_key] = group_entries

        return game_data

    def get_zdata_paths(self):
        paths = []

        game_core_zdata = parse_zdata_file(self.game_core_data_path)
        for group_info in game_core_zdata.exports["Root"]["Groups"].values():
            for filename in group_info.get("FromFiles", []):
                paths.append(os.path.join(self.base_path, filename))

            for entry_zdata_path, entry_export_key in ensure_dict(
                group_info.get("Entries", {})
            ).values():
                paths.append(os.path.join(self.base_path, entry_zdata_path))

        return paths

    def load_zdata_file(self, relative_path):
        zdata = self.zdata_cache.get(relative_path, None)
        if zdata:
            return zdata

        zdata = parse_zdata_file(relative_path)

        dlc_match = DLC_PATTERN.search(relative_path)
        if dlc_match:
            zdata.exports = dict(
                (key, {"_core": dlc_match.group(1), **value})
                for key, value in zdata.exports.items()
            )

        self.zdata_cache[relative_path] = zdata

        return zdata

    @property
    def num_files_loaded(self):
        return len(self.zdata_cache)
