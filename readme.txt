How to get this starter running

Step 1 : Create Python venv with the requirements
	python3 -m venv .venv 
	source .venv/bin/activate 
	pip install -r requirements.txt

Step 2 : Set up the flask db
	- make sure the user model is what you wanted
	- export FLASK_APP=app.py 
	- flask db init
	- flask db migrate
	- flask db upgrade
