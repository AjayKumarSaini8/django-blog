# Django Blog Project

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A full-featured blog application built with Django.

## Features
- User authentication (Login/Register)
- Create, edit, delete blog posts
- Post categories and tags
- Comments system
- Responsive design

## Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/django-blog.git
cd django-blog

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
