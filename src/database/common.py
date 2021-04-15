# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error


# TODO: Migrate from prints to loguru
def get_db(host, port, user, password, db):
    try:
        connection = mysql.connector.connect(host=host,
                                             port=port,
                                             database=db,
                                             user=user,
                                             password=password)
        if connection.is_connected():
            info = connection.get_server_info()
            print("Connected to MySQL Server version ", info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
