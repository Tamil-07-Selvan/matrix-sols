"""

Create a new Django project: django-admin startproject gaming_topup_project cd gaming_topup_project

Create the topup app: python manage.py startapp topup

Install Django REST Framework: pip install djangorestframework

Copy the code above into respective files

Create and run migrations: python manage.py makemigrations python manage.py migrate

Create a superuser: python manage.py createsuperuser

Populate sample data: python manage.py populate_sample_data

Run the development server: python manage.py runserver

API Endpoints:

POST /api/topup/ - Create top-up order
GET /dashboard/ - Analytics dashboard (staff only)
GET /admin/ - Django admin interface
Sample API Request: POST /api/topup/ { "gamename": "PUBG Mobile", "game_id": "pubg123", "product_name": "UC Pack 325", "product_id": 2, "product_price": 4.99, "user_email": "player@example.com", "payment_status": "pending" } """
