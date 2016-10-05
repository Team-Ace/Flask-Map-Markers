import os
import freesources_map
import unittest
import tempfile

class FreesourcesTest(unittest.TestCase):

	def setUp(self):
		self.db_fd, freesources_map.app.config['DATABASE'] = tempfile.mkstemp()
		freesources_map.app.config['TESTING'] = True
		self.app = freesources_map.app.test_client()
		with freesources_map.app.app_context():
			freesources_map.init_db()
	
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(freesources_map.app.config['DATABASE'])

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
		), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_empty_db(self):
		conn = self.app.get('/view_db')
		assert b'No entries here so far' in conn.data

	def test_messages(self):
		self.login('admin', 'grapes1234')
		conn = self.app.post('/add', data=dict(
			title='<Hello>',
			text='<strong>HTML</strong> allowed here'
		), follow_redirects=True)
		assert b'No entries here so far' not in conn.data
		assert b'&lt;Hello&gt;' in conn.data
		assert b'<strong>HTML</strong> allowed here' in conn.data

if __name__ == '__main__':
	unittest.main()
