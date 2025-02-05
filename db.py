import shelve

db_file = 'users.db'

def session_factory():
    db = shelve.open(db_file)
    try:
        yield db
    finally:
        db.close()