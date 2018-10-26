import pandas as pd
import xlrd
from app.models import Srep, Leaver, Suspect, Buckets
from app import app, db
import os
import datetime
from flask_login import current_user
import bokeh.plotting
from bokeh.embed import components
from sqlalchemy import func
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from index_help import gen_trackalert_table, gen_dropped_table, gen_engagement_table

from bokeh.transform import jitter

######## Bokeh ##############
def create_figure(b_selection, bins):
    leavers = Leaver.query.all()
    df = pd.DataFrame([(d.name, d.result, d.id) for d in leavers],
        columns=['name', 'result', 'id'])
    df = df.groupby('result')['name'].count()
    p = Histogram(df, b_selection, title='Leaver Groups', color='Species',
        bins=bins, legend='top_right', width=600, height=400)

        # Set the x axis label
    p.xaxis.axis_label = b_selection

    # Set the y axis label
    p.yaxis.axis_label = 'Count'
    return p


######## Utilities ##############
# def result(target, field, rez, flag):
#     print('Starting Result Processing...')
#     print('Result Content As Delivered: ')
#     print(target)
#     #print(field)
#     print(rez)
#     print(flag)
#     if rez == 'Recapture' or rez == 'Lead' or rez == 'Left Industry':
#         target.result = rez
#         target.prosrole = target.trackrole
#         target.prosfirm = target.trackfirm
#         target.outprosshell = datetime.datetime.now(datetime.timezone.utc)
#         target.inprosshell = 'No'
#         target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#     elif rez == 'Inactive':
#         target.result = rez
#         target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#     elif rez == 'Tracking':
#         print('Confirmed: ', rez)
#         target.link = flag
#         target.trackend = None
#         target.trackrole = None
#         target.trackfirm = None
#         target.tracklocation = None
#         target.lasttracked = None
#         target.outprosshell = datetime.datetime.now(datetime.timezone.utc)
#         target.result = rez
#         target.inprosshell = 'No'
#         target.trackstart = datetime.datetime.now(datetime.timezone.utc)
#
#     elif rez == 'Engaged':
#         print('Confirmed: ', rez)
#         target.estart = datetime.datetime.now(datetime.timezone.utc)
#         target.result = rez
#
#     elif rez == 'Lost Business':
#         print('Confirmed: ', rez)
#         target.eend = datetime.datetime.now(datetime.timezone.utc)
#         target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#         target.result = rez
#
#     db.session.commit()
#     print('Result Proces Complete')
#     return 'Success'

# def suspect_sort(ident, selection):
#     suspect = Suspect.query.filter_by(id=ident).first()
#     leaver = Leaver.query.filter_by(id=hit.leaverid).first()
#
#     if selection == 'Lead':
#         leaver.leaverrole = suspect.srole
#         leaver.leaverfirm = suspect.sfirm
#         leaver.link = suspect.slink
#         leaver.leaverlocation = suspect.sloaction
#         leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#         leaver.result = 'Lead'
#         leaver.inprosshell = 'No'
#         suspect.result = 'Selected'
#         suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#         try:
#             db.session.commit()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Success', parentdict
#         except:
#             db.session.rollback()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Failure', parentdict
#
#     elif selection == 'Track':
#         leaver.leaverrole = suspect.srole
#         leaver.leaverfirm = suspect.sfirm
#         leaver.link = suspect.slink
#         leaver.leaverlocation = suspect.sloaction
#         leaver.result = 'Tracking'
#         leaver.trackstart = datetime.datetime.now(datetime.timezone.utc)
#         suspect.result = 'Selected'
#         suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#         try:
#             db.session.commit()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Success', parentdict
#         except:
#             db.session.rollback()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Failure', parentdict
#
#     elif selection == 'Recapture':
#         leaver.result = 'Recapture'
#         leaver.prosrole = leaver.trackrole
#         leaver.prosfirm = leaver.trackfirm
#         leaver.outprosshell = datetime.datetime.now(datetime.timezone.utc)
#         leaver.inprosshell = 'No'
#         leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#         suspect.result = 'Selected'
#         suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#         try:
#             db.session.commit()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Success', parentdict
#         except:
#             db.session.rollback()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Failure', parentdict
#
#     elif selection == 'Left Industry':
#         leaver.result = 'Left Industry'
#         leaver.prosrole = leaver.trackrole
#         leaver.prosfirm = leaver.trackfirm
#         leaver.outprosshell = datetime.datetime.now(datetime.timezone.utc)
#         leaver.inprosshell = 'No'
#         leaver.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#         suspect.result = 'Selected'
#         suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#
#         try:
#             db.session.commit()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Success', parentdict
#         except:
#             db.session.rollback()
#             parentdict = {}
#             parentdict['A'] = match_html(id, 1)
#             parentdict['B'] = match_html(id, 2)
#             parentdict['C'] = match_html(id, 4)
#             return 'Failure', parentdict

