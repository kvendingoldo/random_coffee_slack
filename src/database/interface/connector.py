class Connector(object):
    def __init__(self, db):
        self.db = db

    def get(self, sql_statement):
        with self.db.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            self.db.commit()
            return cursor.fetchall()[0]

    def post(self, sql_statement):
        with self.db.cursor(buffered=True) as cursor:
            cursor.execute(sql_statement)
            return self.db.commit()
