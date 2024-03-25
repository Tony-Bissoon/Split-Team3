from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
from urllib.parse import urlparse, parse_qs

DATABASE_NAME = "transactions.db"

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

def fetch_transactions(userId):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE userId = ?", (userId,))
    rows = cursor.fetchall()
    if not rows:
        return {"message": "No transactions found for the specified user."}
    transactions = [{"id": row[0], "date": row[1], "amount": row[2], "description": row[3], "userId": row[4]} for row in rows]
    conn.close()
    return transactions

def fetch_transactions_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    if not rows:
        return {"message": "No transactions found."}
    transactions = [{"id": row[0], "date": row[1], "amount": row[2], "description": row[3], "userId": row[4]} for row in rows]
    conn.close()
    return transactions


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path, query_string = parsed_path.path, parsed_path.query
        query_params = parse_qs(query_string)

        if path == '/transactions':
            self._set_response()
            userId = query_params.get('userId', [None])[0]
            if userId and userId.isdigit():
                response = fetch_transactions(userId)
            else:
                response = fetch_transactions_all()

            # Check if the response is a message or a list of transactions
            if isinstance(response, dict) and "message" in response:
                self.wfile.write(json.dumps(response).encode('utf-8'))  # Sends the message as JSON
            else:
                self.wfile.write(json.dumps(response).encode('utf-8'))  # Sends the transactions as JSON
        else:
            self.send_error(404, "File Not Found: %s" % self.path)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