# def suspect_remove(ident):
#     suspect = Suspect.query.filter_by(id=ident).first()
#     suspect.result = 'Removed'
#     suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
#     lid = suspect.leaverid
#
#     try:
#         db.session.commit()
#         table_html = match_html(lid, 2)
#         return 'Success', parentdict
#     except:
#         db.session.rollback()
#         table_html = match_html(lid, 2)
#         return 'Failure', table_html



######## Index/Homepage HELPERS ##############
#populates placed leavers in table on homepage

# def proslinkgen(num):
#     snum = str(num)
#     fnum = snum[:6]
#     snum = snum[6:]
#     link = 'PROS C ' + fnum + ' ' + snum
#     return link

# def gen_trackalert_table(trackalert_list):
#     ta_headers = str('<thead class="thead-light"><tr><th>ID</th>'
#                 + '<th>Name</th>'
#                 + '<th>Old Role</th>'
#                 + '<th>Old Firm</th>'
#                 + '<th>New Role</th>'
#                 + '<th>New Firm</th>'
#                 + '<th>Location</th>'
#                 + '<th>Link</th>'
#                 + '<th>Alert Date</th>'
#                 + '<th>Actions</th>'
#                 + '</tr></thead><tbody>')
#     table_body = ''
#
#     for item in trackalert_list:
#         table_body += str('<tr><td>'
#         + str(item['leaverid']) + '</td><td>'
#         + str(item['leavername']) + '</td><td>'
#         + str(item['leaverrole']) + '</td><td>'
#         + str(item['leaverfirm']) + '</td><td>'
#         + str(item['trackrole']) + '</td><td class="text"><span>'
#         + str(item['trackfirm']) + '</span></td></div><td>'
#         + str(item['leaverlocation']) + '</td><td><a target="_blank" href="'
#         + str(item['leaverlink']) + ' ">LinkedIn</a></td><td>"'
#         + item['trackend'] + ' "</td><td><div class="dropdown"><div class="btn-group">'
#         + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
#         + 'Action<span class="caret"></span></button>'
#         + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
#         + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
#         + '<li><a class="dropdown-item" href="#">Lead</a></li>'
#         + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
#         + '<li><a class="dropdown-item" href="#">Engaged</a></li>'
#         + '<li><a class="dropdown-item" href="#">Error</a></li></ul></div></div></td></tr>')
#     table_body += '</tbody>'
#     table = ta_headers + table_body
#     return(table)

