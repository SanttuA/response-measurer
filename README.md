# Response measurer
This is a small python app that measures given URL's response time and payload size.
Use any modern python version to run the project's main scripts `app.py` and `export_csv`. Tested to run at least with python 3.11.
The app uses SQLite to store measurements in `response_times.db` database.

To use the app first init and activate venv e.g. in Windows:
````
python -m venv venv
venv\Scripts\activate
```

Install requirements:
```
pip install -r requirements.txt
```

Create file `.env` based on `.env.example`

Start running measuring every minute:
```
python app.py
```

When you want to export measurements into a `output.csv` file, run:
```
python export_csv.py
```
