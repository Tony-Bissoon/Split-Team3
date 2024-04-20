# README: This code supports the manually split functionality of the app. The user is prompted to enter the expenses and people. 
        # The app then splits the cost either evenly or itemized (with an even split on tax and tips). 
        # The transaction is then stored in a database for a history view (another functionality of the app).

import sqlite3

class TransactionDatabase:
    def __init__(self, db_name='transactions.db'): 
        self.conn = sqlite3.connect(db_name)  # Initialize the database connection
        self.create_table()  # Create the table 

    def create_table(self):
        cursor = self.conn.cursor()  # to execute SQL commands

        # Create transactions table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        
        self.conn.commit()  # Commit changes

    def add_transaction(self, date, amount, description):
        cursor = self.conn.cursor()

        # Insert a new transaction into the database
        cursor.execute('''
            INSERT INTO transactions (date, amount, description)
            VALUES (?, ?, ?)
        ''', (date, amount, description))

        self.conn.commit()

    def get_user_input(self):
        date = input("Enter the date of the transaction (YYYY-MM-DD): ")
        while not self.validate_date_format(date):
            print("Wrong date format. Please enter again.")
            date = input("Enter the date of the transaction (YYYY-MM-DD): ")

        amount = float(input("Enter the total amount spent: $ "))
        tax = float(input("Enter the tax amount: $ "))
        tips = float(input("Enter the tips amount: $ "))

        persons = {}
        while True:
            name = input("Enter the name of the person (or 'done' to finish): ")
            if name.lower() == 'done':
                break
            spent = float(input(f"Enter the amount spent by {name}: $ "))
            persons[name] = spent

        split_type = input("Split share evenly or by person (even/person): ").lower()

        return date, amount, tax, tips, persons, split_type

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

    def calculate_and_save_splits(self, date, total_amount, tax, tips, persons, split_type):
        if split_type == 'even':
            total_cost = total_amount + tax + tips
            amount_per_person = total_cost / len(persons)
            
            for name in persons:
                self.add_transaction(date, amount_per_person, f"{name} - Even Split")

                # Save to text file
                with open('transactions.txt', 'a') as file:
                    file.write(f"Date: {date}, Amount: ${amount_per_person}, Description: {name} - Even Split\n")

                print(f"{name} owes: ${amount_per_person}")

        elif split_type == 'person':
            total_spent = sum(persons.values())
            total_cost = total_spent + tax + tips
            
            for name, spent in persons.items():
                personal_share = spent + (tax + tips) / len(persons)
                self.add_transaction(date, personal_share, f"{name} - Personal Share")

                # Save to text file
                with open('transactions.txt', 'a') as file:
                    file.write(f"Date: {date}, Amount: ${personal_share}, Description: {name} - Personal Share\n")

                print(f"{name} owes: ${personal_share}")

# main
if __name__ == "__main__":
    db = TransactionDatabase()
    
    date, total_amount, tax, tips, persons, split_type = db.get_user_input()
    db.calculate_and_save_splits(date, total_amount, tax, tips, persons, split_type)
    
    db.close()
