from mongoengine import connect


def connection(database: str = "vb_tg", host: str = "localhost", port: int = 27017, username: str = None,
               password: str = None, authentication_source: str = None):
    connect(
            database,
            host=host,
            port=port,
            username=username,
            password=password,
            authentication_source=authentication_source
    )
