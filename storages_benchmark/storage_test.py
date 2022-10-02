import time
import uuid
from contextlib import contextmanager
import random
import clickhouse_driver
import psycopg2
import psycopg2.extras
import vertica_python

test_batch = [
    {"film_id": uuid.uuid4(), "user_id": random.randint(1, 99999), "film_position_ms": 1} for _ in range(1000)
]


def roll_over_batch(func):
    def inner(*args, **kwargs):
        for test_obj in test_batch:
            start_time = time.monotonic()
            res = func(test_obj, *args, **kwargs)
            end_time = time.monotonic()
            yield end_time - start_time, res

    return inner


def repeat(n: int):
    def decorator(func):
        def inner(*args, **kwargs):
            for _ in range(n):
                start_time = time.monotonic()
                res = func(*args, **kwargs)
                end_time = time.monotonic()
                yield end_time - start_time, res

        return inner

    return decorator


def get_average_exec_time(func, n, *args, **kwargs):
    avg_time = sum(exec_time for exec_time, _ in repeat(n)(func)(*args, **kwargs)) / n
    return avg_time


def get_average_exec_time_over_batch(func, *args, **kwargs):
    n = len(test_batch)
    avg_time = sum(exec_time for exec_time, _ in roll_over_batch(func)(*args, **kwargs)) / n
    return avg_time


def test_postgres():
    psycopg2.extras.register_uuid()

    @contextmanager
    def pg_conn():
        conn = psycopg2.connect(host="localhost", port="5432", dbname="postgres", user="postgres", password="postgres")
        conn.set_session(autocommit=True)
        try:
            yield conn
        finally:
            conn.close()

    def test_read_speed():
        def test_select(test_obj, cur):
            return cur.execute("SELECT * FROM views WHERE film_id = %(film_id)s AND user_id = %(user_id)s", test_obj)

        with pg_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time_over_batch(test_select, cur)
            return avg_time

    def test_write_speed():
        def test_insert(test_obj, cur):
            cur.execute(
                "INSERT INTO views (film_id, user_id, film_position_ms) VALUES (%(film_id)s, %(user_id)s, %(film_position_ms)s);",
                test_obj,
            )

        with pg_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time_over_batch(test_insert, cur)
            return avg_time

    def test_agg_speed():
        def test_agg_select(cur):
            return cur.execute(
                """
                SELECT MAX(avg_film_position_ms)
                FROM (
                    SELECT t1.film_id, AVG(t1.film_position_ms) AS avg_film_position_ms
                    FROM (
                        SELECT film_id, user_id, MAX(film_position_ms) as film_position_ms 
                        FROM views GROUP BY film_id, user_id
                    ) as t1
                    GROUP BY t1.film_id
                ) as t2;
            """
            )

        with pg_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time(test_agg_select, 1, cur)
            return avg_time

    return {
        "read": test_read_speed(),
        "write": test_write_speed(),
        "agg": test_agg_speed(),
    }


def test_vertica():
    @contextmanager
    def vertica_conn():
        conn = vertica_python.connect(user="dbadmin")
        try:
            yield conn
        finally:
            conn.close()

    def test_read_speed():
        def test_select(test_obj, cur):
            return cur.execute("SELECT * FROM views WHERE film_id = :film_id AND user_id = :user_id", test_obj)

        with vertica_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time_over_batch(test_select, cur)
            return avg_time

    def test_write_speed():
        def test_insert(test_obj, cur):
            cur.execute(
                "INSERT INTO views (film_id, user_id, film_position_ms) VALUES (:film_id, :user_id, :film_position_ms);",
                test_obj,
            )

        with vertica_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time_over_batch(test_insert, cur)
            return avg_time

    def test_agg_speed():
        def test_agg_select(cur):
            return cur.execute(
                """
                SELECT MAX(avg_film_position_ms)
                FROM (
                    SELECT t1.film_id, AVG(t1.film_position_ms) AS avg_film_position_ms
                    FROM (
                        SELECT film_id, user_id, MAX(film_position_ms) as film_position_ms 
                        FROM views GROUP BY film_id, user_id
                    ) as t1
                    GROUP BY t1.film_id
                ) as t2;
            """
            )

        with vertica_conn() as conn, conn.cursor() as cur:
            avg_time = get_average_exec_time(test_agg_select, 10, cur)
            return avg_time

    return {
        "read": test_read_speed(),
        "write": test_write_speed(),
        "agg": test_agg_speed(),
    }


def test_clickhouse():
    @contextmanager
    def ch_conn():
        conn = clickhouse_driver.Client(host="localhost")
        try:
            yield conn
        finally:
            conn.disconnect()

    def test_read_speed():
        def test_select(test_obj, client):
            return client.execute("SELECT * FROM views WHERE film_id = %(film_id)s AND user_id = %(user_id)s", test_obj)

        with ch_conn() as client:
            avg_time = get_average_exec_time_over_batch(test_select, client)
            return avg_time

    def test_write_speed():
        def test_insert(test_obj, client):
            client.execute(
                "INSERT INTO views (film_id, user_id, film_position_ms) VALUES (%(film_id)s, %(user_id)s, %(film_position_ms)s);",
                test_obj,
            )

        with ch_conn() as client:
            avg_time = get_average_exec_time_over_batch(test_insert, client)
            return avg_time

    def test_agg_speed():
        def test_agg_select(client):
            return client.execute(
                """
                SELECT MAX(avg_film_position_ms)
                FROM (
                    SELECT t1.film_id, AVG(t1.film_position_ms) AS avg_film_position_ms
                    FROM (
                        SELECT film_id, user_id, MAX(film_position_ms) as film_position_ms 
                        FROM views GROUP BY film_id, user_id
                    ) as t1
                    GROUP BY t1.film_id
                ) as t2;
            """
            )

        with ch_conn() as client:
            avg_time = get_average_exec_time(test_agg_select, 10, client)
            return avg_time

    return {
        "read": test_read_speed(),
        "write": test_write_speed(),
        "agg": test_agg_speed(),
    }


if __name__ == "__main__":
    results = {
        "postgres": test_postgres(),
        "vertica": test_vertica(),
        "clickhouse": test_clickhouse(),
    }
    headers = ("name", "read", "write", "agg")
    fmt = "{:>10} {:>10} {:>10} {:>10}"

    print(fmt.format(*headers))
    for k, v in sorted(results.items(), key=lambda x: (x[1]["agg"], x[1]["read"], x[1]["write"])):
        print(fmt.format(k, *[round(x, 4) for x in v.values()]))
