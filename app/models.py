from app import db, login
from datetime import datetime
from flask_login import UserMixin


class Srep(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    repcode = db.Column(db.String(10), unique=True)
    teamcode = db.Column(db.String(10))
    leavers = db.relationship('Leaver', backref='rep', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Leaver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    prosrole = db.Column(db.String(100))
    prosfirm = db.Column(db.String(100))
    prosnum = db.Column(db.BigInteger)
    repcode = db.Column(db.String(10), db.ForeignKey('srep.repcode'))
    teamcode = db.Column(db.String(10))
    datetimeadded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    datetimeresult = db.Column(db.DateTime, index=True)
    inprosshell = db.Column(db.String(10))
    result = db.Column(db.String(50), default="Lost")
    leaverrole = db.Column(db.String(250))
    leaverfirm = db.Column(db.String(100))
    leaverlocation = db.Column(db.String(100))
    link = db.Column(db.String(200))
    trackrole = db.Column(db.String(250))
    trackfirm = db.Column(db.String(100))
    tracklocation = db.Column(db.String(100))
    lasttracked = db.Column(db.DateTime, index=True)
    suspectcheck = db.Column(db.DateTime, index=True)
    suspects = db.relationship('Suspect', backref='leaver', lazy='dynamic')
    trackstart = db.Column(db.DateTime, index=True)
    trackend = db.Column(db.DateTime, index=True)
    outprosshell = db.Column(db.DateTime, index=True)
    estart = db.Column(db.DateTime, index=True)
    eend = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Leaver {}>'.format(self.name)

class Suspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leaverid = db.Column(db.Integer, db.ForeignKey('leaver.id'))
    name = db.Column(db.String(100))
    srole = db.Column(db.String(250))
    sfirm = db.Column(db.String(100))
    slocation = db.Column(db.String(75))
    slink = db.Column(db.String(100), unique=True)
    datetimeadded = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    datetimeresult = db.Column(db.DateTime, index=True)
    result = db.Column(db.String(50))

    def __repr__(self):
        return '<Leaver {}>'.format(self.name)

class Buckets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), index=True)
    count = db.Column(db.Integer, index=True)
    team = db.Column(db.String(20), index=True)
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Bucket {}>'.format(self.name)

class LJFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), index=True)
    count = db.Column(db.Integer, index=True)
    team = db.Column(db.String(20), index=True)
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<LJFT {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return Srep.query.get(int(id))


# flask db init
# flask db migrate -m "db setup"
# flask db upgrade
