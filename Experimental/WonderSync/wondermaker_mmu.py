# Read-only WonderMaker filament metadata bridge.
#
# Reads the touchscreen's tmt1.ini file and exposes a virtual "mmu"
# Klipper status object for Moonraker and compatible slicers.

import configparser
import logging
import os


MATERIALS = {
    0: "PLA",
    1: "PLA-Silk",
    2: "ABS",
    3: "PETG",
    15: "ASA",
}

FILAMENT_NAMES = {
    0: "Generic PLA",
    1: "Generic PLA Silk",
    2: "Generic ABS",
    3: "Generic PETG",
    15: "Generic ASA",
}


COLORS = {
    0: ("White", "FFFFFF"),
    2: ("Brown", "8B4513"),
    3: ("Grey", "808080"),
    4: ("Black", "000000"),
    7: ("Blue", "0000FF"),
    8: ("Green", "008000"),
    10: ("Yellow", "FFFF00"),
    11: ("Orange", "FFA500"),
    14: ("Red", "FF0000"),
}


class WondermakerMMU:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.source_file = os.path.expanduser(
            config.get(
                "source_file",
                "/home/t13dp/printer_data/config/tmt1.ini",
            )
        )

        self.num_gates = config.getint(
            "num_gates",
            4,
            minval=1,
            maxval=16,
        )

        # Register the Orca/Happy-Hare-compatible object name.
        self.printer.add_object("mmu", self)

        self.last_mtime = None
        self.last_status = self._default_status()

    def _default_status(self):
        return {
            "enabled": True,
            "num_gates": self.num_gates,
            "gate_name": [""] * self.num_gates,
            "gate_material": [""] * self.num_gates,
            "gate_color": ["808080"] * self.num_gates,
            "gate_temperature": [0] * self.num_gates,
            "gate_status": [0] * self.num_gates,
            "gate_spool_id": [-1] * self.num_gates,
            "ttg_map": list(range(self.num_gates)),
            "tool_to_gate_map": list(range(self.num_gates)),
            "filament": "Unknown",
            "filament_pos": 0,
            "tool": -1,
            "gate": -1,
        }

    def _read_status(self):
        parser = configparser.ConfigParser()

        try:
            loaded = parser.read(self.source_file)

            if not loaded or not parser.has_section("slot"):
                logging.warning(
                    "WonderMaker MMU: missing [slot] in %s",
                    self.source_file,
                )
                return self.last_status

            filament_names = []
            materials = []
            colors = []
            statuses = []

            for gate in range(self.num_gates):
                material_index = parser.getint(
                    "slot",
                    "material%d" % gate,
                    fallback=-1,
                )
                color_index = parser.getint(
                    "slot",
                    "color%d" % gate,
                    fallback=-1,
                )

                material = MATERIALS.get(
                    material_index,
                    "Unknown-%d" % material_index,
                )

                filament_name = FILAMENT_NAMES.get(
                    material_index,
                    "Generic %s" % material,
                )

                color_name, color_hex = COLORS.get(
                    color_index,
                    ("Unknown-%d" % color_index, "808080"),
                )

                filament_names.append(filament_name)
                materials.append(material)
                colors.append(color_hex)

                # The screen defines all four configured slots.
                # Presence sensors remain handled by WonderMaker itself.
                statuses.append(1)

            return {
                "enabled": True,
                "num_gates": self.num_gates,
                "gate_name": filament_names,
                "gate_material": materials,
                "gate_color": colors,
                "gate_temperature": [220] * self.num_gates,
                "gate_status": statuses,
                "gate_spool_id": [-1] * self.num_gates,
                "ttg_map": list(range(self.num_gates)),
                "tool_to_gate_map": list(range(self.num_gates)),
                "filament": "Loaded",
                "filament_pos": 10,
                "tool": -1,
                "gate": -1,
            }

        except Exception:
            logging.exception(
                "WonderMaker MMU: unable to read %s",
                self.source_file,
            )
            return self.last_status

    def get_status(self, eventtime):
        try:
            mtime = os.path.getmtime(self.source_file)
        except OSError:
            mtime = None

        if mtime != self.last_mtime:
            self.last_status = self._read_status()
            self.last_mtime = mtime

        return self.last_status


def load_config(config):
    return WondermakerMMU(config)
