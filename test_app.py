from unittest import TestCase
from flask import session

from app import app, boards
from app import SESS_BOARD_UUID_KEY

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIn(SESS_BOARD_UUID_KEY, session)
            self.assertIn('<td id="row-0-col-0">', html)
            self.assertIn('<form', html)

    def test_validateword(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            # get UUID
            client.get('/') #mimics going to homepage
            unique_id = session[SESS_BOARD_UUID_KEY]
            board_instance = boards.get(unique_id)
            board_instance[0] = ['A', 'P', 'P', 'L', 'E']
            session[SESS_BOARD_UUID_KEY] = board_instance
            # print(f"{board_instance}")
            response = client.post('/api/score-word', json={"player_word": "APPLE"})

            self.assertEqual(response.json["result"], "ok")
