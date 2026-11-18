# Power Window

See reserve battery charge, mains status and the next scheduled outage from your local power bridge.

Put the charge level beside the next outage on the same device. A battery at 40% means something quite different when the power is due back in ten minutes than when the next scheduled cut is about to begin.

## Check the reserve before disconnecting

1. Start the bridge on the machine that can read your Mac battery or UPS. Enter its address in the app settings as described below.
2. Open the app and read the percentage and source on the front. The rear screen distinguishes mains power, battery power and an unknown state.
3. Turn the wheel to read the next scheduled event. The recorded Mac was fully charged and had no upcoming window.

![The front moves from a Mac battery at 100% to No window.](media/guide/reserve-to-outage.gif)

## Read the return time during a cut

1. On the schedule page, **Outage** is the number of minutes until the next cut starts. During an active window, **Restore** counts down to its scheduled end.
2. Turn the wheel again to return to charge. Click to request a new sample if you have just switched the power source.
3. If the bridge goes offline, read the rear status before relying on the percentage. The last successful reading stays on screen.

![The No window page gives way to the Mac battery reading.](media/guide/return-to-battery.gif)

## Set up the source

The included Python bridge reads a Mac battery with pmset or a UPS through Network UPS Tools (upsc). It reads a local outage schedule on every request and returns the current or next window.

Run `python3 bridge/power.py --schedule windows.json` on the Mac. For a NUT UPS, add `--ups desk@localhost`. The schedule file is optional. Example contents: `[{"start":"2026-12-01T14:00:00+02:00","end":"2026-12-01T16:00:00+02:00"}]`. Supply current times from your utility.

For the emulator run `~/.busy-emulator/bin/busy-emulator allow-local 8765`, set Power bridge URL to `http://127.0.0.1:8765/power` and restart. For hardware, bind the bridge to its trusted LAN address with `--host` and enter that address on the bar. Wheel switches between charge and planned outage. Click for a fresh reading. An unreachable source marks the last reading offline.

## Run in the emulator

Open BUSY Bar Emulator. From this repository, run:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

Press **Back** to exit.

The GIFs are excerpts from the emulator recording. Each front-display pixel is shown at 9× its original width and height. The end frames pause for reading.

[Full recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md) · [MIT license](LICENSE)
