# Event Management REST API (Django)

Test task implementation for event management using Django REST Framework.

## Implemented Features

- Event model (`title`, `description`, `date`, `location`, `organizer`)
- Event CRUD API
- User signup and JWT authentication
- Event registration / unregister
- Event attendees endpoint
- OpenAPI schema + Swagger
- Docker support
- Bonus: filtering/searching and email notification on registration

## Tech Stack

- Django
- Django REST Framework
- SimpleJWT
- drf-spectacular
- django-filter
- SQLite (default)

## Quick Start (Local)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py test
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`.

## Quick Start (Docker)

```bash
copy .env.example .env
docker compose up --build
```

## Main Endpoints

- `POST /api/auth/signup/` - create user
- `POST /api/auth/token/` - obtain JWT tokens
- `POST /api/auth/token/refresh/` - refresh access token
- `GET|POST /api/events/` - list/create events
- `GET|PATCH|PUT|DELETE /api/events/{id}/` - retrieve/update/delete event
- `POST /api/events/{id}/register/` - register for event
- `DELETE /api/events/{id}/unregister/` - cancel registration
- `GET /api/events/{id}/attendees/` - list attendees
- `GET /api/schema/` - OpenAPI schema
- `GET /api/docs/swagger/` - Swagger UI

## Filtering and Search

Supported query params on `GET /api/events/`:

- `search=<text>` for title/description/location
- `organizer=<user_id>`
- `date=<iso_datetime>`
- `ordering=date`, `ordering=-created_at`, etc.

## Email Notifications

When a user registers for an event, a confirmation email is sent.
By default, backend is console email backend (`DJANGO_EMAIL_BACKEND`), so message appears in server logs.

## Notes

- Only event organizer can update or delete an event.
- Event date must be in the future.
- Duplicate registration for the same event is blocked.
