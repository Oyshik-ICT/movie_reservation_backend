# 🎬 Movie Reservation System

A comprehensive movie ticket booking backend system built with Django REST Framework. This system allows users to browse movies, book tickets, and make payments through SSLCommerz gateway.

##  Features

###  For Regular Users
- **User Authentication**: Register, login, and manage profile with JWT authentication
- **Password Reset**: Secure OWASP-compliant password reset with email verification
- **Browse Movies**: View available movies with details (genre, language, actors)
- **Book Tickets**: Select seats and book tickets for movie showings
- **Online Payment**: Pay securely through SSLCommerz payment gateway
- **Booking History**: View all your past and current bookings
- **Email Notifications**: Receive booking confirmations via email

###  For Admin Users
- **Movie Management**: Add, update, and delete movies
- **Theater Management**: Manage theaters and auditoriums
- **Seat Management**: Bulk create and manage seats
- **Show Scheduling**: Schedule movie showings with date, time, and pricing
- **Actor Management**: Add and manage actor information
- **Payment Monitoring**: View all payment transactions
- **Booking Oversight**: Monitor all bookings across the system

###  Security Features
- JWT token-based authentication
- OWASP-compliant password reset flow
- Rate limiting on password reset attempts
- Timing attack prevention
- Secure payment processing

###  Performance Optimizations
- Database query optimization with `select_related()` and `prefetch_related()`
- Redis caching for session management
- Async email sending with Celery
- Database locking for concurrent booking prevention
- Efficient bulk operations

##  Tech Stack

- **Framework**: Django 5.2.4
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (Docker) / SQLite (Local dev)
- **Caching**: Redis
- **Task Queue**: Celery 5.6.2
- **Payment Gateway**: SSLCommerz
- **Email**: SMTP
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)

## 📋 Prerequisites

**For Local Development:**
- Python 3.10 or higher
- Redis Server
- pip (Python package manager)

**For Docker (Recommended):**
- Docker Desktop
- Docker Compose

##  Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Oyshik-ICT/movie_reservation_backend.git

cd movie_reservation_backend
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the `movie_reservation` directory (same level as `settings.py`):
```env
# ============================================
# Email Configuration
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@moviereservation.com

# ============================================
# Database (Docker uses PostgreSQL)
# ============================================
POSTGRES_DB=movie_reservation
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_123

# Database URL (automatically used in Docker)
DATABASE_URL=postgresql://postgres:your_secure_password_123@db:5432/movie_reservation

# ============================================
# Redis & Celery
# ============================================
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=django-db

# ============================================
# SSLCommerz Payment Gateway
# ============================================
SSLCOMMERZ_ID=your-store-id
SSLCOMMERZ_PASS=your-store-password
SSLCOMMERZ_IS_SANDBOX=True


# ============================================
# Backend URL (for payment callbacks)
# ============================================
BACKEND_URL=http://localhost:8000
# For testing real payments, use ngrok: https://your-id.ngrok-free.app
```

