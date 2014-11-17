# -*- coding: UTF-8 -*-
"""
EIO user registration webapp :: Flask views.

Copyright 2014, EIO Team.
License: MIT
"""
from datetime import datetime
import traceback

from flask import render_template, flash, Markup, request, redirect, url_for, jsonify, make_response
from flask_wtf import Form
from wtforms import StringField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_mail import Message

from .main import app, db, mail
from .model import Registration
from . import logic

import logging
log = logging.getLogger('eio_userdb.views')

# ---------------------------------------------------------------------------- #
@app.route('/')
def index():
    return redirect(url_for('over'))

@app.route('/over')
def over():
    return render_template('over.html')
# ---------------------------------------------------------------------------- #
class RegistrationForm(Form):
    first_name = StringField('Eesnimi', validators=[DataRequired(), Length(max=255)])
    last_name = StringField('Perenimi', validators=[DataRequired(), Length(max=255)])
    category = SelectField('Kategooria', choices=[('', ''), ('school', u'õpilane'), ('university', u'üliõpilane'), ('other', 'muu')], validators=[DataRequired()])
    school = StringField('Kool/asutus', validators=[DataRequired(), Length(max=255)], description=u'(kooli korral kindlasti ametlik nimi eesti keeles)')
    grade = StringField('Klass', validators=[DataRequired(), Length(max=255)], description=u'(õpilastel 1..12, üliõpilastel I..V, muudel -)')
    email = StringField('Meiliaadress', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Parool', validators=[DataRequired(), Length(min=6, message=u'Parool liiga lühike'), 
                                                   EqualTo('confirm', message=u'Parool ja parooli kordus ei ole identsed'),
                                                   Length(max=255)],
                                       description=u'Palun, ära kasuta siin oma mujal juba kasutusel oleva parooli!')
    confirm = PasswordField('Parooli kordus')
    agree = BooleanField(u'Olen nõus, et minu andmeid kasutatakse informaatikavõistlustega seotud teavitusteks', validators=[DataRequired(message=u'Puudub nõusolek andmete kasutamiseks')])

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        r = Registration(first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         category=form.category.data,
                         school=form.school.data,
                         grade=form.grade.data,
                         email=form.email.data,
                         password=form.password.data)
        result = logic.register(r)
        if result is not None:
            return result
    return render_template('register.html', form=form)

# ---------------------------------------------------------------------------- #
class ActivateForm(Form):
    code = StringField('Aktiveerimiskood', validators=[DataRequired(), Length(max=120)])

@app.route('/activate', methods=('GET', 'POST'))
def activate():
    form = ActivateForm(request.form)
    if form.validate_on_submit():
        if logic.activate(form.code.data.strip()):
            flash('Kasutaja aktiveeritud', 'success')
            return redirect(url_for('index'))
        else:
            flash(u'Vale või aegunud aktiveerimiskood', 'danger')
    return render_template('activate.html', form=form)

# ---------------------------------------------------------------------------- #
class PasswordForm(Form):
    password = PasswordField('Uus parool', validators=[DataRequired(), Length(min=7, message=u'Parool liiga lühike'), 
                                                   EqualTo('confirm', message=u'Parool ja parooli kordus ei ole identsed'),
                                                   Length(max=255)])
    confirm = PasswordField('Parooli kordus')

class EmailForm(Form):
    email = StringField('Meiliaadress', validators=[DataRequired(), Email(), Length(max=120)])
    

@app.route('/passwordreset', methods=('GET', 'POST'))
@app.route('/passwordreset/<code>', methods=('GET', 'POST'))
def passwordreset(code=None):
    password_form = PasswordForm(request.form)
    email_form = EmailForm(request.form)
    if code is not None:
        if password_form.validate_on_submit():
            r = logic.reset_password(code, password_form.password.data)
            if r is not None:
                return r
    elif email_form.validate_on_submit():
        r = logic.send_password_reset_mail(email_form.email.data)
        if r is not None:
            return r
    return render_template('passwordreset.html', code=code, password_form=password_form, email_form=email_form)

# ---------------------------------------------------------------------------- #
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
