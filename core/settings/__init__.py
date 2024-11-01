from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env("SECRET_KEY")

if env.bool("PROD", default=False):
    from core.settings.production import *
else:
    from core.settings.development import *
