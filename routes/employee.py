from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, LeaveRequest

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

@employee_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("employee_dashboard.html", user=current_user)

@employee_bp.route("/apply_leave", methods=["GET", "POST"])
@login_required
def apply_leave():
    if request.method == "POST":
        leave = LeaveRequest(
            start_date=request.form["start_date"],
            end_date=request.form["end_date"],
            reason=request.form["reason"],
            user_id=current_user.id
        )
        db.session.add(leave)
        db.session.commit()
        return redirect(url_for("employee.my_leaves"))
    return render_template("apply_leave.html")

@employee_bp.route("/my_leaves")
@login_required
def my_leaves():
    leaves = LeaveRequest.query.filter_by(user_id=current_user.id).all()
    return render_template("my_leaves.html", leaves=leaves)
