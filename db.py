import mysql.connector
global cnx 

# creating connection to the db
cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
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
    

def query_expense(category, date, start_date, end_date):
    sql_query = """
        SELECT SUM(e.amount)
        FROM expense e
        INNER JOIN category c ON e.category_id = c.category_id
        WHERE 1=1
    """

    if start_date and end_date:
        sql_query += f" AND e.expense_date BETWEEN '{start_date}' AND '{end_date}'"
    if category:
        sql_query += f" AND c.category_name = '{category}'"
    
    if date:
        sql_query += f" AND e.expense_date = '{date}'"
    
    try:
        cursor = cnx.cursor()
        cursor.execute(sql_query)
        total_spending = cursor.fetchone()[0]
        cursor.close()

        return total_spending

    except mysql.connector.Error as err:
        print(f"Error querying expenses: {err}")
        cnx.rollback()
        
        return -1
    
    except Exception as e:
        print(f"An error occured : {e}")
        cnx.rollback()
        
        return -1