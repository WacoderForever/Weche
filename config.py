import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-security-key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    WECHE_MAIL_SUBJECT_PREFIX = '[Weche]'
    WECHE_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    WECHE_ADMIN = os.environ.get('WECHE_ADMIN')
    WECHE_MAIL_SERVER='smtp.gmail.com'
    WECHE_MAIL_PORT=587
    WECHE_MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    WECHE_MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True  
    MAIL_USE_SSL= False


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('WECHE_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('WECHE_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'data.sqlite')
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}