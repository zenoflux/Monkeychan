# Monkeychan

Welcome to Monkeychan, I got bored and decided to try to learn Flask. 
Here's my attempt at a simple "chan"-like image board.

It's lightweight, beginner-friendly, and easy to run locally.

##  Features

User registration, login, and logout

Secure password storage using Werkzeug hashing

User profiles with email editing and profile picture upload

A shared “Wall” where users can post messages and images

Threaded replies to posts

Sessions that expire after 3 minutes of inactivity

SQLite database using SQLAlchemy

## Project Structure
```
project/
|-- monkeychan.py               # Main Flask app
|-- templates/           # HTML (Jinja2) templates
|-- static/uploads/      # Profile pictures & post images
|-- .env                 # Environment variables
|-- requirements.txt     # Python dependencies
```
## Getting Started
1. Clone the Repository:
```
git clone https://github.com/zenoflux/Monkeychan
```
2. Enter the directory:
```
cd Monkeychan
```
3. Create a Virtual Environment (optional but recommended):
```
python -m venv venv
```


Activate it:

Windows:
```
venv\Scripts\activate
```

macOS/Linux:
```
source venv/bin/activate
```
4. Install Dependencies
 ```
 pip install -r requirements.txt
 ```

5. Create a .env File
Linux:
```
 touch .env
```
Windows:
```
type nul >.env
```

6. Add the following to the .env file

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///users.sqlite3
UPLOAD_FOLDER=static/uploads
```

5. Run the App
   ```python monkeychan.py```


Then visit:
http://localhost:8181




## Image Uploads
Allowed file types: png, jpg, jpeg, gif
Profile pictures are saved as: username_avatar.ext
Wall images are timestamped to prevent name conflicts


## License
This project is open-source under the MIT License.
