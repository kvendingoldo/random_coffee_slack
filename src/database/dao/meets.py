# -*- coding: utf-8 -*-


def add(db, user1, user2):
    sql_statement = f"INSERT IGNORE INTO meets (uid1, uid2) VALUES " \
                    f"(\"{user1.uid}\", " \
                    f"\"{user2.uid}\" "

    with db.cursor() as cursor:
        cursor.execute(sql_statement)
        db.commit()
    pass
