# Key-Value REST API

This project is a Django-based REST API that provides a secure and efficient key-value storage system. It supports both simple and nested pairs, uses JWT authentication for secure access, and offers comprehensive API documentation through Swagger and ReDoc.

---

## Features

- **User Authentication**: Secure JWT-based user authentication with RS256 encryption.
- **Key-Value Storage**: Flexible handling of key-value data, supporting various data types and nested structures.
- **Cursor Pagination**: Handles large datasets efficiently.
- **PostgreSQL Database**: Optimized querying with advanced indexing.
- **OpenAPI Documentation**: Interactive API documentation with Swagger UI and ReDoc.
- **Testing and Coverage**: Automated test coverage reports to ensure reliability and maintainability.
- **Production-ready Configuration**: Deployment ready with `Docker` and `docker-compose`.

---

## Project Structure

- **core**: Main configuration and settings files.
- **users**: Custom user model and authentication-related functionality.
- **pairs**: Key-value storage app with support for nested pairs.

---

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL
- RSA private and public keys for JWT (place in `keys/private.pem` and `keys/public.pem`)
- Create a `.env` file at the root of the project. Example content in `.env.sample` file.

---

## Setup

### Step 1: Clone the Repository

```bash
$ git clone https://github.com/amirkhgraphic/qtask-rest-api.git
$ cd qtask-rest-api
```

### Step 2: Set Up Environment Variables

Create a `.env` file at the root of the project. Example content in `.env.sample` file.

### Step 3: Install Dependencies

```bash
$ pip install -r requirements.txt
```

### Step 4: RSA Key Generation

If you don't have existing RSA keys, you can generate them using the following commands:

```bash
$ openssl genpkey -algorithm RSA -out keys/private.pem -pkeyopt rsa_keygen_bits:2048
$ openssl rsa -pubout -in keys/private.pem -out keys/public.pem
```

### Step 5: Run with Docker Compose

Build and run the project with Docker Compose:

```bash
$ docker-compose up --build
```

The application should now be available at http://localhost:8000.

---

## API Documentation

- **Swagger UI**: [http://localhost:8000/api/swagger-ui/](http://localhost:8000/api/swagger-ui/)
- **ReDoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---

## Testing

Run tests with coverage and generate reports:

```bash
$ chmod +x test_coverage.sh
$ ./test_coverage.sh
```

The coverage reports will be generated in `coverage_reports`:

- HTML report: `coverage_reports/html/index.html`
- XML report: `coverage_reports/coverage.xml`
- Text report: `coverage_reports/coverage_report.txt`

## Development/Production Settings

The app uses SQLite and a console email backend for local development and 
PostgreSQL and an SMTP email backend for production. you can switch between 
them by toggling the `PROD` environment variable.

```dotenv
PROD=True/False
```

## Additional Configuration

### Custom Pagination

The `CustomCursorPagination` class in `core.pagination` allows for cursor-based pagination, improving API response efficiency.

### JWT Configuration

JWT authentication uses `RS256` encryption. You can adjust token lifetimes in `SIMPLE_JWT` settings in `core/settings/base.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # other items
}
```

---

*[\- Amirhossein Khalili](https://github.com/amirkhgraphic)*