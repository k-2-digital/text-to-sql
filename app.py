import streamlit as st
import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    return response.text.replace("```sql", "").replace("```", "").strip()

# Function to retrieve SQL queries from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.commit()
        conn.close()

# Define prompt for the model
prompt = [
    """
    You are an expert converting English language into SQL query!
    The SQL database has table name STUDENT and has the following columns: [NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT]
    
    For example:
    Example-1 - How many total records in the table. The SQL command will be like this: SELECT COUNT(*) FROM STUDENT
    Example-2 - Tell me the students who are studying in class Analytics. The SQL command will be like this: SELECT * FROM STUDENT WHERE CLASS = 'Analytics'
    Example-3 - Show me all the students records sorted by their marks. The SQL command will be like this: SELECT * FROM STUDENT ORDER BY MARKS
    Example-4 - List the names of students who scored more than 90. The SQL command will be like this: SELECT NAME FROM STUDENT WHERE MARKS > 90
    Example-5 - Find the average marks of students in section A. The SQL command will be like this: SELECT AVG(MARKS) FROM STUDENT WHERE SECTION = 'A'
    Example-6 - Count the number of students in each class. The SQL command will be like this: SELECT CLASS, COUNT(*) FROM STUDENT GROUP BY CLASS
    Example-7 - Retrieve the highest mark in the class Data Eng. The SQL command will be like this: SELECT MAX(MARKS) FROM STUDENT WHERE CLASS = 'Data Eng'
    Example-8 - Get the details of students whose names start with 'A'. The SQL command will be like this: SELECT * FROM STUDENT WHERE NAME LIKE 'A%'
    
    Also, SQL should not have ``` in the beginning or end SQL word in output
    """
]


# Streamlit app
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App to retrieve SQL data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(f"Generated SQL: {response}")
    data = read_sql_query(response, "student.db")
    st.subheader("The response is ")
    for row in data:
        print(row)
        st.header(row)
