import psycopg2
import psycopg2.extras


# Database connection setup
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="Health-Fitness-Club",
        user="postgres",
        password="comp3005",
        port="5432",
    )


# Generic query execution helper
def execute_query(query, args=(), fetch=False):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, args)
    if fetch:
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    else:
        conn.commit()
        cursor.close()
        conn.close()