# def gen_engagement_table(elist):
#     ta_headers = str('<thead class="thead-light"><tr><th>ID</th>'
#                 + '<th>Name</th>'
#                 + '<th>Tracking Role</th>'
#                 + '<th>Tracking Firm</th>'
#                 + '<th>Location</th>'
#                 + '<th>PROS Link</th>'
#                 + '<th>Engagent Duration</th>'
#                 + '<th>Link</th>'
#                 + '<th>Actions</th>'
#                 + '</tr></thead><tbody>')
#     table_body = ''
#
#     for item in elist:
#         table_body += str('<tr><td>'
#         + str(item['eid']) + '</td><td>'
#         + str(item['ename']) + '</td><td>'
#         + str(item['erole']) + '</td><td class="text"><span>'
#         + str(item['efirm']) + '</span></td><td>'
#         + str(item['elocation']) + '</td><td>'
#         + str(item['ePROS']) + '</td><td>'
#         + str(item['eduration']) + '</td><td><a target="_blank" href="'
#         + str(item['elink']) + ' ">LinkedIn</a></td><td>'
#         + '<div class="dropdown"><div class="btn-group">'
#         + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
#         + 'Action<span class="caret"></span></button>'
#         + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
#         + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
#         + '<li><a class="dropdown-item" href="#">Lost Business</a></li>'
#         + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
#         + '<li><a class="dropdown-item" href="#">Manual Track</a></li>'
#         + '<li><a class="dropdown-item" href="#">Inactive</a></li></ul></div></div></td></tr>')
#     table_body += '</tbody>'
#     table = ta_headers + table_body
#     return(table)
#
# def gen_dropped_table(drop_list):
#     drop_headers = str('<thead class="thead-light"><tr>'
#                         + '<th>ID</th>'
#                         + '<th>Name</th>'
#                         + '<th>Role</th>'
#                         + '<th>Firm</th>'
#                         + '<th>PROS Link</th>'
#                         + '<th>Actions</th>'
#                         + '</tr></thead><tbody>')
#     table_body = ''
#     for item in drop_list:
#         table_body += str('<tr><td>'
#         + str(item['leaverid']) + '</td><td>'
#         + str(item['leavername']) + '</td><td>'
#         + str(item['prosrole']) + '</td><td>'
#         + str(item['prosfirm']) + '</div></td><td>'
#         + str(item['proslink']) + ' </td><td><div class="dropdown"><div class="btn-group">'
#         + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
#         + 'Action<span class="caret"></span></button>'
#         + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
#         + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
#         + '<li><a class="dropdown-item" href="#">Lead</a></li>'
#         + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
#         + '<li><a class="dropdown-item" href="#">Engaged</a></li>'
#         + '<li><a class="dropdown-item" href="#">Delayed Trial</a></li>'
#         + '<li><a class="dropdown-item" href="#">Manual Track</a></li>'
#         + '<li><a class="dropdown-item" href="#">Inactive</a></li></ul></div></div></td></tr>')
#     table_body += '</tbody>'
#     table = drop_headers + table_body
#     return(table)

# def delay_delete(ident):
#     print('Starting Delay Delete')
#     try:
#         updated = Leaver.query.filter_by(id=ident).first()
#         print('Leaver Query Confirm: ', updated.name)
#         updated.suspects.delete()
#         Leaver.query.filter_by(id=ident).delete()
#         db.session.commit()
#         return 'Success'
#     except:
#         db.session.rollback()
#         return 'Failure'

# def e_duration(leaver):
#     d1 = leaver.estart.date()
#     d2 = datetime.date.today()
#     return abs((d2 - d1).days)

