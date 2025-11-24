# 📚 Masterblog Full-Stack Application

This project implements a comprehensive full-stack solution for managing a blog. It consists of a robust **Python Flask API** for handling data logic and a dynamic **HTML/CSS/JavaScript** frontend for the user interface.

## ✨ Key Features

The application is fully functional and supports the following features:

* **Full CRUD:** Complete functionality to **C**reate, **R**ead, **U**pdate, and **D**elete blog posts.
* **Dynamic UI:** Posts can be edited inline and deleted dynamically without page refreshes.
* **Search:** Allows filtering posts by keywords present in the **Title** or **Content**.
* **Sort:** Supports sorting posts by **Title** or **Content** in either ascending (`asc`) or descending (`desc`) order.
* **Data Persistence:** All blog post data is saved to and loaded from a local JSON file (`posts.json`).
* **API Documentation (Swagger UI):** Interactive documentation automatically generated and available via a web interface.

---

## 🛠️ Setup and Installation

### Prerequisites

You must have Python 3.x and `pip` installed.

Install the required Python packages:
```bash
pip install Flask Flask-CORS flask_swagger_ui