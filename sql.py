import sqlite3

def create_and_populate_table():
    # Connect to sqlite3
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    try:
        # Create the table if it doesn't exist
        table_info = """
        CREATE TABLE IF NOT EXISTS STUDENT (
            NAME VARCHAR(25),
            CLASS VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS INT
        );
        """
        cursor.execute(table_info)

        # Insert records into the table
        students = [
            ('Manoj', 'Data Eng', 'A', 95),
            ('Ajit', 'Analytics', 'B', 87),
            ('Reena', 'Data Science', 'B', 92),
            ('Vishal', 'Gen AI', 'A', 96),
            ('Alok', 'Data Eng', 'A', 92),
            ('Richard', 'Analytics', 'B', 91),
            ('Viv', 'Analytics', 'B', 84)
        ]

        cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", students)

        # Display records
        print("The inserted records are:")
        data = cursor.execute("SELECT * FROM STUDENT")
        for row in data:
            print(row)

        # Commit the transaction
        connection.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed
        connection.close()

if __name__ == "__main__":
    create_and_populate_table()
