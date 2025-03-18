# Configuration files
# Connecting to the database
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'Team_16'
# USERNAME = 'root'
# PASSWORD = '3076f76'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI




SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "artfinder"



# Mail configuration
MAIL_SERVER = "smtp.qq.com"  # QQ email is used in the project
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "1664924965@qq.com"
MAIL_PASSWORD = "irjsnzfssvuxefhf"
MAIL_DEFAULT_SENDER = "1664924965@qq.com"


