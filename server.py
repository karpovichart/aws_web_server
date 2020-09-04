from flask import Flask, request
import psycopg2
import time
import subprocess
import argparse
import sys


class WorkWithDB:
    dbHost: str
    dbPort: int
    dbName: str
    dbPass: str
    dbUser: str

    def __init__(self, dbHost: str, dbName: str, dbUser: str, dbPass: str):
        self.dbHost = dbHost
        # self.dbPort = dbPort
        self.dbName = dbName
        self.dbUser = dbUser
        self.dbPass = dbPass
        self.doQuery('Create table  IF NOT EXISTS active(ID  SERIAL PRIMARY KEY, timee TEXT, ip TEXT)')

    def doQuery(self, query: str):
        conn = psycopg2.connect(dbname=self.dbName, user=self.dbUser,
                                password=self.dbPass, host=self.dbHost)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()


def file_work(query: str):
    path = "/srv/log.txt"
    print("file up start")
    with open(path, 'at') as f:
        f.write(query + '\n')
        print("file updated")


# if not os.path.exists(path):
#     f = open(path, 'wt')
#     f.write('0-0')
#     f.close()
# else:


def aws_s3_work_first_connect():
    path = "log.txt"
    bucket = "testbbucket31"

    s = subprocess.check_output('aws s3 ls', shell=True)
    s = str(s)
    if s.find(bucket) == -1:
        query = "aws s3 mb s3://" + bucket
        print("bucket created")
    else:
        query = f"aws s3 cp   s3://{bucket}/log.txt /srv/ "
        print("file downloaded")
    subprocess.call(query, shell=True)


def aws_s3_work_update_file():
    path = "log.txt"
    bucket = "testbbucket31"
    query = f"aws s3 cp /srv/log.txt  s3://{bucket} "
    print("file uploaded to aws")
    subprocess.call(query, shell=True)


app = Flask(__name__)
parser = argparse.ArgumentParser(
    description="webserver")
parser.add_argument('-d', '--dbname', nargs='?', default='postgres', help="Database name")
parser.add_argument('-ho', '--dbhost', nargs='?', default='localhost', help="Database host")
parser.add_argument('-u', '--dbuser', nargs='?', default='postgres', help="Database username")
parser.add_argument('-p', '--dbpass', nargs='?', default='qwerty123', help="Database password")
parser.add_argument('-s', '--serverhost', nargs='?', default='localhost', help="Server host")
# parser.add_argument('-po', '--serverport', type=int, nargs='?', default=8080, help="Server port")
cred = parser.parse_args(sys.argv[1:])
db = WorkWithDB(cred.dbhost, cred.dbname, cred.dbuser, cred.dbpass)
aws_s3_work_first_connect()


@app.route('/')
def index():
    db.doQuery(f'Insert into active(timee, ip) values(\'{time.time()}\',\'{str(request.remote_addr)}\') ')
    # s3 = WorkWithAWSS3("aaa.huy")
    # s3.sync_bucket("", "", "log.txt")

    file_work(f'{time.time()}-{str(request.remote_addr)}')
    aws_s3_work_update_file()
    # file = WorkWithFile
    # file.print_path
    # file.write_info( f'{time.time()}-{str(request.remote_addr)}')
    # s3.sync_bucket("", "", "log.txt")
    return 'HI!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
# app.run(host="127.0.0.1", port=8080)