# def actionfill(flag):
#     parentdict = {}
#     if flag == 'B':
#         TA_dict = {}
#         TA_list = []
#         print('Flag is B')
#         TA_Confirm = Leaver.query.filter_by(result='TrackAlert', repcode=current_user.repcode).all()
#         for l in TA_Confirm:
#             TA_dict = {'leavername': l.name, 'leaverfirm': l.leaverfirm, 'leaverrole': l.leaverrole, 'leaverid': l.id, 'trackend': l.trackend, 'leaverlocation': l.leaverlocation, 'leaverlink': l.link, 'trackfirm': l.trackfirm, 'trackrole': l.trackrole}
#             TA_list.append(TA_dict)
#         ta_table = gen_trackalert_table(TA_list)
#         parentdict['B'] = ta_table
#
#     elif flag == 'A':
#         DROP_dict = {}
#         DROP_list = []
#         print('Flag is A')
#         DROP_Confirm = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
#         for d in DROP_Confirm:
#             DROP_dict = {'leavername': d.name, 'prosfirm': d.prosfirm, 'prosrole': d.prosrole, 'leaverid': d.id, 'proslink': proslinkgen(d.prosnum)}
#             DROP_list.append(DROP_dict)
#         dropped_table = gen_dropped_table(DROP_list)
#         parentdict['A'] = dropped_table
#
#     elif flag == 'C':
#         ENG_dict = {}
#         ENG_list = []
#         print('Flag is C')
#         ENG_Confirm = Leaver.query.filter_by(result='Engaged', repcode=current_user.repcode).all()
#         for e in ENG_Confirm:
#             ENG_dict = {'eduration': e_duration(e), 'ename': e.name, 'efirm': e.trackfirm, 'erole': e.trackrole, 'eid': e.id, 'ePROS': proslinkgen(e.prosnum), 'elocation': e.leaverlocation, 'elink': e.link}
#             ENG_list.append(ENG_dict)
#         e_table = gen_engagement_table(ENG_list)
#         parentdict['C'] = e_table
#
#     elif flag == 'AB':
#         DROP_dict = {}
#         DROP_list = []
#         TA_dict = {}
#         TA_list = []
#         ENG_dict = {}
#         ENG_list = []
#         print('Flag is AB')
#         TA_Confirm = Leaver.query.filter_by(result='TrackAlert', repcode=current_user.repcode).all()
#         DROP_Confirm = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
#         ENG_Confirm = Leaver.query.filter_by(result='Engaged', repcode=current_user.repcode).all()
#
#         for l in TA_Confirm:
#             TA_dict = {'leavername': l.name, 'leaverfirm': l.leaverfirm, 'leaverrole': l.leaverrole, 'leaverid': l.id, 'trackend': l.trackend.date().strftime("%m-%d-%Y"), 'leaverlocation': l.leaverlocation, 'leaverlink': l.link, 'trackfirm': l.trackfirm, 'trackrole': l.trackrole}
#             TA_list.append(TA_dict)
#         ta_table = gen_trackalert_table(TA_list)
#         parentdict['B'] = ta_table
#         for d in DROP_Confirm:
#             # num = d.prosnum
#             # link = proslinkgen(num)
#             DROP_dict = {'leavername': d.name, 'prosfirm': d.prosfirm, 'prosrole': d.prosrole, 'leaverid': d.id, 'proslink': proslinkgen(d.prosnum)}
#             DROP_list.append(DROP_dict)
#         dropped_table = gen_dropped_table(DROP_list)
#         parentdict['A'] = dropped_table
#
#         for e in ENG_Confirm:
#             ENG_dict = {'eduration': e_duration(e), 'ename': e.name, 'efirm': e.trackfirm, 'erole': e.trackrole, 'eid': e.id, 'ePROS': proslinkgen(e.prosnum), 'elocation': e.leaverlocation, 'elink': e.link}
#             ENG_list.append(ENG_dict)
#         e_table = gen_engagement_table(ENG_list)
#         parentdict['C'] = e_table
#
#     return parentdict

def dropfill():
    dropped = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
    parentdict = {}
    placed_dict = {}
    placed_list = []
    for l in dropped:
        num = l.prosnum
        link = proslinkgen(num)
        placed_dict = {'leavername': l.name, 'prosfirm': l.prosfirm, 'prosrole': l.prosrole, 'leaverid': l.id, 'proslink': link}
        placed_list.append(placed_dict)
    parentdict['B'] = placed_list
    return parentdict

# def reset_leaver(id):
#     lvr_id = int(id)
#     reset_lvr = Leaver.query.filter_by(id=lvr_id).first()
#     reset_suspects = Suspect.query.filter_by(leaverid=lvr_id).all()
#     reset_lvr.result = 'Tracking'
#     #reset_lvr.leaverrole = None
#     #reset_lvr.leaverfirm = None
#     #reset_lvr.leaverlocation = None
#     #reset_lvr.link = None
#     reset_lvr.trackrole = None
#     reset_lvr.trackfirm = None
#     reset_lvr.tracklocation = None
#     reset_lvr.lasttracked = None
#     reset_lvr.datetimeresult = None
#     #reset_lvr.suspectcheck = None
#     reset_lvr.trackend = None
#     #for s in reset_suspects:
#         #s.datetimeresult = None
#         #s.result = None
#     db.session.commit()
#     return 'Success'

######## UPLOAD HELPERS ##############
#sets the inpros flag in db to NO to detect those No longer in the LJFT bucket
def inpros():
    existnames = Leaver.query.filter_by(result='Lost').all()
    for n in existnames:
        n.inprosshell = 'No'
    return 'Success'

#adds pros shell and pros contact numbers together
def concat(a, b):
    return int(f"{a}{b}")

