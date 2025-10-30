# INF37407
# TP 1 - Inforoute UQAR

### Requirements
- Python
- Django
- MySQL Server
- Django REST framework
- Graphene-Django
- drf-yasg

### Installation
1. Clone the repository
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2. Create a virtual environment and activate it
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the MySQL database and update the `settings.py` file with your database
    credentials.
5. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Start the development server:
    ```bash
    python manage.py runserver
    ```
7. Access the application at `http://
    localhost:8000/`
### Usage
- Obtain an authentication token by registering or logging in.
- Create, read, update, and delete resources using the REST API or GraphQL interface.
- Follow the API documentation at `http://localhost:8000/swagger/` for REST endpoints.
- Access the GraphQL interface at `http://localhost:8000/graphql/`.

### Authors
- Adam Benzidane
- Alexis Salaun
