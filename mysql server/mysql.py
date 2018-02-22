import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","testuser","test123","testdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """CREATE TABLE POST(
		ID INT,
		POST_URL VARCHAR(255),
		LOCATION VARCHAR(255),
		CONTENT TEXT)"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()