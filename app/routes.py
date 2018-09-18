from flask import render_template, flash, redirect, url_for, request, json, Flask, jsonify, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, BokehForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Leaver, Suspect, Srep
from sqlalchemy import DateTime
from werkzeug.urls import url_parse
from helpers import processfile, pd2class, inpros, fillselect, populate_table, actionfill, dropfill, result, reset_leaver, create_figure
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
    prosid = request.args.get( 'data', '', type = int )
    action_type = request.args.get( 'action', '')
    print('Action Type Sent to Confirm Route: ', action_type)
    if action_type == 'Lead':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('Changed Result Field to Lead: ', db)
        placed_dict = actionfill('B')
        return json.dumps(placed_dict)
    elif action_type == 'Reset':
        reset_result = reset_leaver(prosid)
        print('Reset Leaver Result: ', reset_result)
        placed_dict = actionfill('B')
        return json.dumps(placed_dict)
    elif action_type == 'User Placed':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('Changed Result Field to User Placed: ', db)
        placed_dict = actionfill('B')
        return json.dumps(placed_dict)
    elif action_type == 'Rep Placed':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', action_type, 'Y')
        print('Changed Result Field to User Placed: ', db)
        placed_dict = actionfill('B')
        return json.dumps(placed_dict)
    else:
        placed_dict = actionfill('AB')
        return json.dumps(placed_dict)

@app.route('/dropclick', methods=['GET', 'POST'])
@login_required
def dropclick():
    prosid = request.args.get( 'data', '', type = int )
    action_type = request.args.get( 'action', '')
    try:
        mlink = request.args.get( 'lnk', '')
    except:
        pass
    if action_type == 'REPMoveN':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', 'New Rep Moved, NoTerminal', 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)
    elif action_type == 'REPMoveY':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', 'New Rep Moved, HasTerminal', 'Y')
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
    elif action_type == 'Inactive':
        iprosid = int(prosid)
        updated = Leaver.query.filter_by(id=iprosid).first()
        db = result(updated, 'result', 'Inactive', 'Y')
        print('DB Addition Result: ', db)
        placed_dict = actionfill('A')
        return json.dumps(placed_dict)
    elif action_type == 'Reset':
        iprosid = int(prosid)
        reset_result = reset_leaver(iprosid)
        print('DB Reset Result: ', reset_result)
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
    lhit.result = 'User Placed'
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
    lhit.result = 'Rep Placed'
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


    # choices = ['result', 'role']
    # b_selection = request.args.get("b_selection")
    # if b_selection == None:
    #     b_selection = "result"
    #
    # plot = create_figure(b_selection, 10)
    # script, div = components(plot)
    # form = BokehForm()
    # if request.method == 'POST':
    #     leavers = Leaver.query.all()
    #     df = pd.DataFrame([(d.name, d.result, d.id) for d in leavers],
    #               columns=['name', 'result', 'id'])
    #     print(df.head())
    #     source = ColumnDataSource(df)
    #     plot = figure()
    #     plot.circle(x="name",y="result",source = source)
    #return render_template('bokeh.html')

@app.route('/bokeh', methods=['GET', 'POST'])
def bokeh():
    title = 'bokeh'

    x = Counter({
        'United States': 157,
        'United Kingdom': 93,
        'Japan': 89,
        'China': 63,
        'Germany': 44,
        'India': 42,
        'Italy': 40,
        'Australia': 35,
        'Brazil': 32,
        'France': 31,
        'Taiwan': 31,
        'Spain': 29
    })
    leavers = Leaver.query.all()
    total_lvr = len(leavers)
    df = pd.DataFrame([(d.name, d.result, d.id) for d in leavers],
              columns=['name', 'result', 'id'])
    data = df.groupby('result', as_index=False)['name'].count()

    data['angle'] = data['name']/total_lvr * 2*pi
    data['color'] = Category20c[len(data)]

    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@result: @name")

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='result', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    # grab the static resources
    #js_resources = INLINE.render_js()
    #css_resources = INLINE.render_css()

    # render template
    script, div = components(p)

    # colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    # colors = [colormap[x] for x in flowers['species']]
    df1 = pd.DataFrame([(d.name, d.result, d.id, d.datetimeadded) for d in leavers],
              columns=['name', 'result', 'id', 'date'])
    df1['date'] = pd.to_datetime(df1['date'])
    p1 = figure(title = "Scatter", x_axis_type="datetime")
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Result'

    p1.circle(df1["date"], df1["result"],
         color='navy', fill_alpha=0.2, size=10)

    script1, div1 = components(p1)

    return render_template('bokeh.html', title = title, script = script, div = div, script1 = script1, div1 = div1)

@app.route('/chartgen', methods=['GET', 'POST'])
def chartgen():
    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)
    # leavers = Leaver.query.all()
    # df = pd.DataFrame([(d.name, d.result, d.id) for d in leavers],
    #     columns=['name', 'result', 'id'])
    # group1 = df.groupby('result', as_index=False)['name'].count()
    # data = group1.to_dict(orient='list')
    # buckets = g1['result'].tolist()
    # output_file("pie.html")
    #

    #
    # plot_script, plot_div = components(p)
    # kwargs = {'plot_script': plot_script, 'plot_div': plot_div}
    # kwargs['title'] = 'hello'
    # if request.method == 'GET':
    #     return render_template('bokeh.html', **kwargs)
    # source = ColumnDataSource(data=data)
    #
    #
    # #get max possible value of plotted columns with some offset
    # p = figure(x_range=buckets, y_range=(0, g1[['name']].values.max() + 3),
    #            plot_height=250, title="Report",
    #            toolbar_location=None, tools="")
    #
    # p.vbar(x=dodge('result', -0.25, range=p.x_range), top='name', width=0.4, source=source,
    #        color="#c9d9d3", legend=value("count"))
    #
    #
    # p.x_range.range_padding = 0.1
    # p.xgrid.grid_line_color = None
    # p.legend.location = "top_left"
    # p.legend.orientation = "horizontal"

    #return encode_utf8(html)



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
