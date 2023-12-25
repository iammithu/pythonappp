from flask import Flask, render_template, request, redirect, url_for, send_file, session
import sqlite3
import os
import io
from functools import wraps


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secure secret key for session management

port = int(os.environ.get('PORT', 5000))

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg TEXT,
                year TEXT,
                calss TEXT,
                section INTEGER,
                roll INTEGER,
                s_name_en TEXT,
                s_name_bn TEXT,
                f_name_en TEXT,
                f_name_bn TEXT,
                m_name_en TEXT,
                m_name_bn TEXT,
                dob TEXT,
                gender TEXT,
                Religion TEXT,
                disability TEXT,
                photo BLOB,
                number TEXT,
                vi TEXT,
                post TEXT,
                upazilla TEXT,
                district TEXT,
                students_id TEXT
            )
        ''')
        # Create a table for users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        # Add a sample user for demonstration
        cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('admin', '103789'))
        conn.commit()
# Custom decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if 'user_id' not in session:
            # Print or log for debugging
            print("User not logged in. Redirecting to login page.")
            print("Next URL:", request.url)
            # If not logged in, redirect to the login page
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_registered_students_count():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM students')
        count = cursor.fetchone()[0]
    return count

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('students.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()

        if user:
            # Store user information in the session
            session['user_id'] = user[0]
            # Print or log session for debugging
            print("Session after login:", session)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error=None)
# Logout route
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Home route
@app.route('/')
@login_required
def home():
    registered_students_count = get_registered_students_count()  # You need to implement this function
    return render_template('index.html', registered_students_count=registered_students_count)

@app.route('/form')
@login_required
def form():
    # Fetch the registered student number
    registered_students_count = get_registered_students_count()  # You need to implement this function

    return render_template('addmission.html', registered_students_count=registered_students_count)

# Display all students route
@app.route('/display_students')
@login_required
def display_students():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()

        # Get search parameters
        search_query = request.args.get('search', '')
        selected_class = request.args.get('class', '')
        selected_year = request.args.get('year', '')

        if selected_class and selected_year:
            query = 'SELECT * FROM students WHERE calss = ? AND year = ? AND (s_name_en LIKE ? OR s_name_bn LIKE ?) ORDER BY roll'
            params = (selected_class, selected_year, f'%{search_query}%', f'%{search_query}%')
        elif selected_class:
            query = 'SELECT * FROM students WHERE calss = ? AND (s_name_en LIKE ? OR s_name_bn LIKE ?) ORDER BY roll'
            params = (selected_class, f'%{search_query}%', f'%{search_query}%')
        elif selected_year:
            query = 'SELECT * FROM students WHERE year = ? AND (s_name_en LIKE ? OR s_name_bn LIKE ?) ORDER BY roll'
            params = (selected_year, f'%{search_query}%', f'%{search_query}%')
        else:
            query = 'SELECT * FROM students WHERE s_name_en LIKE ? OR s_name_bn LIKE ? OR gender LIKE? OR religion LIKE? OR vi LIKE? OR number LIKE? OR students_id LIKE? OR reg LIKE? ORDER BY roll '
            params = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')



        cursor.execute(query, params)
        students = cursor.fetchall()

    # Precompute row numbers
    
    registered_students_count = get_registered_students_count()  # You need to implement this function

    return render_template('display_students.html', students=students , registered_students_count=registered_students_count)




# ... (the rest of your routes remain the same)


# Display individual student route
@app.route('/display_student/<int:student_id>')
@login_required
def display_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()

    return render_template('display_student.html', student=student)

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
        reg = request.form['reg']
        year = request.form['year']
        calss = request.form['calss']
        section = request.form['section']
        roll = request.form['roll']
        s_name_en = request.form['s_name_en']
        s_name_bn = request.form['s_name_bn']
        f_name_en = request.form['f_name_en']
        f_name_bn = request.form['f_name_bn']
        m_name_en = request.form['m_name_en']
        m_name_bn = request.form['m_name_bn']
        dob = request.form['dob']
        gender = request.form['gender']
        Religion = request.form['Religion']
        disability = request.form.get('disability', '')
        # Handle photo upload
        if 'photo' in request.files:
            photo_file = request.files['photo']
            if photo_file.filename != '':
                photo_data = photo_file.read()
            else:
                photo_data = None
        else:
            photo_data = None

        number = request.form['number']
        vi = request.form['vi']
        post = request.form['post']
        upazilla = request.form['upazilla']
        district = request.form['district']

        students_id = request.form['students_id']

    # Insert data into the database
        with sqlite3.connect('students.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO students (reg, year, calss, section, roll, s_name_en, s_name_bn, f_name_en, f_name_bn, m_name_en, m_name_bn, dob, gender, Religion, disability, photo, number, vi, post, upazilla, district, students_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (reg, year, calss, section, roll, s_name_en, s_name_bn, f_name_en, f_name_bn, m_name_en, m_name_bn, dob, gender, Religion, disability, photo_data, number, vi, post, upazilla, district, students_id ))
            conn.commit()

        return redirect(url_for('form'))

# Edit student route
# Edit student route
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            # Handle photo upload
            if 'photo' in request.files:
                photo_file = request.files['photo']
                if photo_file.filename != '':
                    # Read the new photo data
                    photo_data = photo_file.read()
                else:
                    # If 'photo' is present but no file is selected, retain the existing photo
                    photo_data = cursor.execute('SELECT photo FROM students WHERE id = ?', (student_id,)).fetchone()[0]
            else:
                # If 'photo' is not present in the form, retain the existing photo
                photo_data = cursor.execute('SELECT photo FROM students WHERE id = ?', (student_id,)).fetchone()[0]

            # Update student data in the database
            cursor.execute('''
                UPDATE students
                SET reg=?, year=?, calss=?, section=?, roll=?, s_name_en=?, s_name_bn=?, f_name_en=?, f_name_bn=?, m_name_en=?, m_name_bn=?, dob=?, gender=?, Religion=?, disability=?, photo=?, number=?, vi=?, post=?, upazilla=?, district=?, students_id=?
                WHERE id=?
            ''', (
                request.form['reg'],
                request.form['year'],
                request.form['calss'],
                request.form['section'],
                request.form['roll'],
                request.form['s_name_en'],
                request.form['s_name_bn'],
                request.form['f_name_en'],
                request.form['f_name_bn'],
                request.form['m_name_en'],
                request.form['m_name_bn'],
                request.form['dob'],
                request.form['gender'],
                request.form['Religion'],
                request.form.get('disability', ''),  # Use get() to handle cases where 'disability' is not present in the form
                photo_data,
                request.form['number'],
                request.form['vi'],
                request.form['post'],
                request.form['upazilla'],
                request.form['district'],
                request.form['students_id'],
                student_id
            ))
            conn.commit()

            return redirect(url_for('display_students'))
        else:
            # Fetch the existing student data for editing
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()

    return render_template('edit_student.html', student=student)

# Delete student route
@app.route('/delete_student/<int:student_id>')
@login_required
def delete_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()

    return redirect(url_for('display_students'))

# Display student photo route
@app.route('/display_photo/<int:student_id>')
def display_photo(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT photo FROM students WHERE id = ?', (student_id,))
        result = cursor.fetchone()

    if result and result[0]:
        return send_file(io.BytesIO(result[0]), mimetype='image/jpeg')
    else:
        return 'Photo not found'


# Run the application
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
