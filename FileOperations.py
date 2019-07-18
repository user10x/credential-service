import logging

def read_users_data(users_file):
    users = {}
    with open(users_file, 'r') as r:
        for line in r.readlines():
            try:
                if not str(line).startswith('#'):
                    user = dict()
                    line = line.split(':')
                    user["name"],user['uid'],user["gid"],user["comment"],user["home"],user["shell"]=line[0],  int(line[2]),int(line[3]), line[4], line[5], line[6]
                    users[user['uid']]=user
            except ValueError:
                logging.addLevelName(logging.DEBUG,'')
                logging.debug('line format not supported')
        return users


def read_group_data(groups_file):
    groups = {}
    with open(groups_file, 'r') as r:
        for line in r.readlines():
            try:
                if not str(line).startswith('#') or len(line) == 0:
                    group = dict()
                    line  = line.strip('\n').split(':')
                    group['name'],group['password'],group['gid']= line[0], line[1],int(line[2])
                    members = []
                    if len(line[3])>1:
                        members = line[3].split(',')
                    group['members'] = members
                    groups[group['gid']]=group

            except ValueError:
                logging.addLevelName(logging.DEBUG,'')
                logging.debug('line format not supported')

        return groups
