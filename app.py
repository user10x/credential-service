from flask import Flask
from flask import jsonify, Response
import  json

app = Flask(__name__)

# todo read from file
users = [
    {
        "name": "root",
        "uid": 0, "gid": 0,
        "comment": "root",
        "home": "/root",
        "shell": "/bin/bash"
    },
    {
        "name": "dwoodlins",
        "uid": 1001, "gid": 1001,
        "comment": "",
        "home":"/home/dwoodlins",
        "shell": "/bin/false"
    }
]

# todo read from file
groups = [
    {
        "name": "_analyticsusers",
        "gid": 250,
        "members":["_analyticsd","_networkd","_timed"]
    },
    {
        "name": "docker",
        "gid": 1002,
        "members": []
    }
]


""":returns list[users]"""

@app.route('/api/v1/users',methods=['GET'])
def get_users():
    return jsonify({
        'users': users
    })

""":return user by id"""

@app.route('/api/v1/users/<int:uid>')
def get_user_by_id(uid):
    ret = {}
    for user in users :
        if users['uid'] == uid:
            ret =  user
    return jsonify(ret)


""":returns list[groups]"""

@app.route('/api/v1/groups',methods=['GET'])
def get_groups():
    return jsonify({
        'groups': groups
    })



""":return group by gid"""

@app.route('/api/v1/groups/<int:gid>')
def get_group_by_id(gid):
    ret = {}
    for group in groups :
        if group['gid'] == gid:
            ret =  group
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

