from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'note'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456788'
app.config['MYSQL_DATABASE_DB'] = 'note_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)