from flask import render_template, flash, redirect, url_for, request, json, Flask, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Leaver, Suspect, Srep
from sqlalchemy import DateTime
from werkzeug.urls import url_parse
from helpers import processfile, pd2class, inpros, fillselect, populate_table, actionfill, dropfill, result
import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')

#populates initial table on homepage
@app.route('/actionitems', methods=['GET', 'POST'])
@login_required
def actionitems():
    action_dict = actionfill()
    return json.dumps(action_dict)

#populates initial table on homepage
@app.route('/dropitems', methods=['GET', 'POST'])
@login_required
def dropitems():
    drop_dict = dropfill()
    return json.dumps(drop_dict)

#homepage 'Confirm' button posts here after user updates 'placed' users in PROS
@app.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    prosid = request.args.get( 'data', '', type = int )
    action_type = request.args.get( 'action', '')
    if action_type == 'Lead':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill()
        return json.dumps(placed_dict)
    elif action_type == 'Placed':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill()
        return json.dumps(placed_dict)
    elif action_type == 'Left_Industry':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill()
        return json.dumps(placed_dict)
    else:
        placed_dict = actionfill()
        return json.dumps(placed_dict)

@app.route('/cleanup', methods=['GET', 'POST'])
@login_required
def cleanup():
    prosid = request.args.get( 'data', '', type = int )
    action_type = request.args.get( 'action', '')
    if action_type == 'Placed':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = dropfill()
        return json.dumps(placed_dict)
    elif action_type == 'Left_Industry':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = dropfill()
        return json.dumps(placed_dict)
    elif action_type == 'Inactive':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = dropfill()
        return json.dumps(placed_dict)
    else:
        print('!Something Went Wrong with cleanup..!')
        placed_dict = dropfill()
        return json.dumps(placed_dict)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        print('file uploaded: ', f)
        prosu = inpros()
        rez = processfile(f)
        if rez == "Success" and prosu == 'Success':
            return redirect(url_for('match'))

    return render_template('upload.html', title='Upload XLSX File')

@app.route('/match', methods=['GET', 'POST'])
@login_required
def match():

    return render_template('match.html', title='Match')

@app.route('/ndrop', methods=['GET', 'POST'])
@login_required
def ndrop():
    leavers = Leaver.query.filter_by(repcode=current_user.repcode, inprosshell='Yes', result='Lost').all()
    leaver_dict = fillselect(leavers)
    return json.dumps(leaver_dict)

#populates suspect table on leaver selection from dropdown
@app.route('/ajax', methods=['POST', 'GET'])
@login_required
def ajax():
    thing = request.args.get( 'data', '', type = int )
    parentdict = populate_table(thing)
    return json.dumps(parentdict)

#changes leaver status to Tracking on 'follow' button click (on table)
@app.route('/leadclick', methods=['GET', 'POST'])
@login_required
def leadclick():
    ident = request.args.get( 'data', '', type = int )
    hit = Suspect.query.filter_by(id=ident).first()
    lhit = Leaver.query.filter_by(id=hit.leaverid).first()
    lhit.leaverrole = hit.srole
    lhit.leaverfirm = hit.sfirm
    lhit.link = hit.slink
    lhit.leaverlocation = hit.slocation
    lhit.result = 'Lead'
    lhit.inprosshell = 'No'
    hit.result = 'Selected'
    hit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    #.isoformat()
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result=None).all()
    leaver_dict = fillselect(leavers)
    return json.dumps(leaver_dict)

@app.route('/trackclick', methods=['GET', 'POST'])
@login_required
def trackclick():
    ident = request.args.get( 'data', '', type = int )
    print('confirming ident capture: ', ident)
    hit = Suspect.query.filter_by(id=ident).first()
    print('confirming suspect ident match: ', hit.name)
    lhit = Leaver.query.filter_by(id=hit.leaverid).first()
    print('confirming leaver suspect match: ', lhit.name)
    lhit.leaverrole = hit.srole
    lhit.leaverfirm = hit.sfirm
    lhit.link = hit.slink
    lhit.leaverlocation = hit.slocation
    lhit.result = 'Tracking'
    hit.result = 'Selected'
    hit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result='Lost', inprosshell='Yes').all()
    leaver_dict = fillselect(leavers)

    return json.dumps(leaver_dict)
#changes leaver status to placed and reloads dropdown
@app.route('/placeclick', methods=['GET', 'POST'])
@login_required
def placeclick():
    ident = request.args.get( 'data', '', type = int )
    hit = Suspect.query.filter_by(id=ident).first()
    lhit = Leaver.query.filter_by(id=hit.leaverid).first()
    lhit.leaverrole = hit.srole
    lhit.leaverfirm = hit.sfirm
    lhit.link = hit.slink
    lhit.leaverlocation = hit.slocation
    lhit.status = 'Placed'
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result='Lost').all()
    leaver_dict = fillselect(leavers)
    return json.dumps(leaver_dict)

#deletes suspect from possible matches for a given leaver
@app.route('/removeclick', methods=['GET', 'POST'])
@login_required
def removeclick():
    ident = request.args.get( 'data', '', type = int )
    suspect = Suspect.query.filter_by(id=ident).first()
    suspect.result = 'Removed'
    suspect.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    db.session.commit()

    lid = suspect.leaverid
    suspect_dict = []
    suspects = Suspect.query.filter_by(leaverid=lid, result=None).all()

    print('checking suspects: removeclick...')
    for s in suspects:
        print('name: ', s.name)
        print('result: ', s.result)
    for s in suspects:
        s_dict = {'ident': s.id, 'name': s.name, 'link': s.slink, 'role': s.srole, 'firm':s.sfirm, 'location': s.slocation}
        suspect_dict.append(s_dict)
    return json.dumps(suspect_dict)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.repcode.data, form.remember_me.data))
        user = Srep.query.filter_by(repcode=form.repcode.data).first()
        if user is None:
            flash('Invalid RepCode or TeamCode')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegistrationForm()

    if request.method == 'POST':
        print(regform.errors)
        print(regform.validate_on_submit())
        print('post')
        print(regform.firstname.data)
        if regform.validate_on_submit():
            print('valid form')
            fname = regform.firstname.data + ' ' + regform.lastname.data
            print(fname)
            newsrep = Srep(name=fname, email=regform.email.data, repcode=regform.repcode.data, teamcode=regform.teamcode.data)
            print('name: ', newsrep.name)
            db.session.add(newsrep)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=regform)
