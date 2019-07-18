import os,json,sys

from flask import Flask
from flask import jsonify, Response, request
from  FileOperations import  read_users_data
from FileOperations import read_group_data

app = Flask(__name__)

# for fast lookup by id
users = {} 
groups = {}

""":returns list[users]"""

@app.route('/api/v1/users',methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

""":return user by id"""

@app.route('/api/v1/users/<int:uid>')
def get_user_by_id(uid):
    ret = None
    if uid in users:
        ret = users[uid]
    else:
        invaliUserObjectErrorMsg = {
            'error': 'user with ' + str(uid) + ' does not exist'
        }
        return Response(json.dumps(invaliUserObjectErrorMsg), status=404, mimetype='application/json')
    
    return jsonify(ret)


""":returns list[groups]"""

@app.route('/api/v1/groups',methods=['GET'])
def get_groups():
    return jsonify( list(groups.values()))

""":return group by gid"""

@app.route('/api/v1/groups/<int:gid>')
def get_group_by_id(gid):
    ret = None
    if gid in groups:
        ret = groups[gid]
    else:
        invalidGroupObjectErrorMsg = {
            'error': 'group with id ' + str(gid) + ' does not exist'
        }
        return Response(json.dumps(invalidGroupObjectErrorMsg), status=404, mimetype='application/json')
    return jsonify(ret)

""" validates all the query params passed by the user"""

def validate_user_object(request_args):
    ret = []
    total_query_length = len(request_args)
    for user_id,values_map in users.items():
        result = []
        for requested_item in request_args.items():
             # if len(1) then O(1) and lookup by id
            if str(values_map[requested_item[0]]) != requested_item[1]:
                break
            else:
                result.append(requested_item)

        # check if the values equaled the checked values and append to return list
        if len(result) == total_query_length:
            ret.append(values_map)

    return ret


"""returns with query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]"""

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


"""":returns user with all the groups """

@app.route('/api/v1/users/<int:uid>/group')
def get_groups_for_user(uid):
    if uid not in users:
        invaliUserObjectErrorMsg = {
            'error': 'user with ' + str(uid) + ' does not exist'
        }
        return Response(json.dumps(invaliUserObjectErrorMsg), status=404, mimetype='application/json')

    user_element = users[uid]
    user_name = user_element['name']

    members = []
    for group in groups.values():
        for ele in group['members']:
            if user_name == ele:
                members.append(group['name'])

    gid = user_element['gid']

    # on unix mac all the groups are part of this (id username), this may vary on other system
    members.append('everyone')

    ret = {
        'name': user_name,
        'gid': gid,
        'members': members
    }

    return jsonify(ret)

if __name__ == '__main__':
    users_file='/etc/passwd'
    group_file = '/etc/group'
    
    if len(sys.argv) == 3:
        file_1 = sys.argv[1]
        file_2 = sys.argv[2]
    else:
        print('using the default files ',(users_file, group_file))
        
    users= read_users_data(users_file)
    groups= read_group_data(group_file)
    app.run(port=8080)

