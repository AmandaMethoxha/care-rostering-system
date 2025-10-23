# 🩺 Care Rostering System

> A lightweight rostering and scheduling platform for care providers — built with **FastAPI**, **Streamlit**, and **PostgreSQL (Dockerized)**.

---

## 🚀 Overview

The **Care Rostering System** is an end-to-end scheduling platform designed for adult social care services.
It allows managers to:

* Maintain staff and service user records
* Manage staff availability
* Assign staff to service users based on their needs
* Streamline rostering operations with real-time updates

Developed entirely by **Amanda Methoxha**, this project showcases full-stack development skills using modern Python frameworks and containerized deployment.

---

## 🧩 Tech Stack

| Component              | Technology Used                                                  |
| ---------------------- | ---------------------------------------------------------------- |
| **Frontend**           | [Streamlit](https://streamlit.io/) — dashboard & user interface  |
| **Backend API**        | [FastAPI](https://fastapi.tiangolo.com/) — RESTful API framework |
| **Database**           | PostgreSQL (Docker container)                                    |
| **Containerization**   | Docker & Docker Compose                                          |
| **DB Driver**          | psycopg2                                                         |
| **Data Visualisation** | Pandas + Streamlit built-in charts                               |

---

## 🧠 Features

***✅** Manage **staff profiles** (create, update, delete)
***✅**  Manage **service user records** with RAG ratings
***✅**  Record **staff availability** by weekday and shift times
*✅ Create and view **assignments** between staff and service users
*✅ Log **service user care needs** (e.g. medical, wellbeing, domestic)
*✅ REST API accessible via FastAPI Swagger UI
*✅ Full environment in Docker — one command setup

---

## ⚙️ Local Setup (via Docker)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/care-rostering-system.git
cd care-rostering-system
```

### 2️⃣ Start the full stack

```bash
docker-compose up --build
```

This launches:

* PostgreSQL database (`care_roster_db`)
* FastAPI backend (`care_roster_backend`)
* pgAdmin interface (`care_roster_pgadmin`)

Access URLs:

* **API** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **pgAdmin** → [http://127.0.0.1:5050](http://127.0.0.1:5050)
  Email: `admin@example.com`
  Password: `admin`

---

## 🖥️ Frontend (Streamlit)

Once backend is running, open a new terminal and start the dashboard:

```bash
streamlit run dashboard.py
```

Then visit:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🧱 Database Schema

| Table                      | Description                                      |
| -------------------------- | ------------------------------------------------ |
| `staff_details`            | Staff records                                    |
| `service_user_details`     | Service user profiles                            |
| `staff_availability`       | Weekly shift preferences                         |
| `service_user_assignments` | Assignment history                               |
| `service_user_needs`       | Specific care tasks (e.g. nurse visit, check-in) |

---

## 🧰 Example API Endpoints

| Method | Endpoint              | Description                         |
| ------ | --------------------- | ----------------------------------- |
| `GET`  | `/staff`              | Fetch all staff                     |
| `POST` | `/staff`              | Add new staff member                |
| `GET`  | `/service-users`      | Fetch all service users             |
| `POST` | `/service-user-needs` | Log a service user's need           |
| `GET`  | `/assignments`        | View staff-service user assignments |

Use the FastAPI Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🗂️ Project Structure

```
care-rostering-system/
│
├── backend/
│   ├── app.py                # FastAPI backend
│   ├── schema.sql            # Database schema
│   └── requirements.txt
│
├── dashboard.py              # Streamlit dashboard
├── docker-compose.yml        # Multi-container setup
├── Dockerfile                # Backend image
├── db-data/                  # Postgres volume (ignored by .gitignore)
└── README.md
```

---

## 🌍 Deployment

Easily deployable on any Docker-capable platform:

* AWS ECS / Fargate
* Azure App Services
* Railway.app
* Render.com
* Local or on-prem VM

---

## 👤 Author

**Amanda Methoxha Shpendi**
📍 Grays, Essex, UK
💻 Embedded & Software Engineer 
📧 [amandashpendi@gmail.com](mailto:amandashpendi@gmail.com) 
🔗 [LinkedIn Profile](https://www.linkedin.com/in/amanda-shpendi-463531160/)

---

## 🏁 Future Improvements

* 🧠 AI-assisted rostering (Power BI + ML integration)
* 🗓️ Interactive calendar view for assignments
* 📱 Mobile-friendly Streamlit layout
* 🔐 Role-based authentication system

---

**Developed by Amanda Methoxha — 2025** ✨
