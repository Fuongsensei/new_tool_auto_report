import os
import sys


def get_app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


yaml_path: str = os.path.join(get_app_dir(), "Config", "config.yml")
yaml_path_home: str = yaml_path