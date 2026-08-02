Just your average 3d print user who got one of these things and has enough knowledge to be dangerous lol.

Seriously try my changes at your own risk and backup all your stock configs first!


CHECK YOUR MACHINE GCODE SECTIONS
start code-
START_PRINT EXTRUDER=[nozzle_temperature_initial_layer] BED=[bed_temperature_initial_layer_single] CHAMBER=[chamber_temperature] INITIAL_TOOL=[initial_tool]  MESH_MIN_X={adaptive_bed_mesh_min[0]}  MESH_MIN_Y={adaptive_bed_mesh_min[1]} MESH_MAX_X={adaptive_bed_mesh_max[0]} MESH_MAX_Y={adaptive_bed_mesh_max[1]} PROBE_COUNT_X={bed_mesh_probe_count[0]} PROBE_COUNT_Y={bed_mesh_probe_count[1]}


End Code- PRINT_END (THIS IS COMMENTED OUT BY DEFAULT IN ORCA AND WM ORCA)
