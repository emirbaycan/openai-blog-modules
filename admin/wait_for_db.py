import sys, time
import psycopg2

HOST = sys.argv[1]
PORT = int(sys.argv[2])
USER = sys.argv[3]
PASSWORD = sys.argv[4]
DBNAME = sys.argv[5]
TIMEOUT = int(sys.argv[6]) if len(sys.argv) > 6 else 60

start = time.time()
while True:
    try:
        conn = psycopg2.connect(
            dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.close()
        print("DB is ready!")
        break
    except Exception as e:
        if time.time() - start > TIMEOUT:
            print("Timeout reached while waiting for db!")
            sys.exit(1)
        print("Waiting for DB:", e)
        time.sleep(2)
