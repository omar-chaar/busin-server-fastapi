# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, LONGBLOB, TINYINT  
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'Company'

    company_id = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(String(50))


class Department(Base):
    __tablename__ = 'Department'

    department_id = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    company_id = Column(ForeignKey('Company.company_id'), nullable=False, index=True)

    company = relationship('Company')


class User(Base):
    __tablename__ = 'User'

    user_id = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    position = Column(String(30), nullable=False)
    email = Column(String(320))
    password = Column(String(225))
    profile_picture = Column(LONGBLOB)
    department_id = Column(ForeignKey('Department.department_id'), nullable=False, index=True)   
    is_adm = Column(TINYINT(4), nullable=False)
    is_owner = Column(TINYINT(4), nullable=False, server_default=text("0"))
    reg_code = Column(String(5), unique=True)

    department = relationship('Department')


class Announcement(Base):
    __tablename__ = 'Announcement'

    announcement_id = Column(INTEGER(11), primary_key=True, unique=True)
    announcement_title = Column(String(45), nullable=False)
    announcement_body = Column(String(600), nullable=False)
    sender_id = Column(ForeignKey('User.user_id'), nullable=False, index=True)
    time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    sender = relationship('User')


class Message(Base):
    __tablename__ = 'Message'

    message_id = Column(INTEGER(11), primary_key=True, unique=True)
    sender_id = Column(ForeignKey('User.user_id'), nullable=False, index=True)
    receiver_id = Column(ForeignKey('User.user_id'), nullable=False, index=True)
    time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    message_body = Column(String(200), nullable=False)
    parent_message_id = Column(ForeignKey('Message.message_id'), index=True)
    was_seen = Column(TINYINT(4), nullable=False, server_default=text("0"))

    parent_message = relationship('Message', remote_side=[message_id])
    receiver = relationship('User', primaryjoin='Message.receiver_id == User.user_id')
    sender = relationship('User', primaryjoin='Message.sender_id == User.user_id')


class AnnouncementReceiver(Base):
    __tablename__ = 'AnnouncementReceiver'

    announcement_id = Column(ForeignKey('Announcement.announcement_id'), primary_key=True, nullable=False)
    receiver_id = Column(ForeignKey('User.user_id'), primary_key=True, nullable=False, index=True)
    time_saw = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    has_seen = Column(TINYINT(4))

    announcement = relationship('Announcement')
    receiver = relationship('User')