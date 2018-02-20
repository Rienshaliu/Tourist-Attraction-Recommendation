import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","testuser","test123","testdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """CREATE TABLE post(
		id INT NOT NULL AUTO_INCREMENT,
		post_url VARCHAR(255),
		location VARCHAR(255),
		content TEXT,
		PRIMARY KEY(id))"""
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