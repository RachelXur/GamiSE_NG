from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user includes Normal User, IT department, Admin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    image_file = db.Column(db.String(200), nullable=True, default='picture1.jpg')
    password = db.Column(db.String(60), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    interest = db.Column(db.String(60), nullable=False)
    qa = db.Column(db.String(40), nullable=False)
    qb = db.Column(db.String(40), nullable=False)
    qc = db.Column(db.String(40), nullable=False)
    qd = db.Column(db.String(40), nullable=False)
    qe = db.Column(db.String(40), nullable=False)
    qf = db.Column(db.String(40), nullable=False)
    qg = db.Column(db.String(40), nullable=False)
    qh = db.Column(db.String(40), nullable=False)
    qi = db.Column(db.String(40), nullable=False)
    qj = db.Column(db.String(40), nullable=False)
    qk = db.Column(db.String(40), nullable=False)
    post_count = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    confirm = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    user_report = db.relationship('Userreport', backref='user', lazy=True)
    it_report = db.relationship('Itreport', backref='user', lazy=True)
    phishresults = db.relationship('Phishingresult', backref='user', lazy=True)
    like_record = db.relationship('LikePostRecord', backref='user', lazy=True)
    dislike_record = db.relationship('DislikePostRecord', backref='user', lazy=True)
    

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}')"
    
    # get token
    def get_token(self, exp=1000):
        """
        payload : {"uid":self.id}
        """
        s = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), exp)
        return s.dumps({"uid":self.id}).decode('utf-8')

    # get sending phishing email token
    def email_token(self, exp=604800):
        """
        payload : {"uid":self.id}
        """
        emails = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), exp)
        return emails.dumps({"uid":self.id}).decode('utf-8')
    
    # since we need to determine if user liked a post already in html file, so we add this func to User class
    def liked_post(self, post_id):
        return LikePostRecord.query.filter(
                    LikePostRecord.post_id==post_id,
                    LikePostRecord.user_id==self.id).count()
        
    def disliked_post(self, post_id):
        return DislikePostRecord.query.filter(
                    DislikePostRecord.post_id==post_id,
                    DislikePostRecord.user_id==self.id).count()

    
    @staticmethod
    def verify_token(token):
        """
        docstring
        """
        s = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = s.loads(token)["uid"]
            # This payload is decoded and safe
        except:
            return None
        # return the user obj
        return User.query.get(user_id)

    # verify phishing email token
    @staticmethod
    def verify_emailtoken(token):
        """
        docstring
        """
        emails = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
        try:
            user_id = emails.loads(token)["uid"]
            # This payload is decoded and safe
        except:
            return None
        # return the user obj
        return User.query.get(user_id)


#Table to store like post id and by which user id
class LikePostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"LikePostRecord('{self.id}', post_id:'{self.post_id}', user_id:'{self.user_id}')"
    
#Table to store dislike post id and by which user id
class DislikePostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"DislikePostRecord('{self.id}', post_id:'{self.post_id}', user_id:'{self.user_id}')"

# IT department unique code
class Ituser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usercode = db.Column(db.String(20), nullable=True, default=0)

    def __repr__(self):
        return f"Ituser('{self.id}','{self.usercode}')"


# User post. IT depatment also can post
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_record = db.relationship('LikePostRecord', backref='post', lazy=True)
    dislike_record = db.relationship('DislikePostRecord', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.post_id}', '{self.post_date}', '{self.post_title}', '{self.content}', '{self.user_id}')"

# User withdrawal questionnaire table
class Withdrawal(db.Model):
    withdrawal_id = db.Column(db.Integer, primary_key=True)
    withdrawal_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    qa = db.Column(db.String(40), nullable=False)
    qb = db.Column(db.String(40), nullable=False)
    qc = db.Column(db.String(40), nullable=False)
    qd = db.Column(db.String(40), nullable=False)
    post_count = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    reason = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Withdrawal('{self.withdrawal_id}', '{self.withdrawal_date}', '{self.qa}', '{self.qb}', '{self.qc}', '{self.feedback}')"

# Normal user report an attack
class Userreport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    senderemail = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    riskaction = db.Column(db.Text, nullable=False)
    reportstatus = db.Column(db.String(40), nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Userreport('{self.report_id}', '{self.subject}', '{self.senderemail}', '{self.reason}', '{self.riskaction}', '{self.reportstatus}', '{self.read}', '{self.report_date}', '{self.user_id}')"


# save the user reports that deleted by IT. So when users ask why IT deleted their report. IT can check the reason.
class Deleteuserreport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    senderemail = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    riskaction = db.Column(db.Text, nullable=False)
    reportstatus = db.Column(db.String(40), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Deleteuserreport('{self.report_id}', '{self.subject}', '{self.senderemail}', '{self.reason}', '{self.riskaction}', '{self.reportstatus}', '{self.report_date}', '{self.user_id}')"


# IT department submit a solution
class Itreport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    senderemail = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Itreport('{self.report_id}', '{self.subject}', '{self.senderemail}', '{self.reason}', '{self.solution}', '{self.report_date}', '{self.user_id}')"


# Admin Phishing campaign
class Phishingcampaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(100), unique=True, nullable=False)
    campaign_type = db.Column(db.String(100), nullable=False)
    campaign_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    phishresults = db.relationship('Phishingresult', backref='campaign', lazy=True)

    def __repr__(self):
        return f"Phishingcampaign('{self.campaign_id}', '{self.campaign_name}', '{self.campaign_type}', '{self.campaign_date}')"

# Admin check phishing campaign result. If user click the link, the phish_click = 1
class Phishingresult(db.Model):
    presult_id = db.Column(db.Integer, primary_key=True)
    phish_send = db.Column(db.Boolean, nullable=False, default=False)
    phish_click = db.Column(db.Boolean, nullable=False, default=False)
    phish_link = db.Column(db.Text, default='link')
    campaign_id = db.Column(db.Integer, db.ForeignKey('phishingcampaign.campaign_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Phishingresult('{self.presult_id}', '{self.phish_send}', '{self.phish_click}', '{self.phish_link}', '{self.campaign_id}', '{self.user_id}')"


# After Phishing simulation, if user click the link, it will save the token and the user id in this table. 
class Phishinglinkrecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    record_link = db.Column(db.Text, default='link')
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Phishingcampaign('{self.campaign_id}', '{self.campaign_name}', '{self.campaign_type}', '{self.campaign_date}')"

class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=True, default='picture1.jpg')

    def __repr__(self):
        return f"Photoselect('{self.photo_id}', '{self.path}')"


# A record that save the email address changing
class Emailchangerecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    before = db.Column(db.String(200), nullable=False)
    after = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Emailchangerecord('{self.record_id}', '{self.record_date}', '{self.before}', '{self.after}')"
