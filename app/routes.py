from flask import render_template, flash, redirect, url_for, request, json, Flask, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, BokehForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Leaver, Suspect, Srep
from sqlalchemy import DateTime
from werkzeug.urls import url_parse
from helpers import processfile, pd2class, inpros, populate_table, dropfill, create_figure, exitpros, chart_data
from match_help import match_html, suspect_remove, suspect_sort
from confirm_help import indx_tbls_update
from index_help import track_fill, drop_fill, engage_fill
#from helpers import fillselect, actionfill, delay_delete
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
@app.route('/indexitems', methods=['GET', 'POST'])
@login_required
def actionitems():
    parentdict = {}
    parentdict['A'] = track_fill()
    parentdict['B'] = drop_fill()
    parentdict['C'] = engage_fill()

    return json.dumps(parentdict)

#homepage 'Confirm' button posts here after user updates 'placed' users in PROS
@app.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    prosid = request.args.get( 'id', '', type = int )
    action_type = request.args.get( 'selection', '')
    table = request.args.get( 'table', '')
    link = request.args.get( 'link', '')
    leaver = Leaver.query.filter_by(id=prosid).first()
    if link == '':
        link = leaver.link

    print('Action Type Sent to Confirm Route: ', action_type)
    print('Table to Adjust: ', table)
    print('ID of Leaver to be Updated: ', prosid)
    print('Link -If Relevant-', link)

    tble_upd_result = indx_tbls_update(leaver, action_type, link)
    print('Index Table Update Result: ', tble_upd_result)

    parentdict = {}
    if table == 'LEADtable':
        parentdict['A'] = track_fill()

        return json.dumps(parentdict)

    elif table == 'DROPtable':
        parentdict['B'] = drop_fill()

        return json.dumps(parentdict)

    elif table == 'ENGAGEtable':
        parentdict['C'] = engage_fill()

        return json.dumps(parentdict)

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
            flash('Upload Successful')
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

# @app.route('/ndrop', methods=['GET', 'POST'])
# @login_required
# def ndrop():
#
#     leaver_dict = fillselect(leavers)
#     return json.dumps(leaver_dict)

#populates suspect table on leaver selection from dropdown
@app.route('/ajax', methods=['POST', 'GET'])
@login_required
def ajax():
    action = request.args.get( 'action', '')
    print('Action to AJAX: ', action)
    if action == 'fillselect':
        parentdict = {}
        id = 1
        parentdict['A'] = match_html(id, 1)

        return json.dumps(parentdict)

    elif action == 'selectactioned':
        id = request.args.get( 'data', '', type = int )
        parentdict = {}
        parentdict['B'] = match_html(id, 2)
        parentdict['C'] = match_html(id, 3)

        return json.dumps(parentdict)


@app.route('/sorter', methods=['POST', 'GET'])
@login_required
def sorter():
    sid = request.args.get( 'id', '', type = int )
    selection = request.args.get( 'selection', '')
    suspect = Suspect.query.filter_by(id=sid).first()
    lid = suspect.leaverid
    print('name for sorter recieved: ', suspect.name)
    print('sorter selection recieved: ', selection)

    if selection == 'Remove':
        result = suspect_remove(sid)
        print('Sorter Remove Result: ', result)
        parentdict = {}
        parentdict['C'] = match_html(lid, 3)
        parentdict['D'] = 'partial'

        return json.dumps(parentdict)

    else:
        result = suspect_sort(sid, selection)
        print('Sorter Other Result: ', result)
        parentdict = {}
        parentdict['A'] = match_html(lid, 1)
        parentdict['D'] = 'full'

        return json.dumps(parentdict)


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
    chartdata3 = chart_data('scatter')
    chartdata4 = chart_data('engage')
    chartdata['A']= chartdata1
    chartdata['B']= chartdata2
    chartdata['C'] = chartdata3
    chartdata['D'] = chartdata4


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

@app.route('/testing', methods=['GET', 'POST'])
def testing():

    return render_template('bokehtesting.html', title='Testing')

@app.route('/datepicker', methods=['GET', 'POST'])
def datepicker():
    parentdict = {}
    parentdict['C'] = testing_fill()

    return json.dumps(parentdict)

@app.route('/edates', methods=['GET', 'POST'])
@login_required
def edates():
    picker_date = request.args.get('date', '')
    picker_id  = request.args.get('eid', '', type = int)
    print('Picker ID: ', picker_id)

    format_str = '%m-%d-%Y' # The format
    datetime_obj = datetime.datetime.strptime(picker_date, format_str)
    print(datetime_obj.date())
    leaver = Leaver.query.filter_by(id=picker_id).first()
    leaver.elast = datetime_obj
    db.session.commit()

    parentdict = {}
    parentdict['C'] = engage_fill()

    return json.dumps(parentdict)
