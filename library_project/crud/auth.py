from models import User


def get_users_from_db(db_session):
    users = db_session.query(User).all()
    return users



def get_user_by_id(db_session, user_id):
    user = db_session.query(User).filter(User.id == user_id).first()
    return user


def get_user_by_username(db_session, username):
    user = db_session.query(User).filter(User.username == username).first()
    return user


def get_user_by_email(db_session, email):
    user = db_session.query(User).filter(User.email == email).first()
    return user


def add_user_to_db(db_session, user):
    db_user = User(**dict(user))
    db_session.add(db_user)
    db_session.commit()
    return db_user