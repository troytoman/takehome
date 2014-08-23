#!flask/bin/python
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

users = []
groups = []


def find_user(userid):
    user = next((u for u in users if u['userid'] == userid), None)
    return user


def find_group_users(group):
    userlist = [u['userid'] for u in users if group in u['groups']]
    return userlist


@app.route('/users/<userid>', methods=['GET'])
def get_user(userid):
    """
        GET /users/<userid>
        Returns the matching user record or 404 if none exist.
    """
    user = find_user(userid)
    if user:
        return jsonify(user)
    else:
        abort(404)


@app.route('/users/<userid>', methods=['POST'])
def add_user(userid):
    if not request.json or userid != request.json['userid']:
        abort(400)
    user = find_user(userid)
    if user:
        abort(409)
    for g in request.json['groups']:
        if g not in groups:
            abort(422)
    newuser = {
        'userid': request.json['userid'],
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'groups': request.json['groups']
    }
    users.append(newuser)
    return jsonify(newuser), 201


@app.route('/users/<userid>', methods=['PUT'])
def mod_user(userid):
    if not request.json or userid != request.json['userid']:
        abort(400)
    for u in users:
        if u['userid'] == request.json['userid']:
            u['first_name'] = request.json['first_name']
            u['last_name'] = request.json['last_name']
            u['groups'] = request.json['groups']
            return jsonify(u), 200
    abort(404)


@app.route('/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    user = find_user(userid)
    if user:
        users.remove(user)
        return jsonify({'result': True}), 204
    else:
        abort(404)


@app.route('/groups/<group>', methods=['GET'])
def get_group(group):
    if group in groups:
        result = find_group_users(group)
        if result == []:
            abort(404)
        return jsonify({'users': result}), 200
    else:
        abort(404)


@app.route('/groups/<group>', methods=['POST'])
def add_group(group):
    if group in groups:
        abort(409)
    else:
        groups.append(group)
        return jsonify({'result': True}), 201


@app.route('/groups/<group>', methods=['PUT'])
def mod_group(group):
    if not request.json:
        abort(400)
    userlist = []
    if group in groups:
        for u in users:
            if group in u['groups']:
                u['groups'].remove(group)
            if u['userid'] in request.json['users']:
                userlist.append(u['userid'])
                u['groups'].append(u['userid'])
        return jsonify({'users': userlist}), 200
    else:
        abort(404)


@app.route('/groups/<group>', methods=['DELETE'])
def delete_group(group):
    if group in groups:
        for u in users:
            if group in u['groups']:
                u['groups'].remove(group)
        return jsonify({'result': True}), 204
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
