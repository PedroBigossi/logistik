"""
User routes.
Handles viewing deliveries and updating delivery status (regular users).
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Delivery
from forms import StatusUpdateForm
from datetime import datetime, date

user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing all deliveries."""
    # Get all deliveries ordered by creation date (newest first)
    deliveries = Delivery.query.order_by(Delivery.created_at.desc()).all()
    
    # Count deliveries by status
    status_counts = {
        'ongoing': Delivery.query.filter_by(status='ongoing').count(),
        'in_route': Delivery.query.filter_by(status='in_route').count(),
        'late': Delivery.query.filter_by(status='late').count(),
        'delivered': Delivery.query.filter_by(status='delivered').count(),
        'total': Delivery.query.count()
    }
    
    return render_template('user/dashboard.html', deliveries=deliveries, status_counts=status_counts)


@user_bp.route('/delivery/<int:delivery_id>/view')
@login_required
def view_delivery(delivery_id):
    """View details of a specific delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('user/delivery_view.html', delivery=delivery)


@user_bp.route('/delivery/<int:delivery_id>/update-status', methods=['GET', 'POST'])
@login_required
def update_status(delivery_id):
    """Update the status of a delivery (users can only update status)."""
    delivery = Delivery.query.get_or_404(delivery_id)
    form = StatusUpdateForm(obj=delivery)
    
    if form.validate_on_submit():
        # Update only the status
        delivery.status = form.status.data
        delivery.updated_by_id = current_user.id
        delivery.updated_at = datetime.utcnow()
        
        # Set actual delivery date if status is delivered
        if form.status.data == 'delivered' and not delivery.actual_delivery_date:
            delivery.actual_delivery_date = date.today()
        
        db.session.commit()
        
        flash('Delivery status updated successfully.', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/update_status.html', form=form, delivery=delivery)

