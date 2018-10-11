from app.models import Srep, Leaver, Suspect, Buckets
from app import app, db
import datetime
from flask_login import current_user
from sqlalchemy import func


def match_html(id, flag):

# HTML for the Card on match.html
    if flag == 1:
        leavers = Leaver.query.filter_by(repcode=current_user.repcode, inprosshell='Yes', result='Lost').all()
        leaver_dict = []
        drop_html = '<option value="">Select Leaver</option>'
        for l in leavers:
            suspects = Suspect.query.filter_by(leaverid=l.id, result=None).all()
            num = len(suspects)
            if num > 0:
                dval = l.name + ' ' + '(' + str(num) + ')'
                s_dict = {'ident': l.id, 'name': dval}
                drop_html += '<option value="' + str(l.id) + '">' + dval + '</option>'
        print('HTML to DropDown: ', drop_html)
        return drop_html

# HTML Generation for PROS Card on MATCH.html
    elif flag == 2:
        l = Leaver.query.filter_by(id=id).first()
        html = str('<div id="PROS"><div class="card-body"><div class="text-center"><h5 class="card-title">PROS Record</h5><ul class="list-inline"><li class="list-inline-item list-group-item-primary">Name: '
        + str(l.name) + '<li class="list-inline-item list-group-item-dark">Role: '
        + str(l.prosrole) + '<li class="list-inline-item list-group-item-primary">Firm: '
        + str(l.prosfirm) + '<li class="list-inline-item list-group-item-dark">Date Added: '
        + str(l.datetimeadded.date().strftime('%m/%d/%Y')) + '</li></ul></div></div>')

        print('HTML to Match Card: ', html)
        return html

#HTML for Table on MATCH.html
    elif flag == 3:
        susp_list = []
        suspects = Suspect.query.filter_by(leaverid=id, result=None).all()
        html = '<thead class="thead-light"><tr><th>ID</th><th>Name</th><th>Role</th><th>Firm</th><th>Location</th><th>Link</th><th>Action</th></tr></thead><tbody>'
        for l in suspects:
            html += str('<tr><td>'
            + str(l.id) + '</td><td>'
            + str(l.name) + '</td><td>'
            + str(l.srole) + '</td><td class="text"><span>'
            + str(l.sfirm) + '</span></td><td>'
            + str(l.slocation) + '</td><td><a target="_blank" href="'
            + str(l.slink) + ' ">LinkedIn</a></td><td><div class="dropdown"><div class="btn-group">'
            + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
            + 'Action<span class="caret"></span></button>'
            + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
            + '<li><a class="dropdown-item" href="#">Lead</a></li>'
            + '<li><a class="dropdown-item" href="#">Track</a></li>'
            + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
            + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
            + '<li><a class="dropdown-item" href="#" data-value="Remove">Remove</a></li></ul></div></div></td></tr>')
        html += '</tbody>'

        print('HTML to Match Table: ', html)
        return html

def suspect_remove(sid):
    suspect = Suspect.query.filter_by(id=sid).first()
    suspect.result = 'Removed'
    suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    lid = suspect.leaverid

    try:
        db.session.commit()
        return 'Success'
    except:
        db.session.rollback()
        return 'Failure'

def suspect_sort(sid, selection):
    suspect = Suspect.query.filter_by(id=sid).first()
    leaver = Leaver.query.filter_by(id=suspect.leaverid).first()

    if selection == 'Lead':
        leaver.result = 'Lead'
        leaver.leaverrole = suspect.srole
        leaver.leaverfirm = suspect.sfirm
        leaver.link = suspect.slink
        leaver.leaverlocation = suspect.slocation
        leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
        leaver.inprosshell = 'No'
        leaver.outprosshell = datetime.datetime.now(datetime.timezone.utc)

        suspect.result = 'Selected'
        suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        try:
            db.session.commit()
            return 'Success'
        except:
            db.session.rollback()
            return 'Failure'

    elif selection == 'Track':
        leaver.result = 'Tracking'
        leaver.leaverrole = suspect.srole
        leaver.leaverfirm = suspect.sfirm
        leaver.link = suspect.slink
        leaver.leaverlocation = suspect.slocation
        leaver.trackstart = datetime.datetime.now(datetime.timezone.utc)

        suspect.result = 'Selected'
        suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        try:
            db.session.commit()
            return 'Success'
        except:
            db.session.rollback()
            return 'Failure'

    elif selection == 'Recapture':
        leaver.result = 'Recapture'
        leaver.leaverrole = suspect.srole
        leaver.leaverfirm = suspect.sfirm
        leaver.link = suspect.slink
        leaver.leaverlocation = suspect.slocation
        leaver.outprosshell = datetime.datetime.now(datetime.timezone.utc)
        leaver.inprosshell = 'No'
        leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        suspect.result = 'Selected'
        suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        try:
            db.session.commit()
            return 'Success'
        except:
            db.session.rollback()
            return 'Failure'

    elif selection == 'Left Industry':
        leaver.result = 'Left Industry'
        leaver.leaverrole = suspect.srole
        leaver.leaverfirm = suspect.sfirm
        leaver.outprosshell = datetime.datetime.now(datetime.timezone.utc)
        leaver.inprosshell = 'No'
        leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        suspect.result = 'Selected'
        suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)

        try:
            db.session.commit()
            return 'Success'
        except:
            db.session.rollback()
            return 'Failure'
