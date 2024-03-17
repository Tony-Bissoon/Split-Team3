import sqlite3

class TransactionDatabase:
    def __init__(self, db_name='transactions.db'):
        # Initialize the database connection
        self.conn = sqlite3.connect(db_name)
        # Create the table if it doesn't exist
        self.create_table()

    def create_table(self):
        # Create a cursor object to execute SQL commands
        cursor = self.conn.cursor()
        # Create the transactions table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        # Commit the changes
        self.conn.commit()

    def add_transaction(self, date, amount, description):
        # Create a cursor object to execute SQL commands
        cursor = self.conn.cursor()
        # Insert a new transaction into the database
        cursor.execute('''
            INSERT INTO transactions (date, amount, description)
            VALUES (?, ?, ?)
        ''', (date, amount, description))
        
        # Commit the changes
        self.conn.commit()

    def close(self):
        # Close the database connection
        self.conn.close()
