# credential-service

# read from the passwd and groups file data

Users:
  - GET all users by endpoint  /users
  - GET users by specied query on endpoint /users/query/?query_param=<query>
  - GET user by id on endpoint /users/<uid> or 404

Groups:
  - GET all groups /groups
  - GET all groups for user by id on endpoint /groups/<uid>/groups or 404
  - GET groups by specied query on endpoint /users/query/?query_param=<query>
 
 
# prerequisite tools 
$ python -V   # Project built on Python 3.6.7 or > Python 3.4.x 

$ pip3 install virtualenv #  pip3 install --upgrade pip

$ virtualenv venv

$ source venv/bin/activate
 
# running instructions 
cd credential-service

pip3 install -r requirements.txt

python app.py /path/to/passwd /path/to/group # started on port 8080


# Todo: export postman calls/provide curl calls to test/ use click to make calls
# Todo: provide unittests and possible refactor code (using blueprints)
# Todo: provide setup.py file
