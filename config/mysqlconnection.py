import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',  # Cambiar según tus credenciales locales de MySQL
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid
                elif query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                else:
                    return True
            except Exception as e:
                print("Error en Base de Datos:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
