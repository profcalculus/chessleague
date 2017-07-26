from . import ApiTest


class TestTeams(ApiTest):
    def setUp(self):
        super(TestTeams, self).setUp()
        import chessleague.api.team_api

    def test_teams(self):
        # get collection
        rv, json = self.client.get('/teams/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual([], json['items'])

        # # create new team
        rv, json = self.client.post('/teams/',
                                    data={'name': 'TamilTigers'})
        self.assertEqual(201, rv.status_code)
        tigers_url = rv.headers['Location']

        # get tigers
        rv, json = self.client.get(tigers_url)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('TamilTigers', json['name'])
        self.assertEqual(tigers_url, json['uri'])

        # create new team
        rv, json = self.client.post('/teams/',
                                    data={'name': 'Limpopo Lions'})
        self.assertEqual(201, rv.status_code)
        lions_url = rv.headers['Location']

        # get lions
        rv, json = self.client.get(lions_url)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('Limpopo Lions', json['name'])
        self.assertEqual(lions_url, json['uri'])

        # get teams
        rv, json = self.client.get('/teams/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(2, len(json['items']))

        # delete lions
        rv, json = self.client.delete(lions_url)
        self.assertEqual(204, rv.status_code)

        # Make sure he's gone
        rv, json = self.client.get(lions_url)
        self.assertEqual(404, rv.status_code) # Not found

        # get teams
        rv, json = self.client.get('/teams/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, len(json['items']))

    def test_team_players(self):
        # create new teams
        rv, json = self.client.post('/teams/', data={'name': 'Zugzwangers'})
        self.assertEqual(201, rv.status_code)
        zz_url = rv.headers['Location']
        rv, json = self.client.post('/teams/', data={'name': 'Perpetuals'})
        self.assertEqual(201, rv.status_code)
        pp_url = rv.headers['Location']

        # Create some players and add them to the teams
        for p in range(1,7):
            self.client.post('/players/', data={
            'first_name': 'first%02d' % p,'last_name': 'last_%02d' % p,
            'dob':'1998-02-%d' % p, 'team': 'Zugzwangers' })
        for p in range(7,12):
            self.client.post('/players/', data={
            'first_name': 'first%02d' % p,'last_name': 'last_%02d' % p,
            'dob':'1999-02-%d' % p, 'team': 'Perpetuals' })

        rv_team, json_team = self.client.get(zz_url)
        rv_players, json_players = self.client.get(json_team['players'])
        self.assertEqual(6, len(json_players))
        self.assertTrue(all(['Zugzwangers' == player['team']['name'] for player in json_players]))
