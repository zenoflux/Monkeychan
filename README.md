🌐 Flask Social Wall App

This is a simple social web app built with Flask — think of it like a mini message board where users can sign up, post messages (with or without images), reply to each other, and even upload profile pictures.

It’s lightweight, beginner-friendly, and easy to run locally.

🎯 What Can It Do?

Here’s what this app currently supports:

✅ User registration, login, and logout
✅ Secure password storage (hashed with Werkzeug)
✅ User profiles with email editing and profile picture upload
✅ A shared “Wall” where users can post messages or images
✅ Replies to posts (threaded messaging)
✅ Sessions that expire after 3 minutes of inactivity
✅ SQLite database powered by SQLAlchemy

🧱 Project Structure
project/
|-- app.py               # Main Flask app
|-- templates/           # HTML (Jinja2) templates
|-- static/uploads/      # Profile pictures & post images
|-- .env                 # Environment variables
|-- requirements.txt     # Python dependencies

⚙️ Getting Started
1️⃣ Clone the Project
git clone <your-repo-url>
cd <your-project-folder>

2️⃣ Optional: Set Up a Virtual Environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create a .env File

Create a file named .env in the project root and add:

SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///users.sqlite3
UPLOAD_FOLDER=static/uploads

5️⃣ Run the App
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

💡 Future Improvements

Some ideas to make this app even better:

Add CSRF protection

Add likes/reactions to posts

Improve styling with Bootstrap or Tailwind

Add pagination or infinite scroll on the wall

Add email verification or notifications

🤝 Contributing

Want to help improve the project?

Fork the repository

Create a new branch (feature-name)

Commit your changes

Submit a pull request!

📜 License

This project is open-source under the MIT License.
