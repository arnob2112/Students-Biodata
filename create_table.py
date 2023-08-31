import sqlite3

connection = sqlite3.connect("All Information.db")
cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS people (ID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, " \
                     "College TEXT, Age TEXT, Gender TEXT, Religion TEXT, Contact_Number TEXT, FB_URL TEXT, Job TEXT," \
                     "Image_Path TEXT, Username TEXT UNIQUE)"
cursor.execute(create_table_query)

create_usertable_query = "CREATE TABLE IF NOT EXISTS user (ID INTEGER PRIMARY KEY, Username TEXT, Password TEXT)"
cursor.execute(create_usertable_query)
connection.commit()
connection.close()