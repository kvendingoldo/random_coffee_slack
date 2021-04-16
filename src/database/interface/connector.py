# -*- coding: utf-8 -*-

from loguru import logger


class Connector(object):
    def __init__(self, connection_pool):

        self.connection = connection_pool.get_connection()

        if self.connection.is_connected():
            info = self.connection.get_server_info()
            logger.info("Connected to MySQL database using connection pool ...")
            logger.info(f"Connected to MySQL Server version {info}")
            cursor = self.connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            logger.info(f"You're connected to database: {record}")

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            logger.info(f"MySQL connection is closed")

    def get(self, sql_statement):
        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            self.connection.commit()
            return cursor.fetchall()[0]

    def post(self, sql_statement):
        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            return self.connection.commit()
