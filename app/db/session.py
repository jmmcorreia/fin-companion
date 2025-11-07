from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)



def get_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise

SessionDep = Annotated[Session, Depends(get_session)]