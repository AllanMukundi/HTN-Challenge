import flask, sqlite3

database = 'HTN_challenge.db'
app = flask.Flask(__name__)

def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(database)
    return db

@app.route('/users', methods=['GET'])
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchall()
    cursor_s = get_db().cursor()
    for i in range(len(data)):
        data[i] = list(data[i])
        cursor_s.execute("SELECT * FROM Skills WHERE email=:email", {'email': data[i][4]})
        data_s = cursor_s.fetchall()
        skills = []
        for n in (range(len(data_s))):
            data_s[n] = list(data_s[n])
            del data_s[n][0]
            skills.append(data_s[n])
        data[i].extend(skills)
    return flask.jsonify(data)

@app.route('/users/<int:id>', methods=['GET', 'PUT'])
def user(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM Users WHERE ID = ?", (id,))
    data = cursor.fetchone()
    data = list(data)
    cursor_s = get_db().cursor()
    cursor_s.execute("SELECT * FROM Skills WHERE email=:email", {'email': data[4]})
    data_s = cursor_s.fetchall()
    skills = []
    for i in range(len(data_s)):
        data_s[i] = list(data_s[i])
        del data_s[i][0]
        skills.append(data_s[i])
    data.extend(skills)
    return flask.jsonify(data)
def update(id):
    None

@app.teardown_request
def teardown_request(exception):
    if hasattr(flask.g, 'db'):
        flask.g.db.close()

if __name__ == '__main__':
    app.run(debug=True)

