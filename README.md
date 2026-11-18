# Power Window

See reserve battery charge, mains status and the next scheduled outage from your local power bridge.

The included Python bridge reads a Mac battery with pmset or a UPS through Network UPS Tools (upsc). It reads a local outage schedule on every request and returns the current or next window.

Run `python3 bridge/power.py --schedule windows.json` on the Mac. For a NUT UPS, add `--ups desk@localhost`. The schedule file is optional. Example contents: `[{"start":"2026-12-01T14:00:00+02:00","end":"2026-12-01T16:00:00+02:00"}]`. Supply current times from your utility.

For the emulator run `~/.busy-emulator/bin/busy-emulator allow-local 8765`, set Power bridge URL to `http://127.0.0.1:8765/power` and restart. For hardware, bind the bridge to its trusted LAN address with `--host` and enter that address on the bar. Wheel switches between charge and planned outage. Click for a fresh reading. An unreachable source marks the last reading offline.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)

[Watch the controls on firmware](media/controls.mp4)
