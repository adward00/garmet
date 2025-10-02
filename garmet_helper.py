
import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="mg000220@",
    database="garmet",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)
    
    def fetch_stock(self):
        sql = "SELECT Numbers, Sort, Size, Price, Stock FROM Stock ORDER BY Numbers"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()  # [(id, name, email), ...]
            
    def insert_stock(self, Numbers, Sort, Size, Price, Stock):
        sql = "INSERT INTO stock (Numbers, Sort, Size, Price, Stock) VALUES (%s, %s, %s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (Numbers, Sort, Size, Price, Stock))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False        