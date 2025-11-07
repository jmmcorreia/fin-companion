from sqlmodel import select, Session
from app.dbmodel.user import User

def get_user_by_username(username: str, session: Session) -> User | None:
    user = session.exec(select(User).where(User.username == username)).first()
    return user