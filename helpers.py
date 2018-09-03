import pandas as pd
import xlrd
from app.models import Srep, Leaver, Suspect
from app import db
import os
import datetime
from flask_login import current_user

######## Utilities ##############
def result(target, field, rez, flag):
    if field == 'result':
        target.result = rez
    if flag == 'Y':
        target.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    db.session.commit()
    return 'Success'

######## Index/Homepage HELPERS ##############
#populates placed leavers in table on homepage
def proslinkgen(num):
    snum = str(num)
    fnum = snum[:6]
    snum = snum[6:]
    link = 'PROS C ' + fnum + ' ' + snum
    return link

def actionfill(flag):
    parentdict = {}
    DROP_dict = {}
    DROP_list = []
    TA_dict = {}
    TA_list = []
    if flag == 'B':
        print('Flag is B')
        TA_Confirm = Leaver.query.filter_by(result='TrackAlert', repcode=current_user.repcode).all()
        for l in TA_Confirm:
            TA_dict = {'leavername': l.name, 'leaverfirm': l.leaverfirm, 'leaverrole': l.leaverrole, 'leaverid': l.id, 'datetimeresult': l.datetimeresult, 'leaverlocation': l.leaverlocation, 'leaverlink': l.link, 'trackfirm': l.trackfirm, 'trackrole': l.trackrole}
            TA_list.append(TA_dict)
        parentdict['B'] = TA_list

    elif flag == 'A':
        print('Flag is A')
        DROP_Confirm = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
        for d in DROP_Confirm:
            num = d.prosnum
            link = proslinkgen(num)
            DROP_dict = {'leavername': l.name, 'prosfirm': l.prosfirm, 'prosrole': l.prosrole, 'leaverid': l.id, 'proslink': link}
            DROP_list.append(DROP_dict)
        parentdict['A'] = DROP_list

    elif flag == 'AB':
        print('Flag is AB')
        TA_Confirm = Leaver.query.filter_by(result='TrackAlert', repcode=current_user.repcode).all()
        print('Number of TrackAlert Leavers: ', len(TA_Confirm))
        DROP_Confirm = Leaver.query.filter_by(inprosshell='No', result='Lost', repcode=current_user.repcode).all()
        print('Number of Dropped Leavers: ', len(DROP_Confirm))
        for i in DROP_Confirm:
            print('DropConfirm Name: ', i.name)
        for l in TA_Confirm:
            TA_dict = {'leavername': l.name, 'leaverfirm': l.leaverfirm, 'leaverrole': l.leaverrole, 'leaverid': l.id, 'datetimeresult': l.datetimeresult, 'leaverlocation': l.leaverlocation, 'leaverlink': l.link, 'trackfirm': l.trackfirm, 'trackrole': l.trackrole}
            TA_list.append(TA_dict)
        parentdict['B'] = TA_list
        for d in DROP_Confirm:
            num = d.prosnum
            link = proslinkgen(num)
            DROP_dict = {'leavername': d.name, 'prosfirm': d.prosfirm, 'prosrole': d.prosrole, 'leaverid': d.id, 'proslink': d.link}
            DROP_list.append(DROP_dict)
        parentdict['A'] = DROP_list
    print('A', parentdict['A'])
    print('B', parentdict['B'])
    return parentdict

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

def reset_leaver(id):
    lvr_id = int(id)
    reset_lvr = Leaver.query.filter_by(id=lvr_id).first()
    reset_suspects = Suspect.query.filter_by(leaverid=lvr_id).all()
    reset_lvr.result = 'Lost'
    reset_lvr.leaverrole = None
    reset_lvr.leaverfirm = None
    reset_lvr.leaverlocation = None
    reset_lvr.link = None
    reset_lvr.trackrole = None
    reset_lvr.trackfirm = None
    reset_lvr.tracklocation = None
    reset_lvr.lasttracked = None
    reset_lvr.datetimeresult = None
    reset_lvr.suspectcheck = None
    for s in reset_suspects:
        s.datetimeresult = None
        s.result = None
    db.session.commit()
    return 'Success'

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
    data_xls = pd.read_excel(file)
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


####### Match HELPERS ############
#populates the dropdown on track page with leavers. selection triggers tablefill
def fillselect(leavers):
    leaver_dict = []

    for l in leavers:
        suspects = Suspect.query.filter_by(leaverid=l.id, result=None).all()
        num = len(suspects)
        if num > 0:
            dval = l.name + ' ' + '(' + str(num) + ')'
            s_dict = {'ident': l.id, 'name': dval}
            leaver_dict.append(s_dict)
    return leaver_dict


#populates dictionary for suspect table on fillselect selection AND comparison card
def populate_table(thing):
    l = Leaver.query.filter_by(id=thing).first()
    ddate = l.datetimeadded.date().strftime('%m/%d/%Y')
    parentdict = {}
    susp_list = []
    leaverdict = {'leavername': l.name, 'leaverfirm': l.prosfirm, 'leaverrole': l.prosrole, 'leavertime': ddate}
    suspects = Suspect.query.filter_by(leaverid=thing, result=None).all()
    for s in suspects:
        s_dict = {'ident': s.id, 'name': s.name, 'link': s.slink, 'role': s.srole, 'firm':s.sfirm, 'location': s.slocation}
        susp_list.append(s_dict)
    parentdict['A'] = leaverdict
    parentdict['B'] = susp_list
    return parentdict
