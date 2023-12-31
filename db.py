import mysql.connector
global cnx 

# creating connection to the db
cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Imane2003.',
        database='expense_tracker'
    )