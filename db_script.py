import mysql.connector
import time

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",              # change if using a different user
    password="root",          # update your password if needed
    database="ADBMS"
)

cursor = conn.cursor()

print("\n---- Instructor Table Data ----")
# Fetch all records from instrucor (note the spelling)
cursor.execute("SELECT * FROM instrucor")
instructors = cursor.fetchall()
for row in instructors:
    print(row)

print("\n---- Teaches Table Data ----")
# Fetch all records from Teaches
cursor.execute("SELECT * FROM Teaches")
teaches = cursor.fetchall()
for row in teaches:
    print(row)

# Measure query time without index
print("\n---- Query Performance Without Index ----")
start_time = time.time()
cursor.execute("SELECT * FROM Teaches WHERE ID = '10101'")
_ = cursor.fetchall()  # must fetch results to clear unread result
end_time = time.time()
print("Time without index:", end_time - start_time, "seconds")

# Create index on Teaches(ID)
print("\nCreating index 'idx_id' on Teaches(ID)...")
cursor.execute("CREATE INDEX idx_id ON Teaches(ID)")

# Measure query time with index
print("\n---- Query Performance With Index ----")
start_time = time.time()
cursor.execute("SELECT * FROM Teaches WHERE ID = '10101'")
_ = cursor.fetchall()
end_time = time.time()
print("Time with index:", end_time - start_time, "seconds")

# Optional: Drop the index (cleanup)
print("\nDropping index 'idx_id' from Teaches...")
cursor.execute("DROP INDEX idx_id ON Teaches")

# Done
cursor.close()
conn.close()
print("\nAll operations completed successfully.")