#translates excel file to pandas df passing rows to pd2class
def processfile(file):
    data_xls = pd.read_excel(file, header=0, names=['prosshell#','proscontact#','first','last','repcode','teamcode','role','firm'])
    data_xls['repcode'] = 'JBUH'
    data_xls['teamcode'] = 'HF3'
    try:
        data_xls["name"] = data_xls["first"] + ' ' + data_xls["last"]
        data_xls = data_xls.drop('first', 1)
        data_xls= data_xls.drop('last', 1)
        data_xls.fillna(' ', inplace=True)
        data_xls.apply(pd2class, axis=1)
        return 'Success'
    except:
        print('Failed to Read SpreadSheet. Please Check Columns')
        return 'Failure'

#adds NEW leavers to database from pandas df
def pd2class(row):
    number = concat(row['prosshell#'], row['proscontact#'])
    number = int(number)
    exists = Leaver.query.filter_by(prosnum=number).first()
    if exists:
        exists.inprosshell = 'Yes'
        print('duplicate detected. Skipping: ', row['name'])
        db.session.commit()
    else:
        l = Leaver(prosnum=number, name=row['name'], repcode=row['repcode'], teamcode=row['teamcode'], prosfirm=row['firm'], prosrole=row['role'], inprosshell='Yes')
        print('Adding Leaver to DB: ', l.name)
        db.session.add(l)
        db.session.commit()

def exitpros():
    newdrop = Leaver.query.filter_by(inprosshell='No').all()
    for n in newdrop:
        if n.outprosshell == None:
            n.outprosshell = datetime.datetime.now(datetime.timezone.utc)
    db.session.commit()
    return 'Success'
####### Match HELPERS ############
#populates the dropdown on track page with leavers. selection triggers tablefill
# def fillselect(leavers):
#
#     return leaver_dict
def populate_table():
    return None


# def match_html(id, flag):
#     # HTML for the Card on match.html
#     if flag == 2:
#         l = Leaver.query.filter_by(id=id).first()
#         html = str('<div id="PROS"><div class="card-body"><div class="text-center"><h5 class="card-title">PROS Record</h5><ul class="list-inline"><li class="list-inline-item list-group-item-primary">Name: '
#         + str(l.name) + '<li class="list-inline-item list-group-item-dark">Role: '
#         + str(l.prosrole) + '<li class="list-inline-item list-group-item-primary">Firm: '
#         + str(l.prosfirm) + '<li class="list-inline-item list-group-item-dark">Date Added: '
#         + str(l.datetimeadded.date().strftime('%m/%d/%Y')) + '</li></ul></div></div>')
#
#         print('HTML to Match Card: ', html)
#         return html
#
#     elif flag == 3:
#         #HTML for Match Table
#         susp_list = []
#         suspects = Suspect.query.filter_by(leaverid=id, result=None).all()
#         html = '<thead class="thead-light"><tr><th>ID</th><th>Name</th><th>Role</th><th>Firm</th><th>Location</th><th>Link</th><th>Action</th></tr></thead><tbody>'
#         for l in suspects:
#             html += str('<tr><td>'
#             + str(l.id) + '</td><td>'
#             + str(l.name) + '</td><td>'
#             + str(l.srole) + '</td><td class="text"><span>'
#             + str(l.sfirm) + '</span></td><td>'
#             + str(l.slocation) + '</td><td><a target="_blank" href="'
#             + str(l.slink) + ' ">LinkedIn</a></td><td><div class="dropdown"><div class="btn-group">'
#             + '<button class="btn btn-sm btn-primary dropdown-toggle" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
#             + 'Action<span class="caret"></span></button>'
#             + '<ul class="dropdown-menu" aria-labelledby="dropdownMenu">'
#             + '<li><a class="dropdown-item" href="#">Lead</a></li>'
#             + '<li><a class="dropdown-item" href="#">Track</a></li>'
#             + '<li><a class="dropdown-item" href="#">Recapture</a></li>'
#             + '<li><a class="dropdown-item" href="#">Left Industry</a></li>'
#             + '<li><a class="dropdown-item" href="#">Remove</a></li></ul></div></div></td></tr>')
#         html += '</tbody>'
#
#         print('HTML to Match Table: ', html)
#         return html
#
#     elif flag == 1:
#         leavers = Leaver.query.filter_by(repcode=current_user.repcode, inprosshell='Yes', result='Lost').all()
#         leaver_dict = []
#         drop_html = '<option value="">Select Leaver</option>'
#         for l in leavers:
#             suspects = Suspect.query.filter_by(leaverid=l.id, result=None).all()
#             num = len(suspects)
#             if num > 0:
#                 dval = l.name + ' ' + '(' + str(num) + ')'
#                 s_dict = {'ident': l.id, 'name': dval}
#                 drop_html += '<option value="' + str(l.id) + '">' + dval + '</option>'
#         print('HTML to DropDown: ', drop_html)
#         return drop_html

