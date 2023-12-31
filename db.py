import mysql.connector
global cnx 

# creating connection to the db
cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Imane2003.',
        database='expense_tracker'
    )

def insert_expense(expense_id, category, amount, date):
    try:
        cursor = cnx.cursor()
        # calling the store procedure.
        cursor.callproc('insert_new_expense', (expense_id, category, amount, date))
        # commiting the change
        
        cnx.commit()
        
        # closing the cursor
        cursor.close() 
        print("Expense inserted successfully")
        
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting expense : {err}")
        
        # rollback changes 
        cnx.rollback()
        
        return -1
    
    except Exception as e:
        print(f"An error occured : {e}")
        cnx.rollback()
        
        return -1

def get_next_expense_id():
    cursor = cnx.cursor()
    
    query = ("SELECT MAX(expense_id) FROM expense")
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    
    if result is None:
        return 1
    else:
        return result + 1


def insert_budget(budget_id, category, amount, start_date, end_date):
    try:
        cursor = cnx.cursor()
        # calling the store procedure.
        cursor.callproc('insert_new_budget', (budget_id, category, amount, start_date, end_date))
        # commiting the change
        
        cnx.commit()
        
        # closing the cursor
        cursor.close() 
        print("Budget inserted successfully")
        
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting Budget : {err}")
        
        # rollback changes 
        cnx.rollback()
        
        return -1
    
    except Exception as e:
        print(f"An error occured : {e}")
        cnx.rollback()
        
        return -1

def get_next_budget_id():
    cursor = cnx.cursor()
    
    query = ("SELECT MAX(budget_id) FROM budget")
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    
    if result is None:
        return 1
    else:
        return result + 1