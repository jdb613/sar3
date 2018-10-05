from flask import render_template, flash, redirect, url_for, request, json, Flask, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, BokehForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Leaver, Suspect, Srep
from sqlalchemy import DateTime
from werkzeug.urls import url_parse
from helpers import processfile, pd2class, inpros, fillselect, populate_table, actionfill, dropfill, reset_leaver, create_figure, exitpros, chart_data, delay_delete
from helpers import result
import datetime
import pandas as pd
from collections import Counter
from math import pi
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')

#populates initial table on homepage
@app.route('/actionitems', methods=['GET', 'POST'])
@login_required
def actionitems():
    action_dict = actionfill('AB')
    return json.dumps(action_dict)

#homepage 'Confirm' button posts here after user updates 'placed' users in PROS
@app.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    prosid = request.args.get( 'id', '', type = int )
    action_type = request.args.get( 'selection', '')
    table = request.args.get( 'table', '')
    link = request.args.get( 'link', '')
    print('Action Type Sent to Confirm Route: ', action_type)
    print('Table to Adjust: ', table)
    print('ID of Leaver to be Updated: ', prosid)
    print('Link -If Relevant-', link)

    if table == 'LEADtable':

        if action_type == 'Error':
            reset_result = reset_leaver(prosid)
            print('Reset Leaver Result: ', reset_result)
            placed_dict = actionfill('B')
            return json.dumps(placed_dict)
        else:
            iprosid = int(prosid)
            updated = Leaver.query.filter_by(id=iprosid).first()
            db_upd = result(updated, 'result', action_type, 'Y')
            print('Changed Result Field to Lead: ', db_upd)
            placed_dict = actionfill('B')
            return json.dumps(placed_dict)

    elif table == 'DROPtable':

        if action_type == 'Manual Track':
            iprosid = int(prosid)
            updated = Leaver.query.filter_by(id=iprosid).first()
            db_upd = result(updated, 'result', 'Tracking', link)
            print('Manually Tracking: ', db_upd)
            placed_dict = actionfill('A')
            return json.dumps(placed_dict)

        elif action_type == 'Delayed Trial':
            iprosid = int(prosid)
            rslt = delay_delete(iprosid)
            print('%s in Deleting User and Suspect' %(rslt))

            placed_dict = actionfill('A')
            return json.dumps(placed_dict)

        else:
            iprosid = int(prosid)
            updated = Leaver.query.filter_by(id=iprosid).first()
            print('Leaver Query Confirm: ', updated.name)
            db_upd = result(updated, "r", action_type, 'Y')
            print('DB Addition Result: ', db_upd)
            placed_dict = actionfill('A')
            return json.dumps(placed_dict)


    elif table == 'ENGAGEtable':

        if action_type == 'Manual Track':
            iprosid = int(prosid)
            updated = Leaver.query.filter_by(id=iprosid).first()
            db_upd = result(updated, 'result', 'Tracking', link)
            print('Manually Tracking: ', db_upd)
            placed_dict = actionfill('C')
            return json.dumps(placed_dict)

        else:
            iprosid = int(prosid)
            updated = Leaver.query.filter_by(id=iprosid).first()
            db_upd = result(updated, 'result', action_type, 'Y')
            print('DB Addition Result: ', db_upd)
            placed_dict = actionfill('C')
            return json.dumps(placed_dict)

    else:
        print('Something Went Wrong With confirm()')
        placed_dict = actionfill('AB')
        return json.dumps(placed_dict)

@app.route('/dropclick', methods=['GET', 'POST'])
@login_required
def dropclick():
    prosid = request.args.get( 'data', '', type = int )
    action_type = request.args.get( 'action', '')
    print(action_type)
    try:
        mlink = request.args.get( 'lnk', '')
    except:
        pass
    if action_type == 'Recapture':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)

    elif action_type == 'Lead':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)

    elif action_type == 'mtrack':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', 'Tracking', mlink)
        print('Manually Tracking: ', mlink)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)

    elif action_type == 'Left Industry':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)

    elif action_type == 'Inactive':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
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
            db.session.commit()
            exit = exitpros()
            print('Status of outprosshell update: ', exit)
            return redirect(url_for('match'))
        else:
            flash('Excel Upload Failed. Please Check Fields.')
            db.session.rollback()
            return redirect(url_for('upload'))

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
    lhit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    lhit.result = 'Lead'
    lhit.inprosshell = 'No'
    hit.result = 'Selected'
    hit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    #.isoformat()
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result='Lost', inprosshell='Yes').all()
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
    lhit.trackstart = datetime.datetime.now(datetime.timezone.utc)
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
    lhit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    lhit.result = 'Recapture'
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result='Lost', inprosshell='Yes').all()
    leaver_dict = fillselect(leavers)
    return json.dumps(leaver_dict)

@app.route('/repclick', methods=['GET', 'POST'])
@login_required
def repclick():
    ident = request.args.get( 'data', '', type = int )
    hit = Suspect.query.filter_by(id=ident).first()
    lhit = Leaver.query.filter_by(id=hit.leaverid).first()
    lhit.leaverrole = hit.srole
    lhit.leaverfirm = hit.sfirm
    lhit.link = hit.slink
    lhit.leaverlocation = hit.slocation
    lhit.datetimeresult = datetime.datetime.now(datetime.timezone.utc)
    lhit.result = 'Left Industry'
    db.session.commit()

    leavers = Leaver.query.filter_by(repcode=current_user.repcode, result='Lost', inprosshell='Yes').all()
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


@app.route('/charts')
@login_required
def charts():

    return render_template('charts.html', title='Charts')


@app.route('/chartgenerator', methods=['GET', 'POST'])
def chartgenerator():
    if request.method == 'POST':
        action_type = request.args.get( 'data', '')
        chartdata = chart_data(action_type)

    chartdata = {}
    chartdata1 = chart_data('doughnut')
    chartdata2 = chart_data('stackedbar')
    chartdata['A']= chartdata1
    chartdata['B']= chartdata2


    return json.dumps(chartdata)


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