**Note**: 
- For Gmail, use [App Passwords](https://support.google.com/accounts/answer/185833)
- Get SSLCommerz credentials from [SSLCommerz](https://sslcommerz.com/)

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### 6. Start Redis Server

```bash
# On Windows (with Redis installed):
redis-server

# On Mac (with Homebrew):
brew services start redis

# On Linux:
sudo service redis-server start
```

### 7. Start Celery Worker (New Terminal)

Open a new terminal, activate the virtual environment, and run:

```bash
# On Windows:
celery -A movie_reservation worker -l info --pool=solo

# On Mac/Linux:
celery -A movie_reservation worker --loglevel=info
```

### 8. Start Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

## 🐳 Running with Docker (Recommended)

Docker simplifies setup by bundling all dependencies (PostgreSQL, Redis, Celery) into containers.

### Quick Start
```bash
# 1. Clone repository
git clone https://github.com/Oyshik-ICT/movie_reservation_backend.git
cd movie_reservation_backend

# 2. Create a `.env` file in the `movie_reservation` directory (same level as `settings.py`) and configure it like before as local host

# 3. Build and start all services
docker-compose up --build

# 4. In a new terminal, run migrations
docker-compose exec web python manage.py migrate

# 5. Create admin user
docker-compose exec web python manage.py createsuperuser

# 6. Access application
# API Docs: http://localhost:8000/api/docs/
# Admin: http://localhost:8000/admin/
```

### Docker Commands Reference
```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f web          # Django logs
docker-compose logs -f celery       # Celery logs

# Stop services
docker-compose down

# Restart after code changes
docker-compose restart web

# Run Django commands
docker-compose exec web python manage.py <command>

# Access database
docker-compose exec db psql -U postgres -d movie_reservation

# Clean restart (removes volumes)
docker-compose down -v
docker-compose up --build
```

### Docker Architecture

The application runs in 4 containers:
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache & Celery broker (port 6379)  
- **web**: Django API server (port 8000)
- **celery**: Background task worker

---

##  API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/
- **Admin Panel**: http://localhost:8000/admin/
- **Silk Profiler**: http://localhost:8000/silk/ (for performance monitoring)

##  API Endpoints

### Authentication (`/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/users/` | Register new user | No |
| POST | `/auth/api/token/` | Login (get JWT tokens) | No |
| POST | `/auth/api/token/refresh/` | Refresh access token | No |
| GET | `/auth/users/` | Get current user profile | Yes |
| PUT/PATCH | `/auth/users/{id}/` | Update user profile | Yes |
| POST | `/auth/forgot-password/` | Request password reset | No |
| POST | `/auth/verify-pin/` | Verify reset PIN | No |
| POST | `/auth/reset-password/` | Reset password | No |

### Movies (`/movie/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/movie/user-movies/` | List all movies | No |
| GET | `/movie/admin-movies/` | List movies (admin) | Admin |
| POST | `/movie/admin-movies/` | Create new movie | Admin |
| GET | `/movie/admin-movies/{id}/` | Get movie details | Admin |
| PUT/PATCH | `/movie/admin-movies/{id}/` | Update movie | Admin |
| DELETE | `/movie/admin-movies/{id}/` | Delete movie | Admin |

### Theaters (`/theater/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/theater/theater-info/` | List all theaters | No |
| POST | `/theater/theater-info/` | Create theater | Admin |
| PUT/PATCH | `/theater/theater-info/{id}/` | Update theater | Admin |
| DELETE | `/theater/theater-info/{id}/` | Delete theater | Admin |

### Auditoriums (`/auditorium/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/auditorium/auditorium-info/` | List auditoriums | No |
| POST | `/auditorium/auditorium-info/` | Create auditorium | Admin |
| PUT/PATCH | `/auditorium/auditorium-info/{id}/` | Update auditorium | Admin |
| DELETE | `/auditorium/auditorium-info/{id}/` | Delete auditorium | Admin |

### Seats (`/seat/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/seat/` | List all seats | No |
| POST | `/seat/bulk_create/` | Bulk create seats | Admin |
| GET | `/seat/by_auditorium/?auditorium_id={id}` | Get seats by auditorium | No |
| PUT/PATCH | `/seat/{id}/` | Update seat | Admin |
| DELETE | `/seat/{id}/` | Deactivate seat | Admin |

### Movie Showings (`/movie-showing/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/movie-showing/` | List all showings | No |
| POST | `/movie-showing/` | Create showing | Admin |
| GET | `/movie-showing/{id}/` | Get showing details | No |
| PUT/PATCH | `/movie-showing/{id}/` | Update showing | Admin |
| DELETE | `/movie-showing/{id}/` | Delete showing | Admin |

### Bookings (`/booking/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/booking/` | List user's bookings | Yes |
| POST | `/booking/` | Create new booking | Yes |
| GET | `/booking/{id}/` | Get booking details | Yes |
| PUT/PATCH | `/booking/{id}/` | Update booking | Admin |
| DELETE | `/booking/{id}/` | Delete booking | Admin |

### Payments (`/pay/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/pay/` | Initiate payment | Yes |
| GET | `/pay/lists/` | List all payments | Admin |
| POST | `/pay/{payment_id}/ipn/` | Payment webhook (SSLCommerz) | No |
| POST | `/pay/{payment_id}/success/` | Payment success callback | No |
| POST | `/pay/{payment_id}/failed/` | Payment failed callback | No |
| POST | `/pay/{payment_id}/cancel/` | Payment cancel callback | No |

### Actors (`/actor/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/actor/information/` | List all actors | Admin |
| POST | `/actor/information/` | Create actor | Admin |
| PUT/PATCH | `/actor/information/{id}/` | Update actor | Admin |
| DELETE | `/actor/information/{id}/` | Delete actor | Admin |

##  Usage Examples

### 1. Register a New User
```bash
POST /auth/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePass@123",
    "phone_number": "+8801712345678"
}
```

### 2. Login
```bash
POST /auth/api/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePass@123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Book Tickets
```bash
POST /booking/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "movie_showing": 1,
    "seat": [1, 2, 3]
}
```

### 4. Make Payment
```bash
POST /pay/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "gateway_type": "SSLCOMMERZ",
    "booking": "550e8400-e29b-41d4-a716-446655440000"
}

