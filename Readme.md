# Lichess Backend

### Steps to Setup

1. Setup Postgres Server on port `5432`, create a database `lichess_db` and create password as `admin`
2. Add Lichess API TOKEN in `lichess_extract.py` file
3. (Optional) Run Command `python -m venv venv` and `venv/Scripts/activate` for windows or `venv/bin/activate` for mac or linux
4. Run command `pip install -r requirements.txt` to install the required python packages
5. Run command `python app.py` to start the application on Port `8081`
