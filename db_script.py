import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",    # ✅ Replace with actual password
    database="ADBMS"           # ✅ Replace with actual database
)
cursor = conn.cursor()

# 1. Create a view of instructors without their salary
cursor.execute("CREATE OR REPLACE VIEW faculty AS SELECT ID, name, dept_name FROM instructor")

# 2. Create a view of department salary totals
cursor.execute("""
    CREATE OR REPLACE VIEW dept_salary_totals AS 
    SELECT dept_name, SUM(salary) AS total_salary 
    FROM instructor 
    GROUP BY dept_name
""")

# 3. Create a role named student
cursor.execute("CREATE ROLE IF NOT EXISTS `student`")

# 4. Give SELECT privileges on view faculty to the role student
cursor.execute("GRANT SELECT ON faculty TO `student`")

# 5. Create a new user and assign the student role
cursor.execute("CREATE USER IF NOT EXISTS 'student_user'@'localhost' IDENTIFIED BY 'password123'")
cursor.execute("GRANT `student` TO 'student_user'@'localhost'")

# 6. Revoke privileges of the new user
cursor.execute("REVOKE `student` FROM 'student_user'@'localhost'")

# 7. Remove the role of student
cursor.execute("DROP ROLE IF EXISTS `student`")

# 8. Give SELECT privileges directly to the user
cursor.execute("GRANT SELECT ON faculty TO 'student_user'@'localhost'")

# 9. Create table teaches2 with ENUM constraint on semester
cursor.execute("""
    CREATE TABLE IF NOT EXISTS teaches2 (
        ID VARCHAR(10),
        course_id VARCHAR(10),
        sec_id VARCHAR(10),
        semester ENUM('Fall', 'Winter', 'Spring', 'Summer'),
        year INT
    )
""")

# 10. Index timing comparison on teaches.ID
try:
    cursor.execute("DROP INDEX idx_id ON teaches")
except:
    pass  # Ignore if index doesn't exist

start = time.time()
cursor.execute("SELECT * FROM teaches WHERE ID = '10101'")
print("Time without index:", time.time() - start)

cursor.execute("CREATE INDEX idx_id ON teaches(ID)")

start = time.time()
cursor.execute("SELECT * FROM teaches WHERE ID = '10101'")
print("Time with index:", time.time() - start)

# 11. Drop index to free space
cursor.execute("DROP INDEX idx_id ON teaches")

# Final commit and cleanup
conn.commit()
cursor.close()
conn.close()
