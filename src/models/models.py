import datetime
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass,Mapped,mapped_column


class Base(DeclarativeBase,MappedAsDataclass):
    pass

class Users(Base,MappedAsDataclass):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]

    def __repr__(self):
        return f'<id:{self.id},name:{self.name}>'






class Tasks(Base,MappedAsDataclass):
    __tablename__ = 'tasks'
    task_id:Mapped[int] = mapped_column(primary_key=True)
    task_status:Mapped[str]
    task_title:Mapped[str]
    task_text:Mapped[str]
    task_time_start:Mapped[datetime.date]
    task_time_end: Mapped[datetime.date]

    def __repr__(self):
        return f'<task_id:{self.task_id},task_status:{self.task_status},task_title:{self.task_title},task_text:{self.task_text},task_time{self.task_time}'