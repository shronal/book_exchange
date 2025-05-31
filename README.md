# 📚 Book Exchange

## 🔍 Overview

**Book Exchange** is a web-based platform designed to facilitate the exchange of books among users. Built using the Django framework, it allows users to list books they wish to give away or exchange, browse available books, and manage exchange requests seamlessly.

---

## 💼 Tech Stack

- **Backend:** Django (Python)  
- **Database:** SQLite (default) or PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript  

---

## 🎯 Features

- 📖 List books available for exchange  
- 🔍 Search and browse books by title, author, or genre  
- 🤝 Send and manage exchange requests  
- 🔐 User authentication and profile management  
- 📬 Notifications for exchange activities  

---

## 📂 Project Structure

```
book_exchange/
├── bookEx/                 # Core application logic  
├── bookMng/                # Book management module  
├── venv/                   # Python virtual environment  
├── db.sqlite3              # SQLite database file  
├── manage.py               # Django management script  
├── requirements.txt        # Python dependencies  
└── README.md               # Project documentation  
```

---

## ⚙️ Setup Instructions

### 🛠️ Step 1: Clone the Repository

```bash
git clone https://github.com/shronal/book_exchange.git
cd book_exchange
```

---

### 🛠️ Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 🛠️ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🛠️ Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 🛠️ Step 5: Run the Development Server

```bash
python manage.py runserver
```

Now visit:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👨‍💻 Author

- **Name:** Shronal Shrestha  
- **Institution:** Khwopa Engineering College  
- **Portfolio:** [shronal.com.np](https://shronal.com.np)  

---

## 📜 License

This project is intended for educational purposes.  
Feel free to use, modify, and distribute with proper attribution.
