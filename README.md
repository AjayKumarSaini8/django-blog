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

User Guide
1. Registration and Authentication
Register: Click "Register" in the navigation bar to create an account

Login: Click "Login" and enter your credentials

Logout: Click "Logout" in the navigation menu

2. Creating and Managing Blog Posts
Create a Post (authenticated users only):

Click "New Post" in the navigation bar

Fill in the title and content using the rich text editor

Click "Publish"

Edit a Post (author only):

Navigate to your post

Click the "Edit" button

Make your changes and click "Update"

Delete a Post (author only):

Navigate to your post

Click the "Delete" button

Confirm deletion

3. Browsing Content
Home Page: Shows all published posts in chronological order

Search: Use the search bar to find posts by title or content
