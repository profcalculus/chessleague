from . import ApiTest


class TestUsers(ApiTest):
    def setUp(self):
        super(TestUsers, self).setUp()
        from ..models import User
        self.User=User # local class reference
        import chessleague.api.user_api


    # def test_password_auth(self):
    #     self.app.config['USE_TOKEN_AUTH'] = False
    #     good_client = TestClient(self.app, self.default_username,
    #                              self.default_password)
    #     rv, json = good_client.get('/users/')
    #     self.assertEqual(200, rv.status_code)
    #
    #     self.app.config['USE_TOKEN_AUTH'] = True
    #     u = User.query.get(1)
    #     good_client = TestClient(self.app, u.generate_auth_token(), '')
    #     rv, json = good_client.get('/users/')
    #     self.assertEqual(200, rv.status_code)
    #
    # def test_bad_auth(self):
    #     bad_client = TestClient(self.app, 'abc', 'def')
    #     rv, json = bad_client.get('/users/')
    #     self.assertEqual(401, rv.status_code)
    #
    #     self.app.config['USE_TOKEN_AUTH'] = True
    #     bad_client = TestClient(self.app, 'bad_token', '')
    #     rv, json = bad_client.get('/users/')
    #     self.assertEqual(401, rv.status_code)

    def test_users(self):
        # get collection
        rv, json = self.client.get('/users/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, len(json['items'])) # Default user for tests

        # # create new user
        rv, json = self.client.post('/users/',
                                    data={'user_name': 'ig', 'first_name': 'Igor', 'last_name': 'Borisovitch',
                                          'password': 'Putin', 'email':'igor@borisovitch.com'})
        self.assertEqual(201, rv.status_code)
        igor_url = rv.headers['Location']

        # get igor
        rv, json = self.client.get(igor_url)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('Igor Borisovitch', json['name'])
        self.assertEqual('igor@borisovitch.com', json['email'])
        self.assertEqual(igor_url, json['uri'])

        # create new user
        rv, json = self.client.post('/users/',
                                    data={'user_name':'bora', 'first_name': 'Boris', 'last_name': 'Igorevitch',
                                          'password': 'Brezhnev','email': 'boris@igorevitch.com'})
        self.assertEqual(201, rv.status_code)
        boris_url = rv.headers['Location']

        # get boris
        rv, json = self.client.get(boris_url)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('Boris Igorevitch', json['name'])
        self.assertEqual('boris@igorevitch.com', json['email'])
        self.assertEqual(boris_url, json['uri'])

        # get users
        rv, json = self.client.get('/users/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(3, len(json['items']))

        # delete boris
        rv, json = self.client.delete(boris_url)
        self.assertEqual(204, rv.status_code)

        # Make sure he's gone
        rv, json = self.client.get(boris_url)
        self.assertEqual(404, rv.status_code) # Not found
        # get users
        rv, json = self.client.get('/users/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(2, len(json['items']))

    def test_auth(self):
        # create new user
        rv, json = self.client.post('/users/',
                                    data={'user_name':'bora', 'first_name': 'Boris', 'last_name': 'Igorevitch',
                                          'password': 'Brezhnev','email': 'boris@igorevitch.com'})
        self.assertEqual(201, rv.status_code)
        bora_url = rv.headers['Location']
        token = self.User.authenticate('bora', 'Brezhnev')

        # rv,json = self.client.put(boris_url, data={'team':'Zugzwangers'})
        # self.assertEqual(204, rv.status_code)
        # self.assertEqual({}, json)
        # rv, json = self.client.get(boris_url)
        # self.assertEqual('Zugzwangers', json['team']['name'])
        # self.assertEqual(zz_url, json['team']['uri'])



        # create bad request
        # rv,json = self.client.post('/users/', data={})
        # self.assertEqual(400, rv.status_code)
        #
        # self.assertRaises(ValidationError, lambda:
        #     self.client.post('/users/',
        #                      data={'not-name': 'david'}))
        #
        # # modify
        # rv, json = self.client.put(david_url, data={'name': 'david2'})
        # self.assertEqual(200, rv.status_code)
        #
        # # get
        # rv, json = self.client.get(david_url)
        # self.assertEqual(200, rv.status_code)
        # self.assertEqual('david2', json['name'])
        #
        # # get collection
        # rv, json = self.client.get('/users/')
        # self.assertEqual(200, rv.status_code)
        # self.assertTrue(susan_url in json['urls'])
        # self.assertTrue(david_url in json['urls'])
        # self.assertTrue(len(json['urls']) == 2)
        #
        # # delete
        # rv, json = self.client.delete(susan_url)
        # self.assertEqual(200, rv.status_code)
        #
        # # get collection
        # rv, json = self.client.get('/users/')
        # self.assertEqual(200, rv.status_code)
        # self.assertFalse(susan_url in json['urls'])
        # self.assertTrue(david_url in json['urls'])
        # self.assertTrue(len(json['urls']) == 1)

    # def test_classes(self):
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/classes/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual([], json['urls'])
    #
    #     # create new
    #     rv, json = self.client.post('/api/v1.0/classes/',
    #                                 data={'name': 'algebra'})
    #     self.assertEqual(201, rv.status_code)
    #     algebra_url = rv.headers['Location']
    #
    #     # get
    #     rv, json = self.client.get(algebra_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual('algebra', json['name'])
    #     self.assertEqual(algebra_url, json['url'])
    #
    #     # create new
    #     rv, json = self.client.post('/api/v1.0/classes/',
    #                                 data={'name': 'lit'})
    #     self.assertEqual(201, rv.status_code)
    #     lit_url = rv.headers['Location']
    #
    #     # get
    #     rv, json = self.client.get(lit_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual('lit', json['name'])
    #     self.assertEqual(lit_url, json['url'])
    #
    #     # create bad
    #     rv,json = self.client.post('/api/v1.0/classes/', data={})
    #     self.assertEqual(400, rv.status_code)
    #
    #     self.assertRaises(ValidationError, lambda:
    #         self.client.post('/api/v1.0/classes/', data={'not-name': 'lit'}))
    #
    #     # modify
    #     rv, json = self.client.put(lit_url, data={'name': 'lit2'})
    #     self.assertEqual(200, rv.status_code)
    #
    #     # get
    #     rv, json = self.client.get(lit_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual('lit2', json['name'])
    #
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/classes/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(algebra_url in json['urls'])
    #     self.assertTrue(lit_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #
    #     # delete
    #     rv, json = self.client.delete(lit_url)
    #     self.assertEqual(200, rv.status_code)
    #
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/classes/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(algebra_url in json['urls'])
    #     self.assertFalse(lit_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    # def test_registrations(self):
    #     # create new students
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'susan'})
    #     self.assertEqual(201, rv.status_code)
    #     susan_url = rv.headers['Location']
    #
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'david'})
    #     self.assertEqual(201, rv.status_code)
    #     david_url = rv.headers['Location']
    #
    #     # create new classes
    #     rv, json = self.client.post('/api/v1.0/classes/',
    #                                 data={'name': 'algebra'})
    #     self.assertEqual(201, rv.status_code)
    #     algebra_url = rv.headers['Location']
    #
    #     rv, json = self.client.post('/api/v1.0/classes/',
    #                                 data={'name': 'lit'})
    #     self.assertEqual(201, rv.status_code)
    #     lit_url = rv.headers['Location']
    #
    #     # register students to classes
    #     rv, json = self.client.post('/api/v1.0/registrations/',
    #                                 data={'student': susan_url,
    #                                       'class': algebra_url})
    #     self.assertEqual(201, rv.status_code)
    #     susan_in_algebra_url = rv.headers['Location']
    #
    #     rv, json = self.client.post('/api/v1.0/registrations/',
    #                                 data={'student': susan_url,
    #                                       'class': lit_url})
    #     self.assertEqual(201, rv.status_code)
    #     susan_in_lit_url = rv.headers['Location']
    #
    #     rv, json = self.client.post('/api/v1.0/registrations/',
    #                                 data={'student': david_url,
    #                                       'class': algebra_url})
    #     self.assertEqual(201, rv.status_code)
    #     david_in_algebra_url = rv.headers['Location']
    #
    #     # get registration
    #     rv, json = self.client.get(susan_in_lit_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(susan_url, json['student'])
    #     self.assertEqual(lit_url, json['class'])
    #
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/registrations/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(susan_in_algebra_url in json['urls'])
    #     self.assertTrue(susan_in_lit_url in json['urls'])
    #     self.assertTrue(david_in_algebra_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 3)
    #
    #     # bad registrations
    #     rv,json = self.client.post('/api/v1.0/registrations/', data={})
    #     self.assertEqual(400, rv.status_code)
    #
    #     self.assertRaises(ValidationError, lambda:
    #         self.client.post('/api/v1.0/registrations/',
    #                          data={'student': david_url}))
    #
    #     self.assertRaises(ValidationError, lambda:
    #         self.client.post('/api/v1.0/registrations/',
    #                          data={'class': algebra_url}))
    #
    #     self.assertRaises(ValidationError, lambda:
    #         self.client.post('/api/v1.0/registrations/',
    #                          data={'student': david_url, 'class': 'bad-url'}))
    #
    #     self.assertRaises(ValidationError, lambda:
    #         self.client.post('/api/v1.0/registrations/',
    #                          data={'student': david_url,
    #                                'class': algebra_url + '1'}))
    #     db.session.remove()
    #
    #     # get classes from each student
    #     rv, json = self.client.get(susan_url)
    #     self.assertEqual(200, rv.status_code)
    #     susans_reg_url = json['registrations']
    #     rv, json = self.client.get(susans_reg_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(susan_in_algebra_url in json['urls'])
    #     self.assertTrue(susan_in_lit_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #
    #     rv, json = self.client.get(david_url)
    #     self.assertEqual(200, rv.status_code)
    #     davids_reg_url = json['registrations']
    #     rv, json = self.client.get(davids_reg_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(david_in_algebra_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    #     # get students for each class
    #     rv, json = self.client.get(algebra_url)
    #     self.assertEqual(200, rv.status_code)
    #     algebras_reg_url = json['registrations']
    #     rv, json = self.client.get(algebras_reg_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(susan_in_algebra_url in json['urls'])
    #     self.assertTrue(david_in_algebra_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #
    #     rv, json = self.client.get(lit_url)
    #     self.assertEqual(200, rv.status_code)
    #     lits_reg_url = json['registrations']
    #     rv, json = self.client.get(lits_reg_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(susan_in_lit_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    #     # unregister students
    #     rv, json = self.client.delete(susan_in_algebra_url)
    #     self.assertEqual(200, rv.status_code)
    #
    #     rv, json = self.client.delete(david_in_algebra_url)
    #     self.assertEqual(200, rv.status_code)
    #
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/registrations/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertFalse(susan_in_algebra_url in json['urls'])
    #     self.assertTrue(susan_in_lit_url in json['urls'])
    #     self.assertFalse(david_in_algebra_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    #     # delete student
    #     rv, json = self.client.delete(susan_url)
    #     self.assertEqual(200, rv.status_code)
    #
    #     # get collection
    #     rv, json = self.client.get('/api/v1.0/registrations/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(len(json['urls']) == 0)
    #
    # def test_rate_limits(self):
    #     self.app.config['USE_RATE_LIMITS'] = True
    #
    #     rv, json = self.client.get('/api/v1.0/registrations/')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue('X-RateLimit-Remaining' in rv.headers)
    #     self.assertTrue('X-RateLimit-Limit' in rv.headers)
    #     self.assertTrue('X-RateLimit-Reset' in rv.headers)
    #     self.assertTrue(int(rv.headers['X-RateLimit-Limit']) == int(rv.headers['X-RateLimit-Remaining']) + 1)
    #     while int(rv.headers['X-RateLimit-Remaining']) > 0:
    #         rv, json = self.client.get('/api/v1.0/registrations/')
    #     self.assertEqual(429, rv.status_code)
    #
    # def test_pagination(self):
    #     # create several students
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'one'})
    #     self.assertEqual(201, rv.status_code)
    #     one_url = rv.headers['Location']
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'two'})
    #     self.assertEqual(201, rv.status_code)
    #     two_url = rv.headers['Location']
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'three'})
    #     self.assertEqual(201, rv.status_code)
    #     three_url = rv.headers['Location']
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'four'})
    #     self.assertEqual(201, rv.status_code)
    #     four_url = rv.headers['Location']
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'five'})
    #     self.assertEqual(201, rv.status_code)
    #     five_url = rv.headers['Location']
    #
    #     # get collection in pages
    #     rv, json = self.client.get('/users/?page=1&per_page=2')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(one_url in json['urls'])
    #     self.assertTrue(two_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #     self.assertTrue('total' in json['meta'])
    #     self.assertEqual(5, json['meta']['total'])
    #     self.assertTrue('prev' in json['meta'])
    #     self.assertTrue(json['meta']['prev'] is None)
    #     first_url = json['meta']['first'].replace('http://localhost', '')
    #     last_url = json['meta']['last'].replace('http://localhost', '')
    #     next_url = json['meta']['next'].replace('http://localhost', '')
    #
    #     rv, json = self.client.get(first_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(one_url in json['urls'])
    #     self.assertTrue(two_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #
    #     rv, json = self.client.get(next_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(three_url in json['urls'])
    #     self.assertTrue(four_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 2)
    #     next_url = json['meta']['next'].replace('http://localhost', '')
    #
    #     rv, json = self.client.get(next_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(five_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    #     rv, json = self.client.get(last_url)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue(five_url in json['urls'])
    #     self.assertTrue(len(json['urls']) == 1)
    #
    # def test_cache_control(self):
    #     client = TestClient(self.app, self.default_username,
    #                         self.default_password)
    #     rv, json = client.get('/auth/request-token')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertTrue('Cache-Control' in rv.headers)
    #     cache = [c.strip() for c in rv.headers['Cache-Control'].split(',')]
    #     self.assertTrue('no-cache' in cache)
    #     self.assertTrue('no-store' in cache)
    #     self.assertTrue('max-age=0' in cache)
    #     self.assertTrue(len(cache) == 3)
    #
    # def test_etag(self):
    #     # create two students
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'one'})
    #     self.assertEqual(201, rv.status_code)
    #     one_url = rv.headers['Location']
    #     rv, json = self.client.post('/users/',
    #                                 data={'name': 'two'})
    #     self.assertEqual(201, rv.status_code)
    #     two_url = rv.headers['Location']
    #
    #     # get their etags
    #     rv, json = self.client.get(one_url)
    #     self.assertEqual(200, rv.status_code)
    #     one_etag = rv.headers['ETag']
    #     rv, json = self.client.get(two_url)
    #     self.assertEqual(200, rv.status_code)
    #     two_etag = rv.headers['ETag']
    #
    #     # send If-None-Match header
    #     rv, json = self.client.get(one_url, headers={
    #         'If-None-Match': one_etag})
    #     self.assertEqual(304, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-None-Match': one_etag + ', ' + two_etag})
    #     self.assertEqual(304, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-None-Match': two_etag})
    #     self.assertEqual(200, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-None-Match': two_etag + ', *'})
    #     self.assertEqual(304, rv.status_code)
    #
    #     # send If-Match header
    #     rv, json = self.client.get(one_url, headers={
    #         'If-Match': one_etag})
    #     self.assertEqual(200, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-Match': one_etag + ', ' + two_etag})
    #     self.assertEqual(200, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-Match': two_etag})
    #     self.assertEqual(412, rv.status_code)
    #     rv, json = self.client.get(one_url, headers={
    #         'If-Match': '*'})
    #     self.assertEqual(200, rv.status_code)
    #
    #     # change a resource
    #     rv, json = self.client.put(one_url, data={'name': 'not-one'})
    #     self.assertEqual(200, rv.status_code)
    #
    #     # use stale etag
    #     rv, json = self.client.get(one_url, headers={
    #         'If-None-Match': one_etag})
    #     self.assertEqual(200, rv.status_code)
if __name__ == '__main__':
    unittest.main()
