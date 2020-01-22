from sqlalchemy import func

from dal.db import engine, Base, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base.metadata.create_all(engine)

session = Session()

def get_data(class_name):
    return session.query(class_name).all()


def get_data_by_id(class_name, id):
    return session.query(class_name).filter_by(id = int(id)).first()

def get_data_by_username(class_name, username):
    return session.query(class_name).filter_by(first_name = username)

def insert_data(data):
    session.add(data)


def delete_data(class_name, id):
    user = session.query(class_name).filter_by(id=id).first()
    session.delete(user)


def update_data(obj, class_name):
    mapped_values = {}
    for item in class_name.__dict__.items():
        field_name = item[0]
        field_type = item[1]
        is_column = isinstance(field_type, InstrumentedAttribute)
        if is_column:
            mapped_values[field_name] = getattr(obj, field_name)

    session.query(class_name).filter_by(id=obj.id).update(mapped_values)


def req1(cl1, cl2, cl3):
    res = session.query(cl1.first_name, func.count(cl3.name))\
        .select_from(cl1)\
        .join(cl2)\
        .join(cl3)\
        .group_by(cl1.first_name).all()
    return res


def req2(cl1, cl2, cl3):
    res = session.query(cl2.id, cl1.first_name, cl1.second_name, cl3.name) \
        .select_from(cl1) \
        .join(cl2) \
        .join(cl3) \
        .all()
    return res


def req3(cl1, cl2, cl3):
    res = session.query(cl3.name, func.count(cl3.name)) \
        .select_from(cl1) \
        .join(cl2) \
        .join(cl3) \
        .group_by(cl3.name).all()
    return res

def req4(cl1, cl2, cl3):
    res = session.query(cl2.id, cl1.name, cl3.name) \
        .select_from(cl1) \
        .join(cl2) \
        .join(cl3) \
        .all()
    return res

def save():
    session.commit()

