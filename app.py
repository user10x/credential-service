from flask import Flask
from flask import jsonify, Response
from  FileOperations import  read_users_data
from FileOperations import read_group_data

app = Flask(__name__)

# globalmap for storing info
users = {}
groups = {}


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
    if uid in users:
        ret = users[uid]
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
    if gid in groups:
        ret =  groups[gid]
    return jsonify(ret)


if __name__ == '__main__':
    users= read_users_data('/etc/passwd')
    groups= read_group_data('/etc/group')
    app.run(debug=True, host='0.0.0.0', port=8080)

