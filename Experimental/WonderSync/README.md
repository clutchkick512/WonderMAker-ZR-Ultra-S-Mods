# WonderSync

WonderSync is an experimental Moonraker compatibility bridge for the WonderMaker ZR Ultra S.

It reads filament material and color assignments from the WonderMaker touchscreen configuration and exposes them as a virtual MMU object. This allows OrcaSlicer to use its filament Sync button with the WonderMaker toolchanger.

## Current Features

- Reads WonderMaker filament data from `tmt1.ini`
- Synchronizes filament material with OrcaSlicer
- Synchronizes filament color with OrcaSlicer
- Supports four tool slots
- Exposes a virtual `mmu` object through Klipper and Moonraker
- Provides tool-to-gate mapping
- Provides gate temperature information
- Does not modify WonderMaker tool-change or motion behavior

## Tested With

- WonderMaker ZR Ultra S
- WonderMaker Klipper firmware
- OrcaSlicer 2.5.0 Dev
- Printer Agent set to `Moonraker`

## Confirmed Material Mappings

| WonderMaker Index | Material | Orca Result |
|---:|---|---|
| 0 | PLA | Generic PLA |
| 1 | PLA Silk | Currently falls back to Generic PLA |
| 2 | ABS | Generic ABS |
| 3 | PETG | Generic PETG |
| 15 | ASA | Generic ASA |

## Confirmed Color Mappings

| WonderMaker Index | Color | Hex |
|---:|---|---|
| 0 | White | `FFFFFF` |
| 2 | Brown | `8B4513` |
| 3 | Grey | `808080` |
| 4 | Black | `000000` |
| 7 | Blue | `0000FF` |
| 8 | Green | `008000` |
| 10 | Yellow | `FFFF00` |
| 11 | Orange | `FFA500` |
| 14 | Red | `FF0000` |

## Installation

### 1. Copy the Python module

Copy:

```text
wondermaker_mmu.py
```

to:

```text
/home/t13dp/klipper/klippy/extras/wondermaker_mmu.py
```

### 2. Add the Klipper configuration section

Add this to `printer.cfg`:

```ini
[wondermaker_mmu]
source_file: /home/t13dp/printer_data/config/tmt1.ini
num_gates: 4
```

### 3. Restart Klipper

```bash
sudo systemctl restart klipper
```

### 4. Verify the MMU object

```bash
curl -s \
"http://127.0.0.1:7125/printer/objects/query?mmu" \
| python3 -m json.tool
```

The response should contain:

```json
"num_gates": 4
```

along with:

```text
gate_material
gate_color
gate_temperature
gate_status
ttg_map
```

### 5. Configure OrcaSlicer

Open the physical printer connection settings in OrcaSlicer.

Set:

```text
Printer Agent: Moonraker
```

Reconnect the printer. The filament Sync button should then become available.

## Important Notes

WonderSync presents the WonderMaker toolchanger as a virtual MMU only for filament metadata synchronization.

Do not use MMU load, unload, eject, preload, or gate-control buttons shown by Fluidd. Those controls are intended for a real Happy Hare MMU and are not connected to WonderMaker tool-change hardware.

The MMU panel can safely be hidden in Fluidd.

## Roadmap

### v0.1

- [x] Virtual MMU object
- [x] Four-tool support
- [x] PLA synchronization
- [x] PETG synchronization
- [x] ABS synchronization
- [x] ASA synchronization
- [x] Basic color synchronization
- [x] OrcaSlicer Sync button support

### v0.2

- [ ] Complete WonderMaker material mapping
- [ ] Complete WonderMaker color palette
- [ ] Resolve PLA Silk profile matching
- [ ] Read real filament sensor states
- [ ] Improve unknown material and color handling

### v0.3

- [ ] Nozzle type and diameter synchronization
- [ ] Spool ID support
- [ ] Remaining filament tracking
- [ ] Optional bidirectional synchronization
- [ ] Installer and update script

## Current Status

Experimental.

Please report:

- Printer model
- OrcaSlicer version
- Material selected on the WonderMaker screen
- Material imported by OrcaSlicer
- Color selected on the WonderMaker screen
- Color imported by OrcaSlicer

## Disclaimer

This project is not affiliated with WonderMaker, OrcaSlicer, Moonraker, Klipper, or Happy Hare.

Use at your own risk. Back up your configuration before installing experimental modifications.