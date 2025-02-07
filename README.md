# Ingredient AI

Ingredient AI is a Django-based web application that allows users to select ingredients and generate AI-powered recipes. The system leverages machine learning to create unique recipes based on user-selected ingredients and presents them in an intuitive web interface.

## Features
- **AI-Powered Recipe Generation**: Generates unique recipes based on selected ingredients.
- **Django Backend**: Uses Django as the web framework with a modular app structure.
- **Celery for Background Processing**: Asynchronous task handling with RabbitMQ as the message broker.
- **Redis Caching**: Speeds up data retrieval and performance.
- **PostgreSQL Database**: Manages recipe and user data efficiently.
- **Ollama for AI Processing**: Utilizes the **Llama3.2:1B** model to generate recipes.
- **Sentry for Error Tracking**: Monitors and captures application errors.
- **AWS S3 Buckets**: Used for storing media files securely.

## Technologies Used
- **Django** (Web Framework)
- **Celery** (Task Queue Management)
- **Redis** (Caching, via django-redis)
- **RabbitMQ** (Message Broker for Celery)
- **Ollama** (AI Model Integration)
- **PostgreSQL** (Database Management)
- **Sentry** (Error Monitoring)
- **AWS S3 Buckets** (File Storage)

## Installation

### Prerequisites
- Python 3.9+
- Django 5.0+
- PostgreSQL
- RabbitMQ
- Redis
- Ollama
- Celery

### Setup
to be filled soon...

## Usage
- Navigate to `http://127.0.0.1:8000/`
- Select ingredients and submit a request for recipe generation.
- Wait for the AI to process and display the generated recipes.

## Project Structure
```
ingredient_ai/
│── config/             # Project settings and configurations
│── ingredient_ai/      # Main app directory
│── requirements.txt    # Dependencies
│── manage.py          # Django management script
│── README.md          # Project documentation
```

## Contributing
Pull requests are welcome! Please ensure your changes align with the project structure and include proper documentation.