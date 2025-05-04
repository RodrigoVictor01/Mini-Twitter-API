# Mini Twitter API

## Project with Python, Django, Redis, and PostgreSQL

## Requirements

Before getting started, make sure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download/)
- [pip](https://pip.pypa.io/en/stable/)
- [Docker](https://www.docker.com/get-started)

## Installation

1. **Clone the repository and navigate into the directory:**

    ```bash
    git clone https://github.com/RodrigoVictor01/Mini-Twitter-API.git
    cd mini-twitter
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install dependencies:**

    The `requirements.txt` file is located in the project root. Run:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL database:**

    1. **Create a database:**

        Access the PostgreSQL terminal:

        ```bash
        psql -U your_username
        ```

        Then, create the database:

        ```sql
        CREATE DATABASE database_name;
        \q
        ```

    2. **Update `settings.py` with your database credentials:**

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'database_name',
                'USER': 'your_username',
                'PASSWORD': 'your_password',
                'HOST': 'db',
                'PORT': '5432',
            }
        }
        ```

5. **Ensure Redis is running and accessible.**

   Example Redis URL for Django settings:

   ```plaintext
   REDIS_URL=redis://redis:6379/0


7. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

8. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

---

## Unit Tests

This project includes unit tests to validate core features.

### Running Tests

1. **Activate your virtual environment:**

    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Run tests for individual apps:**

    For the `users` app:

    ```bash
     docker-compose exec web python manage.py test users.tests -v 2
    ```

    For the `posts` app:

    ```bash
    docker-compose exec web python manage.py test posts.tests -v 2
    ```

### Test Structure

Examples:

- `users/tests/test_file.py`
- `posts/tests/test_file.py`

---

## Docker

You can run the entire project using Docker and Docker Compose.

1. **Build and run containers:**

    ```bash
    docker-compose up --build
    ```

2. **Access the app at:**

    [http://localhost:8000](http://localhost:8000)

---

## API Documentation

Interactive API documentation (Swagger) is available at:

[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)


---

## Contact

For questions, feel free to reach out at [rodrigo.victor.3344@live.com](rodrigo.victor.3344@live.com).




