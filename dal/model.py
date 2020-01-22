from sqlalchemy import Column, String, Integer, Date, ForeignKey, Float

from dal.db import Base

class Username(Base):
    __tablename__ = 'username'

    id = Column(Integer, primary_key=True)
    username = Column(String())
    password = Column(String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.name,
            'password' : self.password
        }

class Person(Base):

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    birthday = Column(Date)
    city = Column(String)

    def __init__(self,id, first_name, second_name, birthday, city):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.birthday = birthday
        self.city = city

    def to_string(self):
        return "Name: " + self.first_name + " " + self.second_name + ", city: " + self.city

class Profession(Base):

    __tablename__ = 'profession'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    minimal_work_expirience = Column(Integer)
    minimal_education = Column(String)
    category = Column(String)

    def __init__(self, id, name, minimal_work_expirience, minimal_education, category):
        self.id = id
        self.name = name
        self.minimal_work_expirience = minimal_work_expirience
        self.minimal_education = minimal_education
        self.category = category

    def to_string(self):
        return "Name: " + self.name + " (" + self.category + "), minimal education: " + self.minimal_education

class Skill(Base):

    __tablename__ = 'skill'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_string(self):
        return "Name: " + self.name

class UserSkill(Base):

    __tablename__ = 'users_skills'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE", onupdate="CASCADE"))
    skill_id = Column(Integer, ForeignKey('skill.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __init__(self, id, user_id, skill_id):
        self.id = id
        self.user_id = user_id
        self.skill_id = skill_id


class ProfessionSkill(Base):

    __tablename__ = 'professions_skills'

    id = Column(Integer, primary_key=True)
    profession_id = Column(Integer, ForeignKey('profession.id', ondelete="CASCADE", onupdate="CASCADE"))
    skill_id = Column(Integer, ForeignKey('skill.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __init__(self, id, profession_id, skill_id):
        self.id = id
        self.profession_id = profession_id
        self.skill_id = skill_id


class Company(Base):

    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)

    def __init__(self, id, company_name):
        self.id = id
        self.company_name = company_name


class Vacancy(Base):

    __tablename__ = 'vacancy'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    duties = Column(String)
    salary = Column(Float)
    description = Column(String)
    created_at = Column(Date)
    profession_id = Column(Integer, ForeignKey('profession.id', ondelete="CASCADE", onupdate="CASCADE"))

    def __init__(self, id, name, duties, salary, description, created_at, profession_id):
        self.id = id
        self.name = name
        self.duties = duties
        self.salary = salary
        self.description = description
        self.created_at = created_at
        self.profession_id = profession_id
