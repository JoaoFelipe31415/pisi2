import sys
import os
from datetime import datetime


class Tee:
    """Write to both original stream and a logfile file-like object.

    Usage:
        tee = Tee(sys.stdout, open('logs/out.log', 'a', encoding='utf-8'))
        sys.stdout = tee
    """

    def __init__(self, stream, fileobj):
        self.stream = stream
        self.file = fileobj

    def write(self, data):
        # maintain original behaviour if empty data
        if not data:
            return
        try:
            self.stream.write(data)
        except Exception:
            pass
        try:
            self.file.write(data)
        except Exception:
            pass

    def flush(self):
        try:
            self.stream.flush()
        except Exception:
            pass
        try:
            self.file.flush()
        except Exception:
            pass


def create_logfile(logs_dir="logs", name_prefix="run"):
    """Ensure logs directory exists and return an open file handle for appending.

    The file will be named like: logs/run-2025-12-01_15-04-02.log
    """
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{name_prefix}-{ts}.log"
    filepath = os.path.join(logs_dir, filename)
    # open the file in append mode with utf-8; keep it open for duration
    f = open(filepath, "a", encoding="utf-8")
    return f


def attach_streams_to_log(logfile=None, logs_dir="logs", prefix="run"):
    """Redirect sys.stdout and sys.stderr so every printed line is also written to logfile.

    If logfile is None, we create a timestamped file in logs_dir.
    Returns the file object (must be closed later if desired).
    """
    if logfile is None:
        logfile = create_logfile(logs_dir, prefix)

    # Replace sys.stdout and sys.stderr with Tee wrappers that also write to file
    sys.stdout = Tee(sys.__stdout__, logfile)
    sys.stderr = Tee(sys.__stderr__, logfile)

    return logfile
