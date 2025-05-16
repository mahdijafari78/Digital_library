# 📚 Digital Library (Django Project)

This project is a Digital Library system built using Django framework. It allows users to browse, search, and manage digital books efficiently through a web interface.

## 📁 Project Structure

```
Digital_library/
├── Digital_library/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── library_app/ # Your main Django app
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ └── urls.py
├── manage.py
├── db.sqlite3 # Database file (if using SQLite)
├── requirements.txt
└── README.md
```


## ⚙️ Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/mahdijafari78/Digital_library.git
cd Digital_library
```
```
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```

Access the app at http://127.0.0.1:8000/

##🧰 Features
- User registration and authentication

- Browse and search digital books by categories

- Admin panel to add, edit, delete books

- Responsive design using Bootstrap

- User-friendly interface

##🛠️ Technologies Used
- Python 3.x

- Django

- SQLite (default database)

- HTML/CSS/JavaScript (Bootstrap)

---

Made with by [@mahdijafari78](https://github.com/mahdijafari78)
