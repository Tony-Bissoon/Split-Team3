# Edit - saves the recorded data in a new text file --> records history
import sqlite3

class TransactionDatabase:
    def __init__(self, db_name='transactions.db'): 

        self.conn = sqlite3.connect(db_name) # Initialize the database connection
        
        self.create_table() # Create the table 

    def create_table(self):
        
        cursor = self.conn.cursor() # to execute SQL commands

        # Create transactions table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        
        self.conn.commit() # Commit changes

    def add_transaction(self, date, amount, description):
        cursor = self.conn.cursor()

        # Insert a new transaction into the database
        cursor.execute('''
            INSERT INTO transactions (date, amount, description)
            VALUES (?, ?, ?)
        ''', (date, amount, description))
        

        self.conn.commit()

    def get_user_input(self):  # user input
        while True:
            date = input("Enter the date of the transaction (YYYY-MM-DD): ")
            if self.validate_date_format(date):
                break
            else:
                print("Wrong date format. Please enter again.")

        while True:
            amount_str = input("Enter the amount of the transaction: $ ")
            try:
                amount = float(amount_str)
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        description = input("Enter a description for the transaction: ")

        # Save transaction to text file
        with open('transactions.txt', 'a') as file:
            file.write(f"Date: {date}, Amount: ${amount}, Description: {description}\n")

        # Display recorded info
        print("Transaction recorded:")
        print(f"Date: {date}, Amount: ${amount}, Description: {description}")

        return date, amount, description

    def validate_date_format(self, date):
        try:
            year, month, day = map(int, date.split('-'))
            if 1 <= month <= 12 and 1 <= day <= 31:
                return True
            else:
                return False
        except ValueError:
            return False

    def close(self):
        # Close the db connection
        self.conn.close()

# main
if __name__ == "__main__":
    db = TransactionDatabase()
    date, amount, description = db.get_user_input()
    db.add_transaction(date, amount, description)
    db.close()