#populates dictionary for suspect table on fillselect selection AND comparison card
# def pop_match_card(thing):
#     flag = 'match_table'
#
#     card_html = match_html(leaverdict, 'card')
#     return card_html
#
# def pop_match_table(thing):
#     flag = 'match_table'
#
#     for s in suspects:
#         s_dict = {'ident': s.id, 'name': s.name, 'link': s.slink, 'role': s.srole, 'firm':s.sfirm, 'location': s.slocation}
#         susp_list.append(s_dict)
#     card_html, table_html = gen_card_html(leaverdict)
#     parentdict['A'] = leaverdict
#     parentdict['B'] = susp_list
#     return parentdict

def role_score(t):
    if t.prosrole == None:
        score = 4
    elif 'Executive' in t.prosrole or 'Cheif' in t.prosrole:
        score = 10
    elif t.prosrole == 'Portfolio Manager':
        score = 9
    elif t.prosrole == 'Quant':
        score = 8
    elif t.prosrole == 'Trader':
        score = 7
    elif 'Risk' in t.prosrole:
        score = 6
    elif t.prosrole == 'Analyst':
        score = 5
    elif t.prosrole == 'Economist':
        score = 4
    elif 'Back' or 'Middle' in t.prosrole:
        score = 3
    else:
        score = 4
    return score

def day_count(t):
    if t.result == 'Tracking':
        today = datetime.date.today()
        start = t.trackstart.date()
        days = abs((today - start).days)
    elif t.result == 'Recapture':
        start = t.datetimeadded.date()
        end = t.datetimeresult.date()
        days = abs((end - start).days)
    elif t.result == 'Engaged':
        today = datetime.date.today()
        start = t.estart.date()
        days = abs((today - start).days)
    return days

def e_length(t):
    today = datetime.date.today()
    last = t.elast.date()
    days = abs((today - last).days)
    return days

def cscore(e):
    if e.result == 'Tracking':
        score = 1
    elif e.result == 'Recapture':
        score = 2
    elif e.result == 'Engaged':
        score = 3
    return score

