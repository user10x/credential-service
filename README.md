# credential-service
# 
# read from the passwd and groups file data

# watch part expained at the end and branch add-watch-feature(not merged)

BASE_URL = http://127.0.0.1:8080/api/v1

Users Map {uid, {user_element}}:  Storage for supporting O(1) lookup by uid
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

Groups Map {guid, {group_element}}: Storage for supporting O(1) lookup by guid

  - GET all groups /groups
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
    
  - GET all groups for user by id on endpoint /groups/<uid>/groups or 404
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
  
  - GET all groups for a user (default part of everyone) /users/<uid>/groups else 404 if user does not exist
  Example: http://127.0.0.1:8080/api/v1/users/0/group
  Response: {
                gid: 0,
                members: [
                "wheel",
                "daemon",
                "kmem",
                "sys",
                "tty",
                "operator",
                "procview",
                "procmod",
                "staff",
                "certusers",
                "admin",
                "everyone"
                ],
                name: "root"
            }
  
  ERROR Response:{
                        error: "user with id 1221182 does not exist"
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

# Todo: 
  - GET groups by specied query on endpoint /users/query/?query_param=<query>
  - provide unittests and possible refactor code (using blueprints)

# Watch file 
Create a background process running

main block : backProc = Process(target=watch_file, args=(lock, file_1,file_2,sleep_timer))
watch_file function

Call function watch file  every x seconds 
Start with 0.0 modified time for both files and compare if the file got updated with access time
create a lock for the thread to access these two variables 

Issue:
- issue the maps(users and groups) is not getting updated as its a global variable and thread is not able to update it in its scope. 

Possible Fix: 
- Use a the muliprocessing Queue class, so threads can access the data and write it back
- Use a shared_map so other process can update


Other Aspects:
- Some systems have negative user id and guid  which is not handled in the current code (url path rules would need to be defined for matching with - in the path) 


