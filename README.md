
# 🚑 NahooCare_API — AI-Powered Symptom-Based Healthcare Recommendation System

> A robust, production-ready **Python + FastAPI** backend for matching symptoms to healthcare centers and delivering first-aid support, seamlessly integrated with a Flutter-based mobile app.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-blazing%20fast-green?logo=fastapi)]()
[![Live API](https://img.shields.io/badge/Live-Render-green?logo=render)](https://nahoocare-api-2.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 🔗 Mobile App Integration

🖥️ This backend powers the Flutter-based mobile frontend:  
👉 **[NahooCare-Mobile-App](https://github.com/Ashenafidejene/NahooCare-Mobile-App)**

### 📱 Frontend Highlights:

- 🌍 **Interactive Maps** – Locate nearby hospitals/clinics using geolocation
- 💾 **Offline Storage** – Access your last queries and results without internet
- 🔐 **Authentication** – Secure login/signup system
- 🧼 **Clean Architecture** – Separation of concerns using MVC and services
- 🌐 **Amharic Language Support** – Built with native experience for Ethiopian users

> Together with this FastAPI backend, the mobile app provides a complete smart health assistant!

---

## 🚀 Why FastAPI?

This project uses **FastAPI**, a modern, async-first web framework for building lightning-fast APIs with Python 3.7+:

- 🔥 **Fast**: Built on Starlette and Pydantic. Extremely high performance.
- 🧩 **Automatic Docs**: Swagger UI and ReDoc enabled out of the box.
- ⛑️ **Type-Safe**: Full typing support, great for IDEs and code clarity.
- ⚙️ **Asynchronous Support**: Non-blocking endpoints using `async` and `await`.

---

## ✨ Core Features

- 🤖 **AI-Enhanced Symptom Matching** – Rule-based NLP logic suggests clinics based on health complaints
- 📍 **Geolocation-Based Filtering** – Uses user location to recommend nearby healthcare centers
- 🩹 **First-Aid Instructions** – Provides basic care steps immediately based on reported symptoms
- 🏥 **Healthcare Center Management** – CRUD operations for clinics and hospitals
- 🌐 **Deployed & Public** – [Explore Live ➜](https://nahoocare-api-2.onrender.com)
- 🧪 **Easy Testing** – Swagger UI and test coverage with `pytest`

---

## 🌐 Live API

Try it now:  
👉 **[https://nahoocare-api-2.onrender.com](https://nahoocare-api-2.onrender.com)**  
Browse `/docs` or `/redoc` for full interactive API reference.

---

## 🏗️ Tech Stack Overview

| Layer        | Technology                  |
|--------------|-----------------------------|
| Language     | **Python 3.10+**            |
| Framework    | **FastAPI** (async API)     |
| Data Model   | Pydantic, SQLite            |
| Geolocation  | Geopy, Haversine Formula    |
| AI Engine    | Rule-based matching logic   |
| Deployment   | Render.com                  |
| Container    | Docker (ready for prod)     |

---

## 📦 Setup & Installation

### 🔧 Requirements

- Python 3.10+
- pip or poetry
- (Optional) Docker

### ⚙️ Setup

```bash
git clone https://github.com/Ashenafidejene/NahooCare_API.git
cd NahooCare_API

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
````

### 🌍 Environment (.env)

```env
DATABASE_URL=sqlite:///./nahoocare.db
GEOCODER_API_KEY=your_api_key_here
```

### ▶️ Run Locally

```bash
uvicorn main:app --reload
```

Access docs:
🔗 `http://localhost:8000/docs` (Swagger)
🔗 `http://localhost:8000/redoc` (ReDoc)

---

## 📚 Main API Endpoints

| Method | Path              | Description                               |
| ------ | ----------------- | ----------------------------------------- |
| POST   | `/predict`        | Get AI-powered clinic matches & first aid |
| GET    | `/health-centers` | List all clinics                          |
| POST   | `/health-centers` | Add new clinic info (admin access)        |

---

## 🔄 Example: Predict Endpoint

```json
POST /predict
{
  "symptoms": ["chest pain", "shortness of breath"],
  "latitude": 8.98,
  "longitude": 38.76,
  "radius_km": 10
}
```

**Sample Response:**

```json
{
  "centers": [
    {
      "name": "Bole Heart Clinic",
      "distance_km": 3.5,
      "first_aid": [
        "Sit down and relax",
        "Take slow deep breaths",
        "Call emergency if pain persists"
      ]
    }
  ]
}
```

---

## 🧠 AI & Symptom Matching Logic

The current AI engine uses domain-knowledge rules to:

* Map symptoms to condition categories
* Match conditions to clinic specialties
* Provide real-time first aid response
* (Future: Add ML-based diagnosis from larger datasets)

---

## 🐳 Docker Deployment

```bash
docker build -t nahoocare_api .
docker run -p 8000:80 --env-file .env nahoocare_api
```

---

## 🧪 Testing

```bash
pytest --cov
```

---

## 📈 Roadmap

* [x] AI Rule-Based Symptom Engine
* [x] RESTful API with auto-docs
* [x] Flutter mobile app integration
* [x] Amharic language support
* [ ] ML-based condition classifier
* [ ] PostgreSQL + Redis backend (scalability)
* [ ] JWT authentication for frontend sync

---

## 👨‍💻 Author

**Ashenafi Dejene Negash**
📍 Addis Ababa, Ethiopia
📧 [sangutashe19@gmail.com](mailto:sangutashe19@gmail.com)
🔗 [Frontend Repo (Flutter)](https://github.com/Ashenafidejene/NahooCare-Mobile-App)

---

## 📄 License

Licensed under the [MIT License](LICENSE).

> Empowering smart healthcare decisions through AI + geolocation, made for Ethiopia 🇪🇹 and beyond.

