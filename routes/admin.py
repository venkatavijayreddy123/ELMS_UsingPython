from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from models import db, LeaveRequest

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    leaves = LeaveRequest.query.all()
    return render_template("admin_dashboard.html", leaves=leaves)

@admin_bp.route("/approve/<int:leave_id>")
@login_required
def approve(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    leave.status = "Approved"
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/reject/<int:leave_id>")
@login_required
def reject(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    leave.status = "Rejected"
    db.session.commit()
    return redirect(url_for("admin.dashboard"))
