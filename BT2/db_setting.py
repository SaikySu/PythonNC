# db_operations.py
import psycopg2
from psycopg2 import sql

class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, dbname, user, password, host, port):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            return True, "Kết nối đến cơ sở dữ liệu thành công!"
        except Exception as e:
            return False, f"Lỗi khi kết nối đến cơ sở dữ liệu: {e}"

    def fetch_all_data(self, table_name):
        """Fetch all data from specified table"""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            self.cur.execute(query)
            return True, self.cur.fetchall()
        except Exception as e:
            return False, f"Lỗi khi tải dữ liệu: {e}"

    def insert_data(self, table_name, id_value, ho_value, ten_value):
        """Insert new record into database"""
        try:
            insert_query = sql.SQL("INSERT INTO {} (id, ho, ten) VALUES (%s, %s, %s)").format(
                sql.Identifier(table_name))
            self.cur.execute(insert_query, (id_value, ho_value, ten_value))
            self.conn.commit()
            return True, "Dữ liệu đã được thêm thành công!"
        except Exception as e:
            self.conn.rollback()
            return False, f"Lỗi khi thêm dữ liệu: {e}"

    def delete_data(self, table_name, id_value):
        """Delete record from database"""
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(table_name))
            self.cur.execute(delete_query, (id_value,))
            self.conn.commit()
            return True, "Dữ liệu đã được xóa thành công!"
        except Exception as e:
            self.conn.rollback()
            return False, f"Lỗi khi xóa dữ liệu: {e}"

    def close(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()