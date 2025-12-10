"""
Admin routes.
Handles CRUD operations for deliveries (admin only).
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Delivery
from forms import DeliveryForm
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to ensure only admins can access the route."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard showing all deliveries."""
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
    
    return render_template('admin/dashboard.html', deliveries=deliveries, status_counts=status_counts)


@admin_bp.route('/delivery/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_delivery():
    """Create a new delivery."""
    form = DeliveryForm()
    
    if form.validate_on_submit():
        # Check if tracking number already exists
        if Delivery.query.filter_by(tracking_number=form.tracking_number.data).first():
            flash('Tracking number already exists.', 'danger')
            return render_template('admin/delivery_form.html', form=form, title='Create Delivery')
        
        # Create new delivery
        delivery = Delivery(
            tracking_number=form.tracking_number.data,
            recipient_name=form.recipient_name.data,
            recipient_address=form.recipient_address.data,
            recipient_phone=form.recipient_phone.data,
            description=form.description.data,
            weight=form.weight.data,
            estimated_delivery_date=form.estimated_delivery_date.data,
            status=form.status.data,
            created_by_id=current_user.id
        )
        
        # Set actual delivery date if status is delivered
        if form.status.data == 'delivered':
            delivery.actual_delivery_date = date.today()
        
        db.session.add(delivery)
        db.session.commit()
        
        flash('Delivery created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/delivery_form.html', form=form, title='Create Delivery')


@admin_bp.route('/delivery/<int:delivery_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_delivery(delivery_id):
    """Edit an existing delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    form = DeliveryForm(obj=delivery)
    
    if form.validate_on_submit():
        # Check if tracking number is being changed and already exists
        if form.tracking_number.data != delivery.tracking_number:
            if Delivery.query.filter_by(tracking_number=form.tracking_number.data).first():
                flash('Tracking number already exists.', 'danger')
                return render_template('admin/delivery_form.html', form=form, title='Edit Delivery', delivery=delivery)
        
        # Update delivery fields
        delivery.tracking_number = form.tracking_number.data
        delivery.recipient_name = form.recipient_name.data
        delivery.recipient_address = form.recipient_address.data
        delivery.recipient_phone = form.recipient_phone.data
        delivery.description = form.description.data
        delivery.weight = form.weight.data
        delivery.estimated_delivery_date = form.estimated_delivery_date.data
        delivery.status = form.status.data
        delivery.updated_by_id = current_user.id
        delivery.updated_at = datetime.utcnow()
        
        # Set actual delivery date if status is delivered
        if form.status.data == 'delivered' and not delivery.actual_delivery_date:
            delivery.actual_delivery_date = date.today()
        
        db.session.commit()
        
        flash('Delivery updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/delivery_form.html', form=form, title='Edit Delivery', delivery=delivery)


@admin_bp.route('/delivery/<int:delivery_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_delivery(delivery_id):
    """Delete a delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    tracking_number = delivery.tracking_number
    db.session.delete(delivery)
    db.session.commit()
    
    flash(f'Delivery {tracking_number} has been deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delivery/<int:delivery_id>/view')
@login_required
@admin_required
def view_delivery(delivery_id):
    """View details of a specific delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('admin/delivery_view.html', delivery=delivery)

