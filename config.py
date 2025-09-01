class Config:
    SECRET_KEY = "super-secret-key"  # Change to a strong key
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:3306/leave_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
