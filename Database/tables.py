from sqlalchemy import create_engine, Column, String, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
load_dotenv()
from os import getenv

user = getenv("USER")
password = getenv('PASSWORD')
host = getenv('HOST')
port = getenv('PORT')
database = getenv('DATABASE')

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    chat_id = Column(BigInteger, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone = Column(String(13), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.chat_id}, {self.firstname!r}, {self.lastname}, {self.phone})'

    @property
    def greating(self):
        return f"Salom, {self.firstname}"

    @classmethod
    def display(cls, session):
        people = session.query(cls).all()
        people = [(p, p.is_adult, p.greating) for p in people]
        return people

    def save(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def save_all(cls, session, instances):
        session.add_all(instances)
        session.commit()

    @classmethod
    def delete(cls, session, id_):
        obj = session.query(cls).filter(cls.chat_id == id_).first()
        if obj:
            session.delete(obj)
            session.commit()
            return True
        return False

    @classmethod
    def get_by_id(cls, session, id_):
        return session.query(cls).filter(cls.chat_id == id_).first()

    # update
    @classmethod
    def update(cls, session, id_, **kwargs):
        obj = cls.get_by_id(session, id_)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise KeyError(f'`{cls.__name__}` class da  `{key}` attribut mavjud emas!')
            session.commit()
            return True
        return False

session = sessionmaker(bind=engine, expire_on_commit=False)
user_session = session()