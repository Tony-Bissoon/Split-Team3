from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json

DATABASE_NAME = "transactions.db"

def fetch_transactions():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = [{"id": row[0], "date": row[1], "amount": row[2], "description": row[3]} for row in cursor.fetchall()]
    conn.close()
    return transactions

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/transactions':
            self._set_response()
            transactions = fetch_transactions()
            self.wfile.write(json.dumps(transactions).encode('utf-8'))
        else:
            self.send_error(404, "File Not Found: %s" % self.path)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
