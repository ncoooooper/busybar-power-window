# Firmware verification

BUSY Bar Emulator 0.1.0-beta.5, firmware 1.3.1.

Read the actual Mac battery through pmset and the HTTP bridge (100%, mains); loaded a controlled upcoming 43-minute outage from the schedule. Switched views, stopped the bridge, and verified the offline path. NUT support is included but a physical UPS was not available.

The app was typechecked, built, installed and exercised on the emulator. Native captures are under screenshots/. The tested installable archive is in packages/.

Verified that the 100% real macOS reading fills all 72 columns of the front charge meter.

Firmware motion pass: up, down, ok. 15 distinct frames in the controls recording. App io.ncoooooper.powerwindow exited: finished; heap peak 81.9 of 128 KiB.

## Display capture

Firmware 1.3.1 rendered both README examples. The display run replayed sample inputs in a separate emulator project. The source test above describes how those readings were obtained. Each square in a guide GIF is one front LED in a 16 × 16 cell. The production archive was built from the source in this repository.

## Screen transition capture

Firmware 1.3.1 rendered the display sequences in the README. The guide uses a 14 × 14 lit area inside each 16 × 16 cell. Input sequences, frame counts and the release archive checksum are in [the capture record](media/screen-transitions.json).
