import logging
import os
import time

import psycopg2

logger = logging.getLogger(__name__)

LIMIT_RETRIES = 5


class Database():
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.db = os.getenv('POSTGRES_DB')

        self.reconnect = True
        self.conn = None
        self.retry_counter = 0

        logger.debug('POSTGRES_HOST: %s', self.host)
        logger.debug('POSTGRES_PORT: %s', self.port)
        logger.debug('POSTGRES_USER: %s', self.user)
        logger.debug('POSTGRES_PASSWORD: %s', self.password)
        logger.debug('POSTGRES_DB: %s', self.db)

        self.connect(self)

        self.cur = self.conn.cursor()
        self._create_extensions()

    def connect(self, retry_counter=0):
        if not self.conn:
            time.sleep(5)
            try:
                self.conn = psycopg2.connect(
                    database=self.db,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    connect_timeout=3,)

                self.conn.autocommit = False
                return self.conn
            except psycopg2.OperationalError as error:
                if not self.reconnect or self.retry_counter >= LIMIT_RETRIES:
                    raise error
                else:
                    self.retry_counter += 1
                    print("got error {}. reconnecting {}".format(
                        str(error).strip(), self.retry_counter))
                    time.sleep(5)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                raise error

    def query(self, query):
        self.cur.execute(query)

    def cursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
        logger.info('Successfully closed db connection')

    def create_tables(self):
        create_table_query = '''DROP TABLE IF EXISTS users;
                                CREATE TABLE users
            (ID SERIAL PRIMARY KEY,
            name           varchar    NOT NULL,
            nationality           varchar    NOT NULL,
            latitude           float8,
            longitude float8); '''
        logger.info('Creating database tables')

        self.query(create_table_query)
        self.commit()
        logger.info('Successfully created db table "users"')

    def _create_extensions(self):
        create_ext_query = '''
            create extension if not exists cube;
            create extension if not exists earthdistance;
            '''
        logger.info('Creating pg extensions')
        self.query(create_ext_query)
        self.commit()
        logger.info('Successfully created pg extensions')
