import os
import envdir

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simplestats.standalone.settings")

CONFIG_DIR = os.path.expanduser('~/.config/simplestats')

if os.path.exists(CONFIG_DIR):
    envdir.open(CONFIG_DIR)
