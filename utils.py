import os
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def ensure_dirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)
