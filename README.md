takehome
===================

Implements a REST service in python that can be used to store, fetch, and update user records. A user record is a JSON
hash like so:

```json
{
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "jsmith",
    "groups": ["admins", "users"]
}
```

The spec for the REST service is defined below.


Installation
=============

NOTE: This code was written and tested under Python 2.7

To start the rest service running on http://127.0.0.1:5000/

```
pip install -r requirements.txt
python takehome.py
```

Some sample requests that can be run:
```
curl -i -X POST http://127.0.0.1:5000/groups/grp1
curl -i -X POST http://127.0.0.1:5000/groups/grp2
curl -i -H "Content-Type: application/json" -X POST -d '{"first_name": "Jim", last_name": "Jones", "userid": "jjones", "groups": ["grp1", "grp2"]}' http://127.0.0.1:5000/users/jjones
curl -i -X GET http://127.0.0.1:5000/users/jjones
curl -i -X GET http://127.0.0.1:5000/users/grp1
```

To run the unit tests, enter the following commands:

```
pip install -r test-requirements.txt
./run-tests.sh
```


API SPEC
==========

```
GET /users/<userid>
    Returns the matching user record or 404 if none exist.
```

```
POST /users/<userid>
    Creates a new user record. The body of the request should be a valid user
    record. Successful POSTs will return a 201. POSTs to an existing user will
    return a status code of 409. A 400
    will be returned when the json request is missing or in the case where
    the userid in the json request does not match the URI.
```

```
DELETE /users/<userid>
    Deletes a user record. A successful DELETE will return a 204. Returns 404
    if the user doesn't exist.
```

```
PUT /users/<userid>
    Updates an existing user record. A successful PUT will return a 200. A missing JSON
    request or an error such as a conflict between userid and the URI will result in 
    return of 409. PUTs to a non-existant user should return a 404.
```

```
GET /groups/<group name>
    Returns a JSON list of userids containing the members of that group.
    Service will return a 404 if the group doesn't exist or has no members.
    Format of the response should look like:
{
  "users": ["jjones", "jjs"]
}
```

```
POST /groups/<group name>
    Creates a empty group. POSTs to an existing group will return a 409.
```

```
PUT /groups/<group name>
    Updates the membership list for the group. The body of the request should 
    be a JSON list describing the group's members. An example of a request would
    be:
{
    "users": ['jjones', 'jjs']
}

```
DELETE /groups/<group name>
    Removes all members from the named group. Should return a 404 for unknown 
    groups.
```

Implementation Notes:

1. What I would do next:
  * Tailor response messages to provide more detail 
    (e.g. 400 error when userid mismatched in URL vs. json)
  * Test more of the response data and other error conditions
  * Beef up the validation of incoming json requests
  * Automate environment build through docker or vagrant. Didn't seem
    complicated enough to warrant the work here.
  * Complete examples in API Spec with full return samples
  * Better packaging. Not quite a full python Package setup here.
2. Tried to keep as true to the spec as possible. But, I would make a
   couple of API changes if possible.
  * I would change the users POST route so that it just went to '/users' vs '/users/<userid>'
    since the userid is already in the json request body
  * I would clarify groups spec a bit more. A GET on groups returns a 404 if it either
    doesn't exist or if it doesn't have any members. So, it's not exactly clear which is true.
    Also, does DELETE get rid of the group or only remove members? Spec just says members so
    I left the group alive. But, that means there is no way to delete a group once it exists.
  * Perhaps a GET /groups (and maybe /users) to get all members of each.
