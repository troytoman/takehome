from takehome import app
import unittest
import json


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.post('/groups/grp1')
        self.app.post('/groups/grp2')
        newuser = json.dumps({"first_name": "Jim",
                              "last_name": "Jones",
                              "userid": "jjones",
                              "groups": ["grp1", "grp2"]
                              })
        rv = self.app.post('/users/jjones',
                           data=newuser,
                           content_type='application/json')
        return rv.status_code

    def test_user_get(self):
        rv = self.app.get('/users/jjones')
        self.assertEqual(rv.status_code, 200)
        resp = json.loads(rv.data)
        self.assertEqual(resp['first_name'], 'Jim')
        self.assertEqual(resp['last_name'], 'Jones')
        self.assertEqual(resp['userid'], 'jjones')
        self.assertEqual(resp['groups'], ['grp1', 'grp2'])

    def test_user_get_error(self):
        rv = self.app.get('users/noone')
        self.assertEqual(rv.status_code, 404)

    def test_user_create_with_invalid_group(self):
        newuser = json.dumps({"first_name": "Jim",
                              "last_name": "Jones",
                              "userid": "jimj",
                              "groups": ["new1", "new2"]
                              })
        rv = self.app.post('/users/jimj',
                           data=newuser,
                           content_type='application/json')
        self.assertEqual(rv.status_code, 422)

    def test_user_post_dupe(self):
        newuser = json.dumps({"first_name": "Jim",
                              "last_name": "Jones",
                              "userid": "jjones",
                              "groups": ["grp1", "grp2"]
                              })
        rv = self.app.post('/users/jjones',
                           data=newuser,
                           content_type='application/json')
        self.assertEqual(rv.status_code, 409)

    def test_user_badreq(self):
        newuser = json.dumps({"first_name": "Jim",
                              "last_name": "Jones",
                              "userid": "jjones",
                              "groups": ["grp1", "grp2"]
                              })
        rv = self.app.post('/users/jimj',
                           data=newuser,
                           content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_user_delete(self):
        rv = self.app.delete('/users/jjones')
        self.assertEqual(rv.status_code, 204)
        rv = self.app.get('/users/jjones')
        self.assertEqual(rv.status_code, 404)

    def test_delete_nonuser(self):
        rv = self.app.delete('/users/noone')
        self.assertEqual(rv.status_code, 404)

    def test_group_get(self):
        rv = self.app.get('/groups/grp1')
        self.assertEqual(rv.status_code, 200)
        resp = json.loads(rv.data)
        self.assertEqual(resp['users'], ['jjones'])
        rv = self.app.delete('/users/jjones')

    def test_group_nomembers(self):
        self.app.post('/groups/grp3')
        rv = self.app.get('/groups/grp3')
        self.assertEqual(rv.status_code, 404)

    def test_group_dupe(self):
        rv = self.app.post('/groups/grp1')
        self.assertEqual(rv.status_code, 409)

    def test_group_delete(self):
        rv = self.app.delete('/groups/grp2')
        self.assertEqual(rv.status_code, 204)
        rv = self.app.get('/groups/grp2')
        self.assertEqual(rv.status_code, 404)

    def tests_group_delete_badgroup(self):
        rv = self.app.delete('/groups/nogroup')
        self.assertEqual(rv.status_code, 404)

    def test_group_mod(self):
        self.app.post('/groups/grp4')
        newgroup = json.dumps({"users": ['jjones']})
        rv = self.app.put('/groups/grp4',
                          data=newgroup,
                          content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        resp = json.loads(rv.data)
        self.assertEqual(resp['users'], ['jjones'])


if __name__ == '__main__':
    unittest.main()
