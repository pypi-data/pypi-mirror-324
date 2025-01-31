
def get_postgresql_connection():
    """Get the PostgreSQL connection using psycopg2."""
    import psycopg2  # For PostgreSQL
    from config.settings import settings

    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_database,
        user=settings.db_username,
        password=settings.db_password
    )
    return conn