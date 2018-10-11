from sqlalchemy import func
from app.models import Srep, Leaver, Suspect, Buckets
from flask_login import current_user
from app import app, db
import os
import datetime

def indx_tbls_update(target, rez, link):

    if rez == 'Recapture' or rez == 'Lead' or rez == 'Left Industry':
        target.result = rez
        target.leaverrole = target.trackrole
        target.leaverfirm = target.trackfirm
        target.outprosshell = datetime.datetime.now(datetime.timezone.utc)
        target.inprosshell = 'No'
        target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
        target.link = link

    elif rez == 'Inactive':
        target.result = rez
        target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

    elif rez == 'Manual Track':
        print('Confirmed: ', rez)
        target.link = link
        target.trackend = None
        target.trackrole = None
        target.trackfirm = None
        target.tracklocation = None
        target.lasttracked = None
        target.outprosshell = datetime.datetime.now(datetime.timezone.utc)
        target.result = rez
        target.inprosshell = 'No'
        target.trackstart = datetime.datetime.now(datetime.timezone.utc)

    elif rez == 'Engaged':
        print('Confirmed: ', rez)
        target.estart = datetime.datetime.now(datetime.timezone.utc)
        target.result = rez

    elif rez == 'Lost Business':
        print('Confirmed: ', rez)
        target.eend = datetime.datetime.now(datetime.timezone.utc)
        target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
        target.result = rez

    elif rez == 'Error':
        target.result = 'Tracking'
        target.trackrole = None
        target.trackfirm = None
        target.tracklocation = None
        target.lasttracked = None
        target.datetimeresult = None
        target.trackend = None

    elif rez == 'Delayed Trial':
        print('Delayed Trial')
        print('Leaver to be Deleted: ', target.name)
        target.suspects.delete()
        ident = target.id
        Leaver.query.filter_by(id=ident).delete()

    try:
        db.session.commit()
        return 'Success'
    except:
        db.session.rollback()
        return 'Failure'
