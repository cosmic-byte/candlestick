from enum import Enum

from environs import Env


env = Env()
APPLICATION_ENV = env("APPLICATION_ENV", None)
env_path = f".env.{APPLICATION_ENV}" if APPLICATION_ENV else None
env.read_env(env_path)


class ApplicationEnv(Enum):
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


application_env = env("APPLICATION_ENV", ApplicationEnv.DEV.value)


CONFIG: dict = {
    "app": {
        "env": application_env,
        "logger": env("LOGGER_TYPE", "console"),
    },
    "repository": {
        "type": env("REPOSITORY_TYPE", "postgres"),
        "postgres": {
            "db_url": env(
                "REPOSITORY_POSTGRES_DB_URL",
                "postgresql+psycopg2://postgres:password@postgres/candlestick",
            )
        },
    },
    "port": {
        "stream_provider": {
            "type": env("STREAM_PROVIDER_TYPE", "partner"),
            "partner": {
                "host": env("PARTNER_STREAM_HOST", default="ws://stream_server"),
                "port": env("PARTNER_STREAM_port", default="8032"),
            },
        },
    },
}
