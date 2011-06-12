import signal
from contextlib import contextmanager

class Timeout(Exception):
    pass

@contextmanager
def timeout(limit):
    def alarm(signum, frame):
        raise Timeout()
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(limit)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

def debork(f, default, limit):
    try:
        with timeout(limit):
            return f()
    except:
        return default