Response:
{
    "success": true,
    "payment_id": "c91f34fa-2d47-4e7c-8f45-123456789abc",
    "payment_url": "https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=..."
}
```

### 5. Bulk Create Seats
```bash
POST /seat/bulk_create/
Authorization: Bearer <admin_access_token>
Content-Type: application/json

{
    "auditorium_id": 1,
    "rows": ["A", "B", "C"],
    "seat_per_row": 10,
    "seat_type": "regular"
}
```


##  Admin Access

To create an admin user:

```bash
python manage.py createsuperuser
```

Then login at: http://localhost:8000/admin/

##  Key Features Explained

### Booking Flow
1. User selects movie showing and seats
2. System validates seats are available and not booked
3. Creates booking with PENDING status
4. User initiates payment
5. Redirected to SSLCommerz payment page
6. After successful payment, booking status changes to CONFIRMED
7. Email confirmation sent via Celery

### Payment Flow
1. User creates booking
2. Payment record created with UNPAID status
3. User redirected to payment gateway
4. Gateway processes payment
5. IPN (Instant Payment Notification) received
6. Payment verified and booking confirmed
7. Email notification sent

### Security Measures
- JWT token expiration
- Password complexity validation
- Phone number verification
- Rate limiting on password reset
- Timing attack prevention
- Database row locking for concurrent bookings


##  Troubleshooting

### Redis Connection Error
- Ensure Redis server is running: `redis-cli ping` should return `PONG`
- Check Redis port: default is 6379

### Celery Not Processing Tasks
- Ensure Celery worker is running
- Check Celery logs for errors
- Verify Redis connection

### Email Not Sending
- Check email credentials in `.env`
- For Gmail, enable "Less secure app access" or use App Password
- Check spam folder

### Payment Gateway Errors
- Verify SSLCommerz credentials
- Ensure `BACKEND_URL` is accessible (use ngrok for local testing)
- Check sandbox mode is enabled for testing

##  Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_BACKEND` | Email backend class | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS | `True` |
| `EMAIL_HOST_USER` | Email username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password | `your-app-password` |
| `DEFAULT_FROM_EMAIL` | From email address | `noreply@example.com` |
| `SSLCOMMERZ_ID` | Store ID | `test123` |
| `SSLCOMMERZ_PASS` | Store password | `testpass` |
| `SSLCOMMERZ_IS_SANDBOX` | Sandbox mode | `True` |
| `BACKEND_URL` | Backend URL (for payment callbacks) | `http://localhost:8000` (use ngrok for testing payments) |


##  Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Happy Coding! 🎬**