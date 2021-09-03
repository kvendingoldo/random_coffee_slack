# -*- coding: utf-8 -*-

from loguru import logger


class Connector:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.connection = connection_pool.get_connection()

        if self.connection.is_connected():
            info = self.connection.get_server_info()
            logger.info("Connected to MySQL database using connection pool ...")
            logger.info(f"Connected to MySQL Server version {info}")
            cursor = self.connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            logger.info(f"Connected to database: {record}")

    def __check_connection(self):
        if not self.connection.is_connected():
            self.connection = self.connection_pool.get_connection()
            logger.info("MySQL connection updated to new one from connection pool")
        else:
            logger.info("MySQL connection is fine")

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection is closed")

    def get(self, sql_statement):
        self.__check_connection()

        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            self.connection.commit()
            return cursor.fetchall()

    def post(self, sql_statement):
        self.__check_connection()

        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            return self.connection.commit()
