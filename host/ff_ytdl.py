"""Native messaging host for FF_ytdl — launches yt-dlp with a given URL."""

import json
import os
import shutil
import struct
import subprocess
import sys


def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) < 4:
        sys.exit(1)
    length = struct.unpack("=I", raw_length)[0]
    data = sys.stdin.buffer.read(length)
    return json.loads(data.decode("utf-8"))


def send_message(msg):
    encoded = json.dumps(msg).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("=I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def find_ytdlp():
    found = shutil.which("yt-dlp")
    if found:
        return found
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    for candidate in [
        os.path.join(program_files, "yt-dlp.exe"),
        os.path.join(program_files, "yt-dlp", "yt-dlp.exe"),
    ]:
        if os.path.isfile(candidate):
            return candidate
    return None


def main():
    message = read_message()
    url = message.get("url", "")

    if not url:
        send_message({"status": "error", "message": "No URL provided"})
        return

    ytdlp = find_ytdlp()
    if not ytdlp:
        send_message({"status": "error", "message": "yt-dlp.exe not found"})
        return

    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "yt-dlp")
    os.makedirs(download_dir, exist_ok=True)
    log_file = os.path.join(download_dir, "yt-dlp.log")

    try:
        with open(log_file, "a") as log:
            subprocess.Popen(
                [ytdlp, url],
                cwd=download_dir,
                stdout=log,
                stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        send_message({"status": "ok"})
    except Exception as e:
        send_message({"status": "error", "message": str(e)})


if __name__ == "__main__":
    main()
