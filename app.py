from flask import Flask

from flask import jsonify, Response, request
from  FileOperations import  read_users_data
from FileOperations import read_group_data
from  multiprocessing import Process, Lock, Queue
import os

app = Flask(__name__)

users= {}
groups = {}

q = Queue()

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


""" validates all the query params passed by the user"""


def validate_user_object(request_args):
    # if len(1) then O(1) lookup by id
    if len(request_args) ==1 and 'uid ' in request_args:
        return users[request_args['uid']]

    ret = []
    total_query_length = len(request_args)
    for user_id,values_map in users.items():
        result = []
        for requested_item in request_args.items():
            # check if the users values have matching values
            if str(values_map[requested_item[0]]) != requested_item[1]:
                break
            else:
                result.append(requested_item)

        # check if the values equaled the checked values and append to return list
        if len(result) == total_query_length:
            ret.append(values_map)

    return ret


""":returns users matched in the  query optional params [name uid gid comment home shell] """


@app.route('/api/v1/users/query',methods=['GET'])
def get_users_with_query():
    request_args = request.args
    ret = {}
    if 'uid' in request_args:
        if int(request_args['uid']) in users:
           ret = validate_user_object(request_args)
        else:
            ret = {}
    else:
        ret = validate_user_object(request_args)

    return jsonify(ret)


def watch_file(lock, arg1, arg2,sleep_timer):
    mode_time_1 = 0.0
    mode_time_2 = 0.0
    import time
    while True:
        time.sleep(sleep_timer)
        print('reading')
        lock.acquire()
        if mode_time_1 != os.path.getmtime(arg1):
            mode_time_1 =  os.path.getmtime(arg1)
            new_data =read_group_data(arg1)
            users = new_data
            print('data changed')

        if mode_time_2 != os.path.getmtime(arg2):
            mode_time_2 =  os.path.getmtime(arg2)
        lock.release()


if __name__ == '__main__':
    file_1='/Users/loaner/PycharmProjects/app-flask/passwd'
    file_2 = '/Users/loaner/PycharmProjects/app-flask/group'
    lock = Lock()
    sleep_timer = 2
    users = read_users_data(file_1)
    groups = read_group_data(file_2)
    backProc = Process(target=watch_file, args=(lock, file_1,file_2,sleep_timer))
    backProc.start()
    app.run(debug=True, host='0.0.0.0', port=8080)
