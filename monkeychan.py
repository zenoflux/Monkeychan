from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv


import os
load_dotenv()
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev_key_fallback")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["UPLOAD_FOLDER"] = os.environ.get("UPLOAD_FOLDER")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.permanent_session_lifetime = timedelta(minutes=3)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

db = SQLAlchemy(app)

# ---------- MODELS ----------

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), unique=True)
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(200))
    profile_pic = db.Column("profile_pic", db.String(200), default="default.png")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)  # 👈 Add this line
    replies = db.relationship('Message', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    user = db.relationship('users', backref='messages')



# ---------- HELPERS ----------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["nm"]
        password = request.form["password"]

        found_user = users.query.filter_by(name=name).first()

        if found_user and check_password_hash(found_user.password, password):
            session['user'] = name
            session['email'] = found_user.email
            flash(f"{name} successfully logged in.")
            return redirect(url_for("wall"))
        else:
            flash("Invalid username or password.")
            return render_template("login.html")

    else:
        if "user" in session:
            flash(f"User already logged in!")
            return redirect(url_for("wall"))
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["nm"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = users.query.filter_by(name=name).first()
        if existing_user:
            flash("User already exists. Please login.")
            return redirect(url_for("login"))

        new_user = users(name, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route('/logout')
def logout():
    if "user" in session:
        user = session['user']
        flash(f"{user} successfully logged out.")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user_profile():
    if "user" not in session:
        return redirect(url_for("login"))

    user = users.query.filter_by(name=session["user"]).first()
    if request.method == "POST":
        email = request.form["email"]
        session["email"] = email
        user.email = email
        db.session.commit()
        flash("Email updated.")

    return render_template("user.html", user=user)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("Please log in to access your profile.")
        return redirect(url_for("login"))

    user = users.query.filter_by(name=session["user"]).first()

    if request.method == "POST":
        if "profile_pic" not in request.files:
            flash("No file part.")
            return redirect(request.url)

        file = request.files["profile_pic"]

        if file.filename == "":
            flash("No selected file.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = f"{user.name}_avatar.{file.filename.rsplit('.', 1)[1].lower()}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            user.profile_pic = filename
            db.session.commit()
            flash("Profile picture updated!")
            return redirect(url_for("profile"))

    return render_template("profile.html", user=user)


@app.route("/wall", methods=["GET", "POST"])
def wall():
    if "user" not in session:
        flash("You must be logged in to view the wall.")
        return redirect(url_for("login"))

    current_user = users.query.filter_by(name=session["user"]).first()

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        parent_id = request.form.get("parent_id")
        image = request.files.get("image")

        image_filename = None
        if image and allowed_file(image.filename):
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image.filename}"
            filename = filename.replace(" ", "_")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)
            image_filename = filename

        if not content and not image_filename:
            flash("Cannot post an empty message.")
            return redirect(url_for("wall"))

        new_message = Message(
            user_id=current_user._id,
            content=content,
            parent_id=int(parent_id) if parent_id else None,
            image_filename=image_filename
        )
        db.session.add(new_message)
        db.session.commit()
        flash("Message posted!")

        return redirect(url_for("wall"))

    # Fetch top-level posts
    top_posts = Message.query.filter_by(parent_id=None).order_by(Message.timestamp.desc()).all()

    # Recursive reply fetching
    def fetch_replies(post):
        post.replies_list = post.replies.order_by(Message.timestamp.asc()).all()
        for reply in post.replies_list:
            fetch_replies(reply)

    for post in top_posts:
        fetch_replies(post)

    return render_template("wall.html", posts=top_posts)


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Make sure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host="0.0.0.0", port = '8181',debug=True)