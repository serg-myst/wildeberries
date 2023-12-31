from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DATABASE, BASE_TYPE

DATABASE_URL = DATABASE

engine = create_engine(DATABASE_URL, echo=False)
if BASE_TYPE == 'PGSQL':
    engine = create_engine(DATABASE_URL, echo=False, client_encoding='utf8')

session_maker = sessionmaker(engine, expire_on_commit=False)

# Работа с SQLAlchemy
# https://otus.ru/journal/vvedenie-v-sqlalchemy/
# https://metanit.com/python/database/3.3.php

# https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh
