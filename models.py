from app import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    creator_fn = db.Column(db.String())
    creator_ln = db.Column(db.String())
    creator_email = db.Column(db.String())
    event_location = db.Column(db.Text())
    event_date = db.Column(db.Date())
    event_time = db.Column(db.Time())
    event_desc = db.Column(db.Text())
    invited = db.relationship("Invited", backref="events", lazy=True)

    def __init__(
        self,
        creator_fn,
        creator_ln,
        creator_email,
        event_location,
        event_date,
        event_time,
        event_desc,
    ):
        self.creator_fn = creator_fn
        self.creator_ln = creator_ln
        self.creator_email = creator_email
        self.event_location = event_location
        self.event_date = event_date
        self.event_time = event_time
        self.event_desc = event_desc


class Invited(db.Model):
    __tablename__ = "invited"

    id = db.Column(db.Integer, primary_key=True)
    invited_email = db.Column(db.String())
    invite_code = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    invite_status = db.Column(db.String())

    def __init__(self, invited_email, invite_code, event_id):
        self.invited_email = invited_email
        self.invite_code = invite_code
        self.event_id = event_id
        self.invite_status = "none"
