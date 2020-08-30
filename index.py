import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='qwerty123', host='database-1.ckatb6zta7tl.eu-central-1.rds.amazonaws.com')
    cursor = conn.cursor()
    cursor.execute("Insert into test(timee, ip) values('lol','kek' ) ")
    conn.commit()
    conn.close()
''' Create table  IF NOT EXISTS active(ID  SERIAL PRIMARY KEY, timee TEXT, ip TEXT)'''
    # 'database-1.ckatb6zta7tl.eu-central-1.rds.amazonaws.com'

