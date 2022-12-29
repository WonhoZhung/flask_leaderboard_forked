from flask import Flask
from main import Submission, User, app

with app.app_context():
    subs = Submission.query.all()
print("SUBMISSION: ")
for sub in subs:
    print(sub.user_id, sub.score)

print()

with app.app_context():
    users = User.query.all()
print("USERS: ")
for user in users:
    print(user.username, user.password)
