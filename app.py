import os
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


# ---------------------------------------------------------------
# LOGIN REQUIRED HELPER
# ---------------------------------------------------------------

def is_logged_in():
    return "user_id" in session


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Invalid username or password")

    return render_template("index.html")


# ---------------------------------------------------------------
# SIGNUP
# ---------------------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            user_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO personal_details (user_id, full_name, email) VALUES (%s, %s, %s)",
                (user_id, full_name, email)
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            conn.rollback()
            cursor.close()
            conn.close()
            return render_template("signup.html", error="Username or email already exists")

        cursor.close()
        conn.close()
        return redirect(url_for("index"))

    return render_template("signup.html")


# ---------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------------------------------------------------------------
# DASHBOARD  (list all records + search)
# ---------------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("index"))

    search_query = request.args.get("q", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search_query:
        cursor.execute(
            "SELECT * FROM personal_details WHERE full_name LIKE %s",
            (f"%{search_query}%",)
        )
    else:
        cursor.execute("SELECT * FROM personal_details")

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("dashboard.html", records=records, search_query=search_query)


# ---------------------------------------------------------------
# ADD PERSON
# ---------------------------------------------------------------

@app.route("/add_person", methods=["GET", "POST"])
def add_person():
    if not is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        full_name = request.form["full_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO personal_details
               (user_id, full_name, dob, gender, phone, email, address)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (session["user_id"], full_name, dob, gender, phone, email, address)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_person.html")


# ---------------------------------------------------------------
# EDIT PERSON
# ---------------------------------------------------------------

@app.route("/edit_person/<int:person_id>", methods=["GET", "POST"])
def edit_person(person_id):
    if not is_logged_in():
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        full_name = request.form["full_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        cursor.execute(
            """UPDATE personal_details
               SET full_name=%s, dob=%s, gender=%s, phone=%s, email=%s, address=%s
               WHERE person_id=%s""",
            (full_name, dob, gender, phone, email, address, person_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

    cursor.execute("SELECT * FROM personal_details WHERE person_id = %s", (person_id,))
    person = cursor.fetchone()
    cursor.close()
    conn.close()

    if person is None:
        return redirect(url_for("dashboard"))

    return render_template("edit_person.html", person=person)


# ---------------------------------------------------------------
# DELETE PERSON
# ---------------------------------------------------------------

@app.route("/delete_person/<int:person_id>")
def delete_person(person_id):
    if not is_logged_in():
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal_details WHERE person_id = %s", (person_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)