import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    address TEXT,
    bloodgp TEXT,
    contact TEXT,
    fathername TEXT,
    mothername TEXT
);
''')

# Clear existing data (optional, so you don't get duplicate inserts on rerun)
cursor.execute('DELETE FROM students;')

# Insert sample data into the correct table 'students'
cursor.execute("INSERT INTO students (name, age, address, bloodgp, contact, fathername, mothername) VALUES ('Rohan Sharma', 21, 'Chandigarh', 'O+', '9876543210', 'Anil Sharma', 'Sunita Sharma');")
cursor.execute("INSERT INTO students (name, age, address, bloodgp, contact, fathername, mothername) VALUES ('Priya Singh', 22, 'Mohali', 'A+', '8765432109', 'Rajesh Singh', 'Anita Singh');")

conn.commit()
conn.close()

print("Database 'student.db' created and populated successfully.")
