from flask import Flask

from flask import jsonify

app = Flask(__name__)

# dummy user data @todo: read from file
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
        if user['uid'] == uid:
            ret =  user
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

