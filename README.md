# 📚 Masterblog API and Frontend Application

This project provides a complete full-stack solution for managing a blog, featuring a robust RESTful API built with Python (Flask) and a basic, dynamic frontend interface built with HTML, CSS, and JavaScript.

The API supports full CRUD (Create, Read, Update, Delete) operations, persistent file storage, and advanced features like searching and sorting.

## 🌟 Features

### Backend (Flask API)
* **Full CRUD:** Endpoints for creating, reading, updating, and deleting blog posts.
* **File Persistence:** Data is stored persistently in a local `posts.json` file.
* **Unique ID Generation:** Automatically generates sequential, unique IDs for new posts, handling deletions gracefully.
* **Searching:** Supports searching posts by title or content via the `/api/posts/search` endpoint.
* **Sorting:** Supports sorting posts by `title` or `content` in ascending (`asc`) or descending (`desc`) order via the `/api/posts` endpoint.
* **API Documentation (Swagger UI):** Automated, interactive documentation available at `/api/docs`.

### Frontend
* A single-page application (SPA) built with vanilla HTML, CSS, and JavaScript.
* Allows users to load, add, delete, edit, and search posts without refreshing the page.

## 🛠️ Setup and Installation

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### 1. Project Structure

Ensure your project is organized with separate directories for the backend and frontend: