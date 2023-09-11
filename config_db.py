import environ

env = environ.Env()
environ.Env.read_env()
POSTGRES_USER = env("POSTGRES_USER")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD")
POSTGRES_DB = env("POSTGRES_DB")
DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"