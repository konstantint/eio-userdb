# Development settings
DEBUG = True
SQLALCHEMY_ECHO = True
MAIL_SUPPRESS_SEND = False

# App settings
SECRET_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
SECRET_PASSWORD = 's3cr3t-p4ssw0rd'
CONTEST_ID = 1
REGISTRATION_SERVER_URL = 'http://localhost:5000/'
CONTEST_SERVER_URL = 'http://localhost/'
CONTACT_URL = 'http://eio.ut.ee/'

# Database connection
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')

# Deployment option
APPLICATION_ROOT = '/'  # Untested
DEBUG_SERVER_HOST = '0.0.0.0'
DEBUG_SERVER_PORT = 33300

# Flask-mail config
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'Eesti Informaatika Olympiaadide Server <kt@ut.ee>'

