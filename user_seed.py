from app import db
from models import *

db.drop_all()
db.create_all()

user1 = User(
    username="test_user_1",
    password="somehashedpassword"
)

db.session.add_all([user1])
db.session.commit()