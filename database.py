from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json

with open("./env/db_info.json", 'r') as config : 
    db_info = json.load(config)

    user = db_info['user']
    password = db_info['password']
    host = db_info['host']
    port = db_info['port']
    database = db_info['database']

# DB 연결
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 세션 생성
SessionLocal = sessionmaker(bind = engine)

# 모델 클래스 베이스 생성 
Base = declarative_base()

def get_db() :
    db = SessionLocal()
    
    try :
        yield db
    finally :
        db.close()