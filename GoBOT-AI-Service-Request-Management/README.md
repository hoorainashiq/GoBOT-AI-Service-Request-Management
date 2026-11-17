# GoBOT AI Service Request Management

A Django web application for submitting, triaging and tracking service requests.
**GoBOT** automatically suggests a category, priority and short summary for every new
request, notifies support staff, and keeps customers updated as work progresses.

## Features
- Role-based accounts: **Customer**, **Support Agent**, **Administrator**
- Submit requests; customers see only their own, agents see all
- AI triage (`requests_app/ai.py`) — keyword-based, dependency-free, easy to swap for an LLM
- Conversation thread on each request
- Agents update status, priority, category and assignee
- In-app notifications with unread counter
- Django admin for user/role management
- PlantUML diagrams in `diagrams/`

## Project structure
```
GoBOT-AI-Service-Request-Management/
├── manage.py
├── requirements.txt
├── config/            # settings, urls, wsgi/asgi
├── accounts/          # custom User model, login, signup
├── requests_app/      # ServiceRequest, Comment, AI triage, views
├── notifications/     # Notification model, services, views
├── templates/
├── static/
├── diagrams/          # use case, class, sequence, activity, component, deployment (.puml)
└── tests/
```

## Getting started
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations accounts requests_app notifications
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/. To create an agent, log into `/admin/` and set a user's
**Role** to *Support Agent*. (Public sign-up always creates customers.)

## Running tests
```bash
python manage.py test tests
```

## Configuration
Environment variables (see `.env.example`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`,
`DJANGO_ALLOWED_HOSTS`. Always set a real secret key and `DJANGO_DEBUG=False` in production.

## Production
```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi
```

## License
MIT (add a LICENSE file if you want one).
