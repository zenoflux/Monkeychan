Welcome to Monkeychan

I was bored one night and decided to learn some Flask and see if I could make a dumb little "chan"-like image board.

It’s lightweight, beginner-friendly, and easy to run locally.

What Can It Do?

Some basic functions include

User registration, login, and logout
Secure password storage (hashed with Werkzeug)
User profiles with email editing and profile picture upload
A shared “Wall” where users can post messages or images
Replies to posts (threaded messaging)
Sessions that expire after 3 minutes of inactivity
SQLite database powered by SQLAlchemy

Project Structure
project/
|-- app.py               # Main Flask app
|-- templates/           # HTML (Jinja2) templates
|-- static/uploads/      # Profile pictures & post images
|-- .env                 # Environment variables
|-- requirements.txt     # Python dependencies

Getting Started
Clone the Project
git clone https://github.com/zenoflux/Monkeychan
cd Monkeychan

Set Up a Virtual Environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Create a .env File

Create a file named .env in the project root and add:

SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///users.sqlite3
UPLOAD_FOLDER=static/uploads

Run the App
python app.py


Then open your browser and visit:
http://localhost:8181

🗄 Database Models
users Table
Field	Description
id	Unique user ID
name	Username (unique)
email	User email
password	Hashed password
profile_pic	Profile picture filename
Message Table
Field	Description
id	Message ID
user_id	ID of the user who posted
content	The message text
timestamp	Auto-generated post time
parent_id	ID of parent message (for replies)
image_filename	Optional image attached to the post
📸 Image Uploads

Allowed file types: png, jpg, jpeg, gif

Profile pictures save as: username_avatar.ext

Wall post images are saved with a timestamp for uniqueness


License:
This project is open-source under the MIT License.
