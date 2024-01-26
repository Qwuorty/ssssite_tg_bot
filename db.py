import sqlite3
import datetime as dt


class Datebase:
    def __init__(self):
        self.db = sqlite3.connect('local_db.db', check_same_thread=False)
        self.sql = self.db.cursor()

    def get_all_orders(self):
        return self.sql.execute(f"SELECT * FROM orders").fetchall()

    def get_cost_by_basket(self, basket):
        ans = 0
        for tov_id, size in basket:
            sizes = self.sql.execute(f"SELECT * FROM sizes WHERE id='{tov_id}'").fetchone()[1].split(';')
            for i in sizes:
                if size == i.split(',')[0]:
                    ans += int((i.split(',')[1]).replace('¥',''))
        return ans