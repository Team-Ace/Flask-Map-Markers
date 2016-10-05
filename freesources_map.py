import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, flash, render_template, send_file
import folium

app = Flask(__name__)
app.config.from_object(__name__)

# App config
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'freesources.db'),
	SECRET_KEY='i_l0ve_py',
	USERNAME='admin',
	PASSWORD='grapes1234'
))
app.config.from_envvar('FREESOURCES_SETTINGS', silent=True)

initial_location = [40.806290, -73.963005]
markers = []
curr_map = folium.Map(location=initial_location, zoom_start=8)
curr_map.save('templates/osm.html')

def connect_db():
	"""Connects to database."""
	conn = sqlite3.connect(app.config['DATABASE'])
	conn.row_factory = sqlite3.Row
	return conn

def get_db():
	"""Opens new db connection if none exists."""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	"""Initialize database."""
	init_db()
	print('Initialized database')

@app.teardown_appcontext
def close_db(error):
	"""Closes the database at end of request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def map():
	return render_template('freesources_map.html')

@app.route('/map')
def show_map():
	return send_file('templates/osm.html')

@app.route('/view_db')
def show_entries():
	db = get_db()
	cur = db.execute('select marker, latlong from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (marker, latlong) values (?, ?)',
                 [request.form['marker'], request.form['latlong']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/submit_markers', methods=["GET"])
def update_db():
	global markers
	latlong = request.args.get('marker')
	db = get_db()
	db.execute('insert into entries (marker, latlong) values (?, ?)', [0, latlong])
	db.commit()
	print('New entry posted')
	flash('New entry posted!')
	latlong = latlong.split(',')
	marker = folium.Marker(latlong, popup='New marker! :D').add_to(curr_map)
	markers += [marker]
	curr_map.save('templates/osm.html')

	# Send them back to map with updated data
	return redirect(url_for('map'))

if __name__ == "__main__":
	app.run()
