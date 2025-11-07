from dataclasses import dataclass
from typing import Protocol

from sqlmodel import Session, select

from app.dbmodel.user import User


class UserRepository(Protocol):
    def get_user_by_username(self, username: str) -> User | None: ...
    def register_user(self, user: User) -> User: ...

@dataclass
class SQLUserRepository:
    session: Session

    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.exec(select(User).where(User.username == username)).first()
        return user
    
    def register_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user