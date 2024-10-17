# Inventory Management System API
## Overview
This project implements a simple Inventory Management System API using Django Rest Framework (DRF). The API allows users to perform CRUD (Create, Read, Update, Delete) operations on inventory items and is secured using JWT-based authentication. Additionally, Redis is used for caching frequently accessed items to improve performance.

### Features
CRUD operations for managing inventory items.
JWT authentication for securing access to the API.
PostgreSQL as the primary database for storing inventory data.
Redis caching for optimizing read operations.
Logging for debugging and monitoring API usage and errors.
Unit tests to verify the functionality of the API.

### Technologies Used
- Python
- Django
- Django Rest Framework (DRF)
- PostgreSQL
- Redis
- JWT for authentication
- Logging for API monitoring and debugging

### Installation and Setup
- asgiref==3.8.1
- async-timeout==4.0.3
- Django==5.1.2
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- psycopg2-binary==2.9.10
- PyJWT==2.9.0
- python-dotenv==1.0.1 a
- redis==5.1.1
- sqlparse==0.5.1 a
- typing_extensions==4.12.2

### Steps
Clone the repository:
```
git clone https://github.com/yourusername/inventory-management-api.git
```
```
cd inventory-management-api
```
### Set up a virtual environment:

```
python -m venv venv
source venv/bin/activate
```
- Install dependencies:

```
pip install -r requirements.txt
```

### Configure environment variables:
- Create a .env file in the root directory to store your environment variables:


### Set up the database:

- Create the PostgreSQL database:

```
CREATE DATABASE inventory_db;
```

### Run migrations:

- python manage.py migrate

#### Run the Redis server
```
redis-server
```

### Run the Django development server:

```
python manage.py runserver
```

### API Endpoints
#### Authentication
- User Registration:

```URL: /api/auth/register/```
- Method: POST

- Request Body:

```{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```
- Response:

```
{
  "id": "uuid",
  "username": "your_username",
  "email": "your_email@example.com"
}
```
- Login and Token Retrieval:

```URL: /api/auth/login/```
- Method: POST
- Request Body:

```{
  "username": "your_username",
  "password": "your_password"
}
```
- Response:

```{
  "access": "JWT_access_token",
  "refresh": "JWT_refresh_token"
}
```

### Item Management (Requires JWT Token)
- Create Item:

```
URL: /api/items/
```
- Method: POST
- Request Body:

```
{
  "name": "item_name",
  "description": "item_description",
  "price": 100.00,
  "quantity": 10
}
```

- Response:

```
{
  "id": "uuid",
  "name": "item_name",
  "description": "item_description",
  "price": 100.00,
  "quantity": 10,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

- Read Item:

```
URL: /api/items/{item_id}/
```
- Method: GET
- Response:

```
{
  "id": "uuid",
  "name": "item_name",
  "description": "item_description",
  "price": 100.00,
  "quantity": 10,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

- Update Item:

```URL: /api/items/{item_id}/```
- Method: PUT
- Request Body:

```{
  "name": "updated_item_name",
  "description": "updated_description",
  "price": 150.00,
  "quantity": 15
}
```
- Response:

```{
  "id": "uuid",
  "name": "updated_item_name",
  "description": "updated_description",
  "price": 150.00,
  "quantity": 15,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

- Delete Item:

```
URL: /api/items/{item_id}/
```
- Method: DELETE
- Response:

```{
  "message": "Item deleted successfully."
}
```
### Testing the API
To run the unit tests for the project, use the following command:
```
python manage.py test
```

This will run all unit tests for the API, ensuring the endpoints work as expected.

### Logging
All logs for the API are saved in the debug.log file. You can find this file in the root directory of the project.

#### Caching with Redis
Redis is used to cache read operations on items to improve performance.
When an item is accessed, it will be cached for 15 minutes, after which it will be fetched from the database again.