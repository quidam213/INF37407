# INF37407 - Technologies de l'inforoute
# TP-1

### Description
This project is a school project from our INF37407 - Technologies de l'inforoute class by PhD. Yacine Yaddaden at UQAR (Université du Québec à Rimouski), QC, Canada.

The goal of this project is to discover the django framework to build a Rest API and a GraphQL API, both alimented by a MySQL database (our choice here) and populated by canadian government free access data of their arcgis API, retrieve by a parser.

### Requirements
All requirements needed is MySQL, Python (3.14.0) and the packages listed in `requirements.txt`.

### Installation
1. Clone and access the repository
    ```bash
    git clone https://github.com/quidam213/INF37407
    cd INF37407
    ```
2. Create a virtual environment and activate it (you can run on your native env but it is not recommended).
    ```bash
    python -m venv [venv_name]
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the MySQL database and create a `.env` file, you can take a look at the `.env.example` to see what is intented.
5. Run migrations:
    ```bash
    python /path/to/manage.py makemigrations
    python /path/to/manage.py migrate
    ```
6. Run the `parser_arcgis.py` with the django command associated with it to populate your database (You can also change the file content itself if you want to add services or custom the parsing).
    ```bash
    python /path/to/manage.py parser_arcgis
    ```
7. Create a django admin account to be able to access the admin page.
    ```bash
    python /path/to/manage.py createsuperuser
    ```
8. Start the server:
    ```bash
    python /path/to/manage.py runserver
    ```
9. Access the application at `http://localhost:8000/` (you can change the default port in the `settings.py`).

### Deployment
To deploy django we need to use a web server to ensure the quality of our project.
At this point we used previously the command `runserver` with the django `manage.py` file that would run a simple server to dev.
Now we will use Uvicorn that runs ASGI project, an asynchrous web server that support python and ideal for django (we could also use WSGI but it is not asynchrous).

To run it, do the following command in the directory of `manage.py`:
```bash
    python -m uvicorn INF37407.asgi:application --host [HOST] --port [PORT]
```
You can also add the --reload flag to reload when you change a file but since this is meant to be deployed it is not ideal to dev on that.

If you want to maximize the app, you can use Gunicorn + Uvicorn but we won't here.

### Usage
- Obtain an access token by registering or logging in.
- Create, read, update, and delete resources using the REST API or GraphQL interface.
- Follow the API documentation at `http://localhost:8000/api/swagger` for REST endpoints.
- Access the GraphQL interface at `http://localhost:8000/graphql/`.
- Access the Django panel admin at `http://localhost:8000/admin`.
- View usage statistics at `http://localhost:8000/admin/stats/` (admin access required).

### Authors
- Adam Benzidane
- Alexis Salaun
