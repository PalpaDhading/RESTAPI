from db import db
import datetime
from sqlalchemy.sql import func

class ItemModel(db.Model):
    __tablename__ = 'itemsdata'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    dateandtime =db.Column(db.String(100))
    itemLocation = db.Column(db.String(500))
    itemCondition = db.Column(db.String(100))
    symptomDetails = db.Column(db.String(200))
    resolutionDetails = db.Column(db.String(500))
    currentstatus = db.Column(db.String(500))
    DateofResolution = db.Column(db.String(30))
    currentRSSI = db.Column(db.Float(precision =2))
    currentVSWR = db.Column(db.Float(precision =2))
    currentSQIDVoltage = db.Column(db.Float(precision =2))
    otherOpportunityDetails = db.Column(db.String(500))


    sitename = db.Column(db.Integer, db.ForeignKey('sitesdata.sitename'))
    site = db.relationship('SiteModel')

    def __init__(self,dateandtime,name,itemLocation,itemCondition,\
                symptomDetails,resolutionDetails,currentstatus,DateofResolution,currentRSSI,currentVSWR,currentSQIDVoltage,otherOpportunityDetails,sitename):
        self.dateandtime =format(datetime.datetime.now().strftime("%B %d, %Y %H:%M"))
        self.name = name
        self.itemLocation = itemLocation
        self.itemCondition = itemCondition
        self.symptomDetails = symptomDetails

        self.resolutionDetails = resolutionDetails
        self.currentstatus = currentstatus
        self.DateofResolution = DateofResolution

        self.currentRSSI = currentRSSI
        self.currentVSWR = currentVSWR
        self.currentSQIDVoltage = currentSQIDVoltage

        self.otherOpportunityDetails = otherOpportunityDetails

        self.sitename = sitename

    def json(self):
        return {'Date&Time':self.dateandtime,'Sitename':self.sitename,'ItemName':self.name,'ItemLocation': self.itemLocation,'ItemCondition':self.itemCondition,'SymptomDetails':self.symptomDetails,\
                'ResolutionDetails':self.resolutionDetails,'Currentstatus':self.currentstatus,'DateofResolution':self.DateofResolution,\
                'CurrentRSSI':self.currentRSSI,'CurrentVSWR':self.currentVSWR,'CurrentSQIDVoltage':self.currentSQIDVoltage ,\
                'OtherOpportunityDetails':self.otherOpportunityDetails}

    @classmethod
    def find_by_site_name(cls,sitename):
        return cls.query.filter_by(sitename=sitename).first()

    @classmethod
    def find_by_itemname_sitename(cls,name,sitename):
        return cls.query.filter_by(name=name,sitename=sitename).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
