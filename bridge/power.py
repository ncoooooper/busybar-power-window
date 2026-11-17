"""Serve a read-only power snapshot from macOS or a Network UPS Tools device."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import subprocess


def power_source(ups):
    if ups:
        raw = subprocess.check_output(["upsc", ups], text=True, timeout=3)
        fields = dict(line.split(": ", 1) for line in raw.splitlines() if ": " in line)
        flags = fields["ups.status"].split()
        return round(float(fields["battery.charge"])), ("battery" if "OB" in flags else "mains" if "OL" in flags else "unknown"), "UPS"
    raw = subprocess.check_output(["pmset", "-g", "batt"], text=True, timeout=3)
    charge = re.search(r"(\d+)%", raw)
    if not charge:
        raise ValueError("No battery available")
    return int(charge[1]), ("mains" if "'AC Power'" in raw else "battery"), "Mac"


def current_window(schedule, now):
    if schedule is None:
        return None
    windows = []
    for item in json.loads(schedule.read_text()):
        start, end = (datetime.fromisoformat(item[key].replace("Z", "+00:00")) for key in ("start", "end"))
        if start.utcoffset() is None or end.utcoffset() is None or start >= end:
            raise ValueError("Each window needs ordered timestamps with UTC offsets")
        if end > now:
            windows.append((start, end))
    if not windows:
        return None
    start, end = min(windows)
    active = start <= now
    target = end if active else start
    return {"active": active, "minutes": max(0, int((target-now).total_seconds()+59)//60)}


def serve():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--ups", help="NUT name, e.g. desk@localhost. Default uses macOS pmset.")
    parser.add_argument("--schedule", type=Path, help="JSON array of ISO-8601 start/end pairs, with offsets.")
    args = parser.parse_args()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/power":
                return self.send_error(404)
            try:
                charge, state, source = power_source(args.ups)
                if not 0 <= charge <= 100:
                    raise ValueError("Battery charge outside measurement range")
                snapshot = {"charge": charge, "state": state, "source": source,
                            "window": current_window(args.schedule, datetime.now(timezone.utc))}
                body = json.dumps(snapshot).encode()
            except (KeyError, ValueError, OSError, subprocess.SubprocessError):
                return self.send_error(503, "Power source or schedule unavailable")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
