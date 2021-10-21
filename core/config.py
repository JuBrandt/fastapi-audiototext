from starlette.config import Config

config = Config(".env_dev")

DATABASE_URL = config("VIDEOV_TO_TEXT_DATABASE_URL", cast=str, default="")
