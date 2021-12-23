import os, re, smtplib
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from models import Event, Invited

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@app.route("/")
def index():

    return "Success", 200


@app.route("/new_rsvp", methods=["GET", "POST"])
def new_rsvp():

    if request.method == "POST":
        form_data = request.json["formData"]

        new_event = Event(
            form_data["creator_fn"],
            form_data["creator_ln"],
            form_data["creator_email"],
            form_data["event_location"],
            form_data["event_date"],
            form_data["event_time"],
            form_data["event_desc"],
        )
        db.session.add(new_event)
        db.session.flush()
        db.session.refresh(new_event)

        # Create invites and send invite emails
        emails = parse_invite_emails(form_data["event_invites"])

        for email in emails:
            invite_code = int(str(new_event.id) + "1234")
            print(invite_code)
            new_invited = Invited(email, invite_code, new_event.id)
            db.session.add(new_invited)

        send_invites(new_event.id, emails)

        db.session.commit()

        # Send the created event back as a response
        event_data = format_event(new_event.id, return_id=True)
        return jsonify(event_data), 200

    return "Bad request", 400


@app.route("/update_rsvp", methods=["GET", "POST"])
def update_rsvp():
    if request.method == "POST":
        form_data = request.json["formData"]
        event_id = form_data["event_id"]
        event_emails = form_data["event_invites"]

        # Remove uneeded fields from event update
        del form_data["event_id"]
        del form_data["event_invites"]
        event = Event.query.filter_by(
            id=event_id,
        )
        event.update(dict(form_data))

        # Update invites
        invites = Invited.query.filter_by(event_id=event_id)
        emails = parse_invite_emails(event_emails)

        for email in emails:
            exists = False
            for invite in invites:
                if invite.invited_email == email:
                    exists = True
                    break
            if not exists:
                invite_code = int(str(event_id) + "1234")
                print(invite_code)
                new_invited = Invited(email, invite_code, event_id)
                db.session.add(new_invited)

        db.session.commit()

        event_data = format_event(event_id, return_id=True)

        if not send_invites(event_id, emails):
            return "Something went wrong sending out the invites...", 400

        return jsonify(event_data), 200

    else:
        return "Bad request", 400


@app.route("/get_rsvp_event", methods=["POST"])
def get_rsvp_by_event():
    form_data = request.json["formData"]
    event = Event.query.filter_by(
        creator_email=form_data["creator_email"],
        id=form_data["event_id"],
    ).first()

    if event:
        event_data = get_event_to_update(event)
        return jsonify(event_data), 200
    else:
        return "No event matching that email or event id", 404


@app.route("/get_rsvp_invite", methods=["POST"])
def get_rsvp_by_invite():

    form_data = request.json["formData"]
    invite = Invited.query.filter_by(
        invited_email=form_data["invited_email"],
        invite_code=form_data["invite_code"],
    ).first()

    if invite:
        event_data = format_event(invite.event_id)
        return jsonify(event_data), 200

    else:

        return "No invite matching that email or invite code", 404


def get_event_to_update(event):
    """ Takes an event and returns a dictionary with the required details to update the event """
    formatted_date = event.event_date.strftime("%m/%d/%Y")
    formatted_time = event.event_time.strftime("%H:%M:%S")
    event_data = {
        "id": event.id,
        "creator_fn": event.creator_fn,
        "creator_ln": event.creator_ln,
        "creator_email": event.creator_email,
        "location": event.event_location.title(),
        "date": formatted_date,
        "time": formatted_time,
        "desc": event.event_desc,
    }

    # Get emails of invited guests
    invited_email_list = []
    for invite in event.invited:
        invited_email_list.append(invite.invited_email)
    event_data["invited_emails"] = invited_email_list

    return event_data


def format_event(event_id, return_id=False):
    """ Takes an event id and returns a dictionary of the event details """

    event_query = Event.query.filter_by(id=event_id).first()

    formatted_name = event_query.creator_fn + " " + event_query.creator_ln
    formatted_date = event_query.event_date.strftime("%A, %B %d")
    formatted_time = event_query.event_time.strftime("%#I:%M %p")
    event_data = {
        "id": event_id if return_id else None,
        "creator": formatted_name,
        "location": event_query.event_location.title(),
        "date": formatted_date,
        "time": formatted_time,
        "desc": event_query.event_desc,
    }

    return event_data


def parse_invite_emails(email_list):
    emails = email_list
    if type(email_list) is str:
        emails = [email.strip() for email in email_list.split(",")]

    for email in emails:
        if not (re.fullmatch(email_regex, email)):
            emails.remove(email)

    return emails


def send_invites(event_id, email_list):
    """ Sends out invite emails to emails in the list. Returns true if succesful."""

    subject = "You've been invited!"
    body = "Hello, this is a test."

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(app.config["GMAIL_USER"], app.config["GMAIL_PASS"])
        for email in email_list:
            email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (
                "Simply RSVP",
                email,
                subject,
                body,
            )
            server.sendmail(app.config["GMAIL_USER"], email, email_text)

        server.close()
        return True

    except:
        return False


if __name__ == "__main__":
    app.run()
