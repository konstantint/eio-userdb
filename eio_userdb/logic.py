# -*- coding: UTF-8 -*-
"""
EIO user registration webapp :: "Business logic"

Copyright 2014, EIO Team.
License: MIT
"""
from time import time
from datetime import datetime
import traceback

from flask import request, Markup, flash, redirect, url_for
from flask_mail import Message

from .main import app, db, mail
from .model import Registration, User


def send_activation_email(r):
    options = {'activation_code': r.activation_code(int(time()/60)),
               'registration_server_url': app.config['REGISTRATION_SERVER_URL'],
               'contest_server_url': app.config['CONTEST_SERVER_URL'],
               'email': r.email}
    
    msg = Message(recipients=[r.email],
                  subject="Registreerimise kinnitus",
                  body=u"""Olete registreerunud EIO lahenduste esitamise süsteemi kasutajaks.

Oma konto aktiveerimiseks sisestage järgneva 20 tunni jooksl kood
%(activation_code)s lehel %(registration_server_url)sactivate.

Kui see on tehtud, saate alates 10. novembrist võistlusserverisse sisse logida lehel
%(contest_server_url)s,
kasutades kasutajatunnust %(email)s ning omavalitud parooli.

Pange tähele, et kasutajatunnus ja parool on tõutundlikud.

Lugupidamisega,
Veebiserver
""" % options)
    mail.send(msg)


def register(r):
    try:
        # Check whether the user with the same email is already registered for the same contest_id
        results = db.session.query(Registration).filter(Registration.contest_id == app.config['CONTEST_ID'],
                                                        Registration.email == r.email).all()
        if (len(results) > 0):
            if results[0].activated:
                flash(Markup(u"Sellise e-mailiga kasutaja juba registreeritud. Parooli vahetada saate <a href='%s'>siit</a>." % url_for('passwordreset') + \
                            u" Andmete vahetamiseks võtke ühendust <a href='%s'>administraatoriga</a>." % app.config['CONTACT_URL'] ), "danger")
                return
            else:
                send_activation_email(results[0])
                flash(Markup(u"Sellise e-mailiga kasutaja juba registreeritud. Kasutaja emailile oli saadetud kiri aktiveerimiskoodiga." + \
                            u" Kasutaja andmete vahetamiseks võtke ühendust <a href='/'>administraatoriga</a>."), "danger")
                return redirect(url_for('activate'))
        
        # Add user to the database and send activation email
        r.activated = False
        r.registration_time=datetime.now()
        r.registration_ip=request.remote_addr
        r.contest_id = app.config['CONTEST_ID']
        db.session.add(r)
        db.session.commit() # Also obtains r.id
        send_activation_email(r)
        flash(u"Kasutaja emailile saadeti kiri aktiveerimiskoodiga, palun sisestage kood alltoodud tekstivälja.", 'success')
        return redirect(url_for('activate'))
    except Exception, e:
        traceback.print_exc()            
        flash(e.message, 'danger')


def is_valid_activation(code, expiration_minutes):
    try:
        a, b, c = str(code).split('$')
        r = db.session.query(Registration).get(int(b))
        cur_time = int(time()/60)
        for i in range(0, expiration_minutes):
            if r.activation_code(cur_time - i) == code:
                return True
    except:
        traceback.print_exc()
        return False
    return False


def activate(code):
    if is_valid_activation(code, 60*20):
        r = db.session.query(Registration).get(int(code.split('$')[1]))
        if not r.activated:
            r.activated = True
            # Create a clone in the User table
            u = User(first_name = r.first_name,
                     last_name = r.last_name,
                     username = r.email,
                     password = r.password,
                     division = r.category,
                     email = r.email,
                     contest_id = r.contest_id)
            db.session.add(u)
            db.session.commit()
        return True
    else:
        return False


def reset_password(code, new_password):
    if is_valid_activation(code, 30):
        r = db.session.query(Registration).get(int(code.split('$')[1]))
        if not r.activated:
            flash("Kasutaja pole aktiveeritud", "danger")
        else:
            r.password = new_password
            u = db.session.query(User).filter(User.username == r.email, User.contest_id == r.contest_id).all()
            if len(u) == 0:
                r.activated == False
                flash("Kasutaja pole aktiveeritud", "danger")
            else:
                u[0].password = new_password
            db.session.commit()
            flash("Parool vahetatud", "success")
            return redirect(url_for("index"))
    else:
        flash(u"Vale või aegunud autentimiskood", "danger")


def send_password_reset_mail(email):
    r = db.session.query(Registration).filter(Registration.contest_id == app.config['CONTEST_ID'],
                                                    Registration.email == email).all()
    if len(r) == 0:
        flash("Sellise emailiga kasutaja pole registreeritud", "danger")
        return
    else:
        options = {'activation_code': r[0].activation_code(int(time()/60)),
                   'registration_server_url': app.config['REGISTRATION_SERVER_URL']}
        
        msg = Message(recipients=[r[0].email],
                      subject="Parooli vahetamine",
                      body=u"""Keegi (arvatavasti Teie ise) soovis vahetada Teie EIO parooli.
                      
Parooli saate vahetada lehel %(registration_server_url)spasswordreset/%(activation_code)s
järgmise poole tunni jooksul.

Kui Te ise paroolivahetust ei tellinud, ignoreerige see kiri.

Lugupidamisega,
Veebiserver
    """ % options)
        mail.send(msg)
        flash("Paroolivahetuse juhendid saadetud etteantud aadressile", "success")
        return redirect(url_for('index'))
