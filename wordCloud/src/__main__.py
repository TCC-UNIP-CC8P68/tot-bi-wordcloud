import psycopg2
from .databaseConfig import config as dbConfig
from .databaseConnection import open, close

from .wordCloud import wordCloud
def main():
  conn = None
  try:
    params = dbConfig()

    print('Connecting to the PostgreSQL database...')
    conn = open(**params)
    cur = conn.cursor()

    wordCloud(cur, conn)

    conn.commit()

    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      close(conn)

if __name__ == '__main__':
  main()
