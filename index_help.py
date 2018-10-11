from sqlalchemy import func
from app.models import Srep, Leaver, Suspect, Buckets
from app import app, db
from flask_login import current_user
import os
import datetime

def gen_trackalert_table(trackalert_list):
    ta_headers = str('<thead class="thead-light"><tr><th>ID</th>'
                + '<th>Name</th>'
                + '<th>Old Role</th>'
                + '<th>Old Firm</th>'
                + '<th>New Role</th>'
                + '<th>New Firm</th>'
                + '<th>Location</th>'
                + '<th>Link</th>'
                + '<th>Alert Date</th>'
                + '<th>Actions</th>'
                + '</tr></thead><tbody>')
    table_body = ''

    for item in trackalert_list:
        table_body += str('<tr><td>'
        + str(item['leaverid']) + '</td><td>'
        + str(item['leavername']) + '</td><td>'
        + str(item['leaverrole']) + '</td><td>'
        + str(item['leaverfirm']) + '</td><td>'
        + str(item['trackrole']) + '</td><td class="text"><span>'
        + str(item['trackfirm']) + '</span></td></div><td>'
        + str(item['leaverlocation']) + '</td><td><a target="_blank" href="'
        + str(item['leaverlink']) + ' ">LinkedIn</a></td><td>"'
        + str(item['trackend']) + ' "</td><td><div class="dropdown"><div class="btn-group">'
        + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
        + 'Action<span class="caret"></span></button>'
        + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
        + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
        + '<li><a class="dropdown-item" href="#">Lead</a></li>'
        + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
        + '<li><a class="dropdown-item" href="#">Engaged</a></li>'
        + '<li><a class="dropdown-item" href="#">Error</a></li></ul></div></div></td></tr>')
    table_body += '</tbody>'
    table = ta_headers + table_body
    return(table)

def gen_dropped_table(drop_list):
    drop_headers = str('<thead class="thead-light"><tr>'
                        + '<th>ID</th>'
                        + '<th>Name</th>'
                        + '<th>Role</th>'
                        + '<th>Firm</th>'
                        + '<th>PROS Link</th>'
                        + '<th>Actions</th>'
                        + '</tr></thead><tbody>')
    table_body = ''
    for item in drop_list:
        table_body += str('<tr><td>'
        + str(item['leaverid']) + '</td><td>'
        + str(item['leavername']) + '</td><td>'
        + str(item['prosrole']) + '</td><td>'
        + str(item['prosfirm']) + '</div></td><td>'
        + str(item['proslink']) + ' </td><td><div class="dropdown"><div class="btn-group">'
        + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
        + 'Action<span class="caret"></span></button>'
        + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
        + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
        + '<li><a class="dropdown-item" href="#">Lead</a></li>'
        + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
        + '<li><a class="dropdown-item" href="#">Engaged</a></li>'
        + '<li><a class="dropdown-item" href="#">Delayed Trial</a></li>'
        + '<li><a class="dropdown-item" href="#">Manual Track</a></li>'
        + '<li><a class="dropdown-item" href="#">Inactive</a></li></ul></div></div></td></tr>')
    table_body += '</tbody>'
    table = drop_headers + table_body
    return(table)

def gen_engagement_table(elist):
    ta_headers = str('<thead class="thead-light"><tr><th>ID</th>'
                + '<th>Name</th>'
                + '<th>Tracking Role</th>'
                + '<th>Tracking Firm</th>'
                + '<th>Location</th>'
                + '<th>PROS Link</th>'
                + '<th>Engagent Duration</th>'
                + '<th>Link</th>'
                + '<th>Actions</th>'
                + '</tr></thead><tbody>')
    table_body = ''

    for item in elist:
        table_body += str('<tr><td>'
        + str(item['eid']) + '</td><td>'
        + str(item['ename']) + '</td><td>'
        + str(item['erole']) + '</td><td class="text"><span>'
        + str(item['efirm']) + '</span></td><td>'
        + str(item['elocation']) + '</td><td>'
        + str(item['ePROS']) + '</td><td>'
        + str(item['eduration']) + '</td><td><a target="_blank" href="'
        + str(item['elink']) + ' ">LinkedIn</a></td><td>'
        + '<div class="dropdown"><div class="btn-group">'
        + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
        + 'Action<span class="caret"></span></button>'
        + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
        + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
        '<li><a class="dropdown-item" href="#">Last Touch Date</a></li>'
        + '<li><a class="dropdown-item" href="#">Lost Business</a></li>'
        + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
        + '<li><a class="dropdown-item" href="#">Delayed Trial</a></li>'
        + '<li><a class="dropdown-item" href="#">Manual Track</a></li>'
        + '<li><a class="dropdown-item" href="#">Inactive</a></li></ul></div></div></td></tr>')
    table_body += '</tbody>'
    table = ta_headers + table_body
    return(table)
def track_fill():
    TA_dict = {}
    TA_list = []
    TA_Confirm = Leaver.query.filter_by(result='TrackAlert', repcode=current_user.repcode).all()
    for l in TA_Confirm:
        TA_dict = {'leavername': l.name, 'leaverfirm': l.leaverfirm, 'leaverrole': l.leaverrole, 'leaverid': l.id, 'trackend': l.trackend.date().strftime('%m-%d-%y'), 'leaverlocation': l.leaverlocation, 'leaverlink': l.link, 'trackfirm': l.trackfirm, 'trackrole': l.trackrole}
        TA_list.append(TA_dict)
    ta_table = gen_trackalert_table(TA_list)
    return ta_table

def drop_fill():
    DROP_dict = {}
    DROP_list = []
    DROP_Confirm = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
    for d in DROP_Confirm:
        DROP_dict = {'leavername': d.name, 'prosfirm': d.prosfirm, 'prosrole': d.prosrole, 'leaverid': d.id, 'proslink': proslinkgen(d.prosnum)}
        DROP_list.append(DROP_dict)
    dropped_table = gen_dropped_table(DROP_list)
    return dropped_table

def engage_fill():
    ENG_dict = {}
    ENG_list = []
    ENG_Confirm = Leaver.query.filter_by(result='Engaged', repcode=current_user.repcode).all()
    for e in ENG_Confirm:
        ENG_dict = {'eduration': e_duration(e), 'ename': e.name, 'efirm': e.trackfirm, 'erole': e.trackrole, 'eid': e.id, 'ePROS': proslinkgen(e.prosnum), 'elocation': e.leaverlocation, 'elink': e.link}
        ENG_list.append(ENG_dict)
    e_table = gen_engagement_table(ENG_list)
    return e_table

def e_duration(leaver):
    d1 = leaver.estart.date()
    d2 = datetime.date.today()
    return abs((d2 - d1).days)

def proslinkgen(num):
    snum = str(num)
    fnum = snum[:6]
    snum = snum[6:]
    link = 'PROS C ' + fnum + ' ' + snum
    return link
