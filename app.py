import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'leave_system'
}

def get_db():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    if session.get('user_id'):
        if session['role'] == 'admin':
            return redirect(url_for('admindashboard'))
        else:
            return redirect(url_for('employeedashboard'))
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'employee'

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                           (username, password, role))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admindashboard'))
            else:
                return redirect(url_for('employeedashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Employee Dashboard
@app.route('/employeedashboard')
def employeedashboard():
    if session.get('user_id') and session['role'] == 'employee':
        return render_template('employeedashboard.html')
    return redirect(url_for('login'))

# Admin Dashboard
@app.route('/admindashboard')
def admindashboard():
    if session.get('user_id') and session['role'] == 'admin':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT lr.id, u.username, lr.start_date, lr.end_date, lr.reason, lr.status
            FROM leave_requests lr
            JOIN users u ON lr.user_id = u.id
        """)
        leaves = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admindashboard.html', leaves=leaves)
    return redirect(url_for('login'))

# Apply Leave
@app.route('/applyleave', methods=['GET', 'POST'])
def applyleave():
    if session.get('user_id') and session['role'] == 'employee':
        if request.method == 'POST':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            reason = request.form['reason']

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leave_requests (user_id, start_date, end_date, reason, status) VALUES (%s,%s,%s,%s,%s)",
                (session['user_id'], start_date, end_date, reason, 'Pending')
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('myleaves'))
        return render_template('applyleave.html')
    return redirect(url_for('login'))

# My Leaves
@app.route('/myleaves')
def myleaves():
    if session.get('user_id') and session['role'] == 'employee':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM leave_requests WHERE user_id=%s", (session['user_id'],))
        leaves = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('myleaves.html', leaves=leaves)
    return redirect(url_for('login'))

@app.route('/handle_leave/<int:leave_id>/<action>')
def handle_leave(leave_id, action):
    if session.get('user_id') and session['role'] == 'admin':
        if action not in ['Approved', 'Rejected']:
            return "Invalid action", 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE leave_requests SET status=%s WHERE id=%s", (action, leave_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admindashboard'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
