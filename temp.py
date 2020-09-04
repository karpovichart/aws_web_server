from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import psycopg2
import argparse
import sys

hostName = "127.0.0.1"
serverPort = 8080


class workWithDB():
    dbHost: str
    dbPort: int
    dbName: str
    dbPass: str
    dbUser: str

    def __init__(self, dbHodt: str, dbName: str, dbUser: str, dbPass: str):
        self.dbHost = dbHodt
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


class HttpProcessor(BaseHTTPRequestHandler):
    db: workWithDB

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"hello !")

        self.db.doQuery(f'Insert into active(timee, ip) values(\'kek\',\'lolll\') ')


class MyServer(HTTPServer):
    db: workWithDB

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="./httpcat.py a program to get cat picture for a http status")
        parser.add_argument('-d', '--dbname', nargs='?', default='postgres', help="Database name")
        parser.add_argument('-ho', '--dbhost', nargs='?',
                            default='database-1.ckatb6zta7tl.eu-central-1.rds.amazonaws.com', help="Database host")
        parser.add_argument('-u', '--dbuser', nargs='?', default='postgres', help="Database username")
        parser.add_argument('-p', '--dbpass', nargs='?', default='qwerty123', help="Database password")
        parser.add_argument('-s', '--serverhost', nargs='?', default='localhost', help="Server host")
        parser.add_argument('-po', '--serverport', type=int, nargs='?', default=8080, help="Server port")
        self.namespace = parser.parse_args(sys.argv[1:])
        type(self.namespace)
        self.db = workWithDB(self.namespace.dbhost, self.namespace.dbname, self.namespace.dbuser, self.namespace.dbpass)

        super().__init__(('localhost', 8080), HttpProcessor())  # todo change


# def do_GET(self):
#     self.send_response(200)
#     self.send_header("Content-type", "text/html")
#     self.end_headers()
#     self.wfile.write(bytes("ok", "utf-8"))
#     conn = psycopg2.connect(dbname=self.namespace.database, user=self.namespace.dbuser,
#                             password=self.namespace.dbpass, host=self.namespace.dbhost)
#     cursor = conn.cursor()
#     cursor.execute(f'Insert into test(timee, ip) values(\'{time.time()}\',\'{self.client_address[0]}\') ')
#     conn.commit()
#     conn.close()


if __name__ == "__main__":
    webServer = MyServer()
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
