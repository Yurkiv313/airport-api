# 🛫 Airport Management API
A **RESTful API** for efficient management of airport operations,
including countries, cities, airports, routes, flights, crew members,
and ticket orders. This project is built with Django and 
Django REST Framework (DRF) for robust performance, PostgreSQL for 
data storage, and Docker for seamless deployment.

---

## 📌 **Key Features**

### 🌍 **Geographic Management**

* **Countries**: Manage country names and codes.
* **Cities**: Create and link cities to specific countries.
* **Airports**: Add airports, link them to cities, and manage locations.

---

### 🛫 **Flight Operations**

* **Routes**: Define flight paths between airports.
* **Airplane Types**: Manage airplane types with seat configurations.
* **Airplanes**: Add airplanes, set capacity, and upload images.
* **Flights**: Schedule flights with routes, airplanes, and crew assignments.

---

### 👥 **Crew Management**

* **Crew Members**: Register pilots, stewardesses, and other staff.
* **Smart Search**: Find crew members by full name.

---

### 🎫 **Ticketing and Orders**

* **Orders**: Manage passenger orders with multiple tickets.
* **Tickets**: Validate seat availability and prevent double booking.

---

### 🔒 **Secure Access**

* **JWT Authentication**: Token-based secure access.
* **Role-Based Permissions**: Fine-grained control for admins and regular users.

---

### 🗂️ **Optimized Data Handling**

* **Custom Serializers**: Separate serializers for lists, details, and images.
* **Filtering and Search**: Powerful filtering across all entities.

---

## 🛠 **Tech Stack**

| Layer              | Technology               |
| ------------------ | ------------------------ |
| **Backend**        | Django + Django REST Framework |
| **Database**       | PostgreSQL               |
| **Authentication** | JWT (Access/Refresh tokens) |
| **Deployment**     | Docker + Docker Compose  |
| **Documentation**  | drf-spectacular (Swagger, Redoc) |


---

## 🚀 **Local Setup**

### 📥 **Step 1: Clone the Repository**

Clone the project from GitHub:

```bash
git clone https://github.com/Yurkiv313/airport-api.git
cd airport-api
```

---

### 📝 **Step 2: Configure Environment**

Create and update the `.env` file with your credentials:

```
POSTGRES_PASSWORD=your_postgres_password  
POSTGRES_USER=your_postgres_user  
POSTGRES_DB=your_postgres_db  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  
SECRET_KEY=your_secret_key   
```

---

### 🐳 **Step 3: Start the Containers**

Build and start the containers:

```bash
docker-compose up --build -d
```

---

### 📊 **Step 4: Populate the Database**

Run the custom management command to fill the database with sample data:

```bash
docker-compose exec web python manage.py populate_db
```

This command will create a basic data set, including countries, cities, airports, routes, airplane types, airplanes, crew members, and other related entities.

---

### 🔄 **Step 5: Check API Status**

* Visit the API at: [http://localhost:8000/](http://localhost:8000/)
* Check Swagger docs at: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)

---

### 🛑 **Step 6: Stop and Clean Up**

When you're done, stop the containers:

```bash
docker-compose down
```

---

## 🐳 **Run from Docker Hub**

### 📥 **Step 1: Pull the Image**

Get the latest version of the image from Docker Hub:

```bash
docker pull yurkivandriy/airport-api:latest
```

---

### 📝 **Step 2: Configure Environment**

Create a `.env` file for your database and Django settings:

```
POSTGRES_PASSWORD=your_postgres_password  
POSTGRES_USER=your_postgres_user  
POSTGRES_DB=your_postgres_db  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  
SECRET_KEY=your_secret_key  
```

---

### 🚀 **Step 3: Start the Containers**

Run the container with the environment file:

```bash
docker run -d -p 8000:8000 --env-file .env --name airport-api yurkivandriy/airport-api:latest
```

---

### 📊 **Step 4: Populate the Database**

If you haven't done this before, populate the database:

```bash
docker exec -it airport-api python manage.py populate_db
```

---

### 🔄 **Step 5: Check API Status**

* Visit the API at: [http://localhost:8000/](http://localhost:8000/)
* Check Swagger docs at: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)

---

### 🛑 **Step 6: Stop and Remove the Container**

When you're done, you can stop and remove the container:

```bash
docker stop airport-api  
docker rm airport-api
```

---

## 💡 **Why Choose Airport Management API?**

* **Built for Real-World Use:** Handles the full lifecycle of flights, from airport setup to ticket sales.
* **Flexible and Scalable:** Easily adapts to new requirements as your project grows.
* **Developer-Friendly:** Clean, modular code with reusable serializers and clear API structure.
* **Fast Setup:** Dockerized for instant local deployment and quick scaling.
* **Powerful Data Management:** Supports complex relationships like routes, flights, and crews.
* **Easy API Exploration:** Swagger and Redoc for rapid testing and integration.

---

<img width="650" alt="airport" src="https://github.com/user-attachments/assets/7e081d28-c51b-4097-8e09-c6e8ef19babd" />





