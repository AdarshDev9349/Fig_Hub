
# Fig Hub

**Fig Hub** is a collaborative platform that allows users to manage and showcase Figma-based projects while connecting with other creatives or developers. This Django REST API backend provides user authentication, profile management, and seamless Figma integration to fetch design previews.

---

## 🚀 Features

- 🔐 **User Signup/Login** – Secure authentication with token-based login system.
- 👤 **User Profiles** – Create and update your personal profile.
- 🎨 **Figma Project Upload** – Paste your Figma design link, and the app fetches a thumbnail image via Figma API.
- 🔍 **Search Users** – Look up other users by username or name.
- 📁 **View Profiles** – View profile info of other registered users.

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: SQLite (default, can be configured)  
- **Authentication**: Token-based (`rest_framework.authtoken`)  
- **API Integration**: Figma API  
- **Utilities**: `requests`, `dotenv`

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AdarshDev9349/Fig_Hub.git
cd Fig_Hub
```

### (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scriptsctivate
```

### 2. Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file in your project root and add your Figma API token:

```env
FIGMA_TOKEN=your_figma_api_token
```

### 4. Run the database migrations:

```bash
python manage.py migrate
```

### 5. Start the development server:

```bash
python manage.py runserver
```

---

## 🔄 API Endpoints

| Method | Endpoint                   | Description                          |
|--------|----------------------------|--------------------------------------|
| POST   | `/signup/`                 | Register a new user                 |
| POST   | `/login/`                  | Login and receive auth token        |
| POST   | `/logout/`                 | Logout and invalidate token         |
| GET    | `/profile/`                | Get logged-in user's profile        |
| POST   | `/profile/`                | Update or create user profile       |
| POST   | `/add_project/`            | Add a Figma project by URL          |
| GET    | `/search_users/?query=`    | Search users by name or username    |
| GET    | `/view_profile/<user_id>/` | View profile of a specific user     |

---

## 📌 Notes

- Ensure your Figma links are publicly accessible for image preview to work correctly.
- This is a backend-only project; you can build a frontend (e.g., React, Flutter) to interact with this API.

--- 

Feel free to reach out if you need further help with the setup or customization!
