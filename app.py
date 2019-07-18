from flask import Flask

from flask import jsonify, Response, request
from  FileOperations import  read_users_data
from FileOperations import read_group_data

app = Flask(__name__)

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
    return jsonify({
        'groups': groups
    })


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
            # check if the users values have matching values
            if str(values_map[requested_item[0]]) != requested_item[1]:
                break
            else:
                result.append(requested_item)

        # check if the values equaled the checked values and append to return list
        if len(result) == total_query_length:
            ret.append(values_map)

    return ret


"""GET /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]"""
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

if __name__ == '__main__':
    users_file='/etc/passwd'
    group_file = '/etc/group'
    if len(sys.argv) == 2:
        file_1 = sys.argv[0]
        file_2 = sys.argv[1]
    else:
        print('using the default files ',(users_file, group_file))
    users= read_users_data(users_file)
    groups= read_group_data(group_file)
    app.run(debug=True, host='0.0.0.0', port=8080)

