from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db   # your models.py has db + tables

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------- DATABASE SETUP -----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()   # creates all tables defined in models.py


# ----------------- LOGIN / DASHBOARD -----------------
@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin":
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ----------------- CUSTOMERS MODULE (Teammate A) -----------------
@app.route('/customers')
def customers():
    return render_template('customers.html')


# ----------------- BOOKINGS MODULE (Teammate B) -----------------
@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


# ----------------- ROOMS MODULE (Teammate C) -----------------
@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    from models import Room

    if request.method == "POST":
        room_no = request.form["room_no"]
        room_type = request.form["type"]

        if not room_no or not room_type:
            flash("All fields are required.", "danger")
            return redirect(url_for("rooms"))

        try:
            room_no = int(room_no)
        except ValueError:
            flash("Room number must be a number.", "danger")
            return redirect(url_for("rooms"))

        new_room = Room(room_no=room_no, type=room_type, status="Available")
        db.session.add(new_room)
        db.session.commit()
        flash("Room added successfully!", "success")

    rooms = Room.query.all()
    return render_template("rooms.html", rooms=rooms)



# ----------------- PAYMENTS MODULE (Teammate D) -----------------
@app.route('/payments')
def payments():
    return render_template('payments.html')


# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)
