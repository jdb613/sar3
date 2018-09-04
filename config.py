import os
basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = {
    'user': 'fmqntwrubliffb',
    'pw': 'a076a655c5e74aff036ca94c0daa4e4da3d81e7974f6455ad6cb80874a22f3cf',
    'db': 'd4u0djq9omtvn',
    'host': 'ec2-54-235-94-36.compute-1.amazonaws.com',
    'port': '5432',
        }

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://fmqntwrubliffb:a076a655c5e74aff036ca94c0daa4e4da3d81e7974f6455ad6cb80874a22f3cf@ec2-54-235-94-36.compute-1.amazonaws.com:5432/d4u0djq9omtvn'
    #'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgres://fmqntwrubliffb:a076a655c5e74aff036ca94c0daa4e4da3d81e7974f6455ad6cb80874a22f3cf@ec2-54-235-94-36.compute-1.amazonaws.com:5432/d4u0djq9omtvn
