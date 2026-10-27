import mysql.connector

# Connect to MySQL Server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sujal123@"  # Enter your MySQL password
)
cursor = db.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS lab_db")
cursor.execute("USE lab_db")

# Create Equipment Table (Parent)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Equipment (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(100) NOT NULL,
        total_stock INT NOT NULL
    )
''')

# Create Borrow Records Table (Child with Foreign Key)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Borrow_Records (
        record_id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(100) NOT NULL,
        student_prn VARCHAR(15) NOT NULL,
        item_id INT,
        borrow_date DATE NOT NULL,
        FOREIGN KEY (item_id) REFERENCES Equipment(item_id)
    )
''')

# Insert Default Lab Equipment
cursor.execute("SELECT COUNT(*) FROM Equipment")
if cursor.fetchone()[0] == 0:
    equipment_data = [
        ('C8051F340 Development Board', 15),
        ('Digital Multimeter', 30),
        ('Digital Storage Oscilloscope', 10),
        ('Soldering Kit', 20)
    ]
    cursor.executemany("INSERT INTO Equipment (item_name, total_stock) VALUES (%s, %s)", equipment_data)
    print("Inserted initial lab equipment.")

db.commit()
db.close()
print("MySQL 'lab_db' database setup complete.")