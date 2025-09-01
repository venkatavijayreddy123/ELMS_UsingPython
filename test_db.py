from app import app
from models import db, User, LeaveRequest

with app.app_context():
    # Make sure tables exist
    db.create_all()

    # Print all users
    users = User.query.all()
    print("Users:", users)

    # Print all leave requests
    leave_requests = LeaveRequest.query.all()
    print("Leave Requests:", leave_requests)
