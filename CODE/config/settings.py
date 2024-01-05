import psycopg2
from psycopg2 import sql

db_user = 'postgres'
db_password = '12345'
db_host = 'localhost'
db_port = 5432
db_name = 'Chainnews'

def execute_query(query):
    try:
        # Kết nối đến cơ sở dữ liệu PostgreSQL
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )

        if connection:
            # Tạo con trỏ
            cursor = connection.cursor()

            # Thực thi truy vấn
            cursor.execute(query)

            # Nếu truy vấn là SELECT, lấy tất cả dòng dữ liệu
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                affected_rows = cursor.rowcount
                return f"Query executed successfully. {affected_rows} rows affected."

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()

def execute_query_with_params(query, params):
    try:
        # Kết nối đến cơ sở dữ liệu PostgreSQL
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )

        if connection:
            # Tạo con trỏ
            cursor = connection.cursor()

            # Thực thi truy vấn với tham số
            cursor.execute(query, params)

            # Nếu truy vấn là SELECT, lấy tất cả dòng dữ liệu
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            else:
                # Commit thay đổi và lấy số dòng bị ảnh hưởng
                connection.commit()
                affected_rows = cursor.rowcount
                return f"Query executed successfully. {affected_rows} rows affected."

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()