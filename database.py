from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

env = Env()
env.read_env()


def get_engine():
    if env.str("ENV") == "dev":
        url = f'{env("DATABASE")}://{env.str("DB_USER")}:{env.str("DB_PWD")}@{env.str("DB_HOST")}:{env("DB_PORT")}/{env.str("DB")}'
    else:
        url = env.str("DATABASE_URL")
    engine = create_engine(url=url)
    return engine


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session


if __name__ == "__main__":
    session = get_session()
    print(session)
