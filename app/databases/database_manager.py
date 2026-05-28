import sqlite3


# -----------------------------------
# Connect to Database
# -----------------------------------

def connect_db():

    conn = sqlite3.connect(

        "ats_database.db"
    )

    return conn


# -----------------------------------
# Create Candidates Table
# -----------------------------------

def create_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT UNIQUE,

            phone TEXT,

            cgpa TEXT,

            semantic_score REAL,

            final_score REAL,

            recommendation TEXT,

            matched_skills TEXT,

            missing_skills TEXT,

            explanation TEXT
        )

    """)

    conn.commit()

    conn.close()


# -----------------------------------
# Check Existing Candidate
# -----------------------------------

def candidate_exists(email):

    conn = connect_db()

    cursor = conn.cursor()

    query = """

        SELECT * FROM candidates

        WHERE email = ?

    """

    cursor.execute(

        query,

        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# -----------------------------------
# Insert Candidate
# -----------------------------------

def insert_candidate(

    candidate
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO candidates (

            name,
            email,
            phone,
            cgpa,
            semantic_score,
            final_score,
            recommendation,
            matched_skills,
            missing_skills,
            explanation

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        candidate["Candidate Name"],

        candidate["Email"],

        candidate["Phone"],

        candidate["CGPA"],

        candidate["Semantic Score"],

        candidate["Final Score"],

        candidate["Recommendation"],

        candidate["Matched Skills"],

        candidate["Missing Skills"],

        candidate["Explanation"]

    ))

    conn.commit()

    conn.close()


# -----------------------------------
# Update Existing Candidate
# -----------------------------------

def update_candidate(

    candidate
):

    conn = connect_db()

    cursor = conn.cursor()

    query = """

        UPDATE candidates

        SET

            name = ?,
            phone = ?,
            cgpa = ?,
            semantic_score = ?,
            final_score = ?,
            recommendation = ?,
            matched_skills = ?,
            missing_skills = ?,
            explanation = ?

        WHERE email = ?

    """

    cursor.execute(

        query,

        (

            candidate["Candidate Name"],

            candidate["Phone"],

            candidate["CGPA"],

            candidate["Semantic Score"],

            candidate["Final Score"],

            candidate["Recommendation"],

            candidate["Matched Skills"],

            candidate["Missing Skills"],

            candidate["Explanation"],

            candidate["Email"]

        )
    )

    conn.commit()

    conn.close()


# -----------------------------------
# Save or Update Candidate
# -----------------------------------

def save_candidate(

    candidate
):

    if candidate_exists(

        candidate["Email"]
    ):

        update_candidate(

            candidate
        )

    else:

        insert_candidate(

            candidate
        )


# -----------------------------------
# Fetch All Candidates
# -----------------------------------

def fetch_candidates():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM candidates"
    )

    data = cursor.fetchall()

    conn.close()

    return data