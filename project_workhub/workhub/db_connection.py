from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
import os
from sqlalchemy.orm import declarative_base
load_dotenv()
"""It's a url for db connection the take db_name,driver_name,username,password and port ,host ,db_name"""
db_url = os.getenv("database_url")

engine = create_async_engine(db_url)

"""sessionmaker => It comes from sqlalchemy.orm that help us to make connection to the db whenever we want it's like a db manager that handle db connection and disconnection it giver seprate connetion for each and every request """

Base = declarative_base()
"""Base => It's like a box whenever we make  models in project. that time we send this Base it args of the class of that models Base take a snapshot of all tables .
we can understand it's llike a box where we put over all model when we run base.create.meta it's directly make the table in database ."""
AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,
expire_on_commit=False,
)
async def get_db() :
    async with AsyncSessionLocal() as db : 
        yield db