def chart_data(type):
    data = {}
    if type == 'doughnut':
        print('getting data for doughnut chart')
        result_list = []
        count_list = []
        for result, count in db.session.query(Leaver.result, func.count(Leaver.id)).group_by(Leaver.result).all():
            print('Users status %s: %d' % (result, count))
            result_list.append(result)
            count_list.append(count)
        data['labels'] = result_list
        data['datasets'] = count_list
        return data

    elif type == 'rezbar':
        print('getting data for result chart')
        data = {}
        df = pd.read_sql(db.session.query(Buckets).statement,db.session.bind)
        df.date = df.date.apply(lambda x: str(x).split(' ')[0])
        accountedfor = df.loc[df['status'].isin(['Tracking','Engaged'])]
        unaccountedfor = df.loc[df['status'].isin(['Lost','Inactive'])]
        act4 = accountedfor.groupby('date', as_index=False)['count'].sum()
        unact4 = unaccountedfor.groupby('date', as_index=False)['count'].sum()
        final = pd.merge(act4, unact4, on='date')
        final = final.rename(index=str, columns={"count_x": "Accounted", "count_y": "Unaccounted"})
        final['%Accounted'] = round((final['Accounted'] / (final['Accounted'] + final['Unaccounted'])) * 100)
        print('dataframe: ', final)

        datasets = []
        actlist = []
        uactlist = []
        dt_list = []
        pct_list = []
        for index, row in final.iterrows():
            actlist.append(row['Accounted'])
            uactlist.append(row['Unaccounted'])
            dt_list.append(row['date'])
            pct_list.append(row['%Accounted'])
        dct_a = {}
        dct_b = {}
        dct_c = {}

        dct_c['type'] = 'line'
        dct_c['data'] = pct_list
        dct_c['label'] = '% Accounted For'
        dct_c['borderColor'] = "#FFFF00"
        dct_c['yAxisID'] = "y-axis-2"
        dct_c['fill'] = False

        dct_a['label'] = 'Accounted For'
        dct_a['data'] = actlist
        dct_a['backgroundColor'] = "#3e95cd"
        dct_a['yAxisID'] = "y-axis-1"

        dct_b['label'] = 'Unaccounted For'
        dct_b['data'] = uactlist
        dct_b['backgroundColor'] = "#085b83"
        dct_b['yAxisID'] = "y-axis-1"


        datasets.append(dct_c)
        datasets.append(dct_a)
        datasets.append(dct_b)



        data['datasets'] = datasets
        data['labels'] = dt_list
        print('result chart data: ', data)
        return data

    elif type == 'stackedbar':
        print('getting data for bar chart')
        data = {}
        df = pd.read_sql(db.session.query(Buckets).statement,db.session.bind)
        df.date = df.date.apply(lambda x: str(x).split(' ')[0])
        dates = df.date.unique()
        dt_list = []
        for d in dates:
            dt_list.append(d)
        data['labels'] = dt_list

        label_list = []
        print('Bar Stacks:')
        for l in df.status.unique():
            print(l)
            label_list.append(l)
        list_data = []
        for l in label_list:
            d = {}
            members = db.session.query(Buckets).filter_by(status=l).all()
            values = []
            for m in members:
                values.append(m.count)
            d['set'] = [m.status, values]
            list_data.append(d)

        data['datasets'] = []
        for i in list_data:
            j = {}
            j['label'] = i['set'][0]
            j['data'] = i['set'][1]
            data['datasets'].append(j)

        colors = ["#3e95cd", "#e8c3b9", "#3cba9f", "#8e5ea2", "#3e95cd", "#c45850", "#5e4fa2", '#D6E9C6', "#085b83"]
        i = 0
        while i < len(data['datasets']):
            data['datasets'][i]['backgroundColor'] = colors[i]
            i += 1
        #print('Bar Chart Data: ', data)
        return data

    elif type == 'scatter':
        print('Generating BubblePlot Data')
        trck = Leaver.query.filter_by(result='Tracking').all()
        rcpt = Leaver.query.filter_by(result='Recapture').all()
        engd = Leaver.query.filter_by(result='Engaged').all()

        print('Lengths:')
        print(len(trck))
        print(len(rcpt))
        print(len(engd))

        dlst = []

        for t in trck:
            d={}
            #d['name'] = t.name
            #d['id'] = t.id
            d['y'] = cscore(t)
            d['x'] = day_count(t)
            d['r'] = role_score(t)
            #d['r'] = t.result
            dlst.append(d)
        for r in rcpt:
            d={}
            #d['name'] = r.name
            #d['id'] = r.id
            d['y'] = cscore(r)
            d['x'] = day_count(r)
            d['r'] = role_score(r)
            #d['r'] = r.result
            dlst.append(d)
        for e in engd:
            d={}
            #d['name'] = r.name
            #d['id'] = r.id
            d['y'] = cscore(e)
            d['x'] = day_count(e)
            d['r'] = role_score(e)
            #d['r'] = e.result
            dlst.append(d)

        print('dlst: ', dlst)
        # bcd = {}
        # bcd['yLabels'] = ['Test', 'Tracking', 'Recapture', 'Engaged']
        # bcd['datasets'] = []
        # dct = {}
        # dct['data'] = dlst
        # bcd['datasets'].append(dct)
        # print('final bubble data: ', bcd)
        return dlst

    elif type == 'engage':
        engd = Leaver.query.filter_by(result='Engaged').all()
        print(len(engd))

        dlst = []

        for e in engd:
            if e.elast == None:
                pass
            else:
                d={}
                #d['name'] = r.name
                #d['id'] = r.id
                d['y'] = 2
                d['x'] = e_length(e)
                d['r'] = role_score(e)
                #d['r'] = e.result
                dlst.append(d)
        return dlst
