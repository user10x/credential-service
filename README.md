# credential-service

# read from the passwd and groups file data

Users:
  - GET all users by endpoint  /users
  - GET users by specied query on endpoint /users/query/?query_param=<query>
  - GET user by id on endpoint /users/<uid> or 404

Groups:
  - GET all groups /groups
  - GET all groups for user by id on endpoint /groups/<uid>/groups
  - GET groups by specied query on endpoint /users/query/?query_param=<query>
