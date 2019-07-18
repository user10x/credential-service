# credential-service

# read from the passwd and groups file data

BASE_URL = http://127.0.0.1:8080/api/v1

Users:
  - GET all users by endpoint  /users
    Example: http://127.0.0.1:8080/api/v1/users
    Response:[
               {
                comment: "System Administrator",
                gid: 0,
                home: "/var/root",
                name: "root",
                shell: "/bin/sh",
                uid: 0
                }
             ]  
              
  - GET users by specied query on endpoint /users/query/?query_param=<query>
    Example: http://127.0.0.1:8080/api/v1/users/query?shell=/usr/bin/false
    Response: [
                {
                  comment: "Install Assistant",
                  gid: 25,
                  home: "/var/empty",
                  name: "_installassistant",
                  shell: "/usr/bin/false",
                  uid: 25
                },
                {
                  comment: "Printing Services",
                  gid: 26,
                  home: "/var/spool/cups",
                  name: "_lp",
                  shell: "/usr/bin/false",
                  uid: 26
               }
              ]

  
  - GET user by id on endpoint /users/<uid> or 404
    Example:{
              comment: "System Services",
              gid: 1,
              home: "/var/root",
              name: "daemon",
              shell: "/usr/bin/false",
              uid: 1
            }
      ERROR Response(404): {
                              error: "user with 2 does not exist"
                           }

Groups:

  # GET all groups /groups
  Example: http://127.0.0.1:8080/api/v1/groups
  Response: [
            {
              gid: 0,
              members: [
              "root"
              ],
              name: "wheel"
              }
            }
    ]
    
  # GET all groups for user by id on endpoint /groups/<uid>/groups or 404
  Example:  http://127.0.0.1:8080/api/v1/groups/0
  Response: {
            gid: 0,
            members: [
            "root"
            ],
            name: "wheel"
            }
  OR
  ERROR Response(404): {
            error: "group with id 1221182 does not exist"
            }
  


# prerequisite tools 
$ python -V   # Project built on Python 3.6.7 or > Python 3.4.x 

$ pip3 install virtualenv #  pip3 install --upgrade pip

$ virtualenv venv

$ source venv/bin/activate
 
# running instructions 
cd credential-service

pip3 install -r requirements.txt

python app.py /path/to/passwd /path/to/group # started on port 8080

# Todo: GET groups by specied query on endpoint /users/query/?query_param=<query>
  
# Todo: provide unittests and possible refactor code (using blueprints)

# Todo: provide setup.py file
