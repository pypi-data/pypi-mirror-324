from box import Box
from . import contants
from django.conf import settings
from dotenv import load_dotenv, dotenv_values

load_dotenv()


def env(key, default=None):
    from os import environ

    return environ.get(key, default=str(default))


def DJANGO_SETTINGS_MODULE():
    import django
    from os import environ

    module = env("settings", "web.settings")
    environ.setdefault("DJANGO_SETTINGS_MODULE", module)
    django.setup()


def reader(path=".yaml"):
    import yaml
    import json

    if not path:
        raise ValueError("Path must not be empty.")

    if path.endswith(".yaml"):
        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    elif path.endswith(".json"):
        with open(path, "r") as file:
            return json.load(file)
    elif path.endswith(".env"):
        return dotenv_values(path)
    elif path.endswith(".log"):
        with open(path, "r") as file:
            return file.readlines()
    elif path.endswith(".txt"):
        with open(path, "r") as file:
            return file.readlines()
    else:
        raise ValueError(f"Unsupported file format for path: {path}")


config = Box(reader(env("config", ".yaml")))
DJANGO_SETTINGS_MODULE()
from .models import *  # noqa
