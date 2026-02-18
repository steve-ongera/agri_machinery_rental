from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    """Platform user — farmers, operators, and admins."""
    class Role(models.TextChoices):
        FARMER = 'farmer', _('Farmer / Smallholder')
        OPERATOR = 'operator', _('Equipment Operator / Owner')
        ADMIN = 'admin', _('Admin')

    role = models.CharField(max_length=15, choices=Role.choices, default=Role.FARMER)
    phone_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    national_id = models.CharField(max_length=50, blank=True)
    id_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class FarmerProfile(models.Model):
    """Profile for smallholder farmers."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=200, blank=True)
    total_land_acres = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    primary_crop = models.CharField(max_length=100, blank=True)
    secondary_crops = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=100)
    village = models.CharField(max_length=100, blank=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    has_smartphone = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=50, default='English')

    def __str__(self):
        return f"Farmer: {self.user.get_full_name()} — {self.county}"


class OperatorProfile(models.Model):
    """Profile for equipment owners/operators."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator_profile')
    business_name = models.CharField(max_length=200, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    license_number = models.CharField(max_length=100, blank=True)
    license_document = models.FileField(upload_to='licenses/', null=True, blank=True)
    service_radius_km = models.PositiveIntegerField(default=50)
    county = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100, blank=True)
    mobile_money_number = models.CharField(max_length=20, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_jobs_completed = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Operator: {self.user.get_full_name()}"


class EquipmentCategory(models.Model):
    """Category of agricultural equipment."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Equipment Categories'


class Equipment(models.Model):
    """Individual machinery/equipment unit listed for rental."""
    class Status(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        RENTED = 'rented', _('Currently Rented')
        MAINTENANCE = 'maintenance', _('Under Maintenance')
        INACTIVE = 'inactive', _('Inactive')

    class FuelType(models.TextChoices):
        DIESEL = 'diesel', _('Diesel')
        PETROL = 'petrol', _('Petrol')
        ELECTRIC = 'electric', _('Electric')
        MANUAL = 'manual', _('Manual / Animal-Powered')

    owner = models.ForeignKey(OperatorProfile, on_delete=models.CASCADE, related_name='equipment')
    category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT, related_name='equipment')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    year_manufactured = models.PositiveIntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, unique=True)
    description = models.TextField(blank=True)
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices, default=FuelType.DIESEL)
    horsepower = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capacity_info = models.CharField(max_length=200, blank=True, help_text="e.g., 3-row planter, 5-ton capacity")

    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                     validators=[MinValueValidator(Decimal('0.01'))])
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_includes_operator = models.BooleanField(default=True)
    price_includes_fuel = models.BooleanField(default=False)

    # Location
    current_county = models.CharField(max_length=100)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.AVAILABLE)
    last_serviced = models.DateField(null=True, blank=True)
    next_service_due = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand}) — {self.owner}"

    class Meta:
        ordering = ['-created_at']


class EquipmentImage(models.Model):
    """Photos of listed equipment."""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='equipment_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.equipment.name}"


class ServiceArea(models.Model):
    """Counties/areas where an operator provides service."""
    operator = models.ForeignKey(OperatorProfile, on_delete=models.CASCADE, related_name='service_areas')
    county = models.CharField(max_length=100)
    additional_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00,
                                            help_text="Extra transport fee for this area")

    class Meta:
        unique_together = ('operator', 'county')

    def __str__(self):
        return f"{self.operator} serves {self.county}"


class RentalBooking(models.Model):
    """A booking/rental request from a farmer."""
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Confirmation')
        CONFIRMED = 'confirmed', _('Confirmed')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELLED_FARMER = 'cancelled_farmer', _('Cancelled by Farmer')
        CANCELLED_OPERATOR = 'cancelled_operator', _('Cancelled by Operator')
        DISPUTED = 'disputed', _('Disputed')

    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', _('Unpaid')
        DEPOSIT_PAID = 'deposit_paid', _('Deposit Paid')
        FULLY_PAID = 'fully_paid', _('Fully Paid')
        REFUNDED = 'refunded', _('Refunded')

    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='bookings')
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='bookings')
    operator = models.ForeignKey(OperatorProfile, on_delete=models.PROTECT, related_name='bookings')

    # Job details
    job_description = models.TextField(help_text="Describe the work needed e.g. ploughing 5 acres of maize")
    land_size_acres = models.DecimalField(max_digits=8, decimal_places=2)
    crop_type = models.CharField(max_length=100, blank=True)
    farm_location_county = models.CharField(max_length=100)
    farm_gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    farm_gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    farm_directions = models.TextField(blank=True)

    # Timing
    requested_start_date = models.DateField()
    requested_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # Pricing
    quoted_rate = models.DecimalField(max_digits=10, decimal_places=2)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_status = models.CharField(max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)

    operator_notes = models.TextField(blank=True)
    farmer_notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.pk} — {self.farmer} rents {self.equipment.name}"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    """Payment record for a rental booking."""
    class Method(models.TextChoices):
        MPESA = 'mpesa', _('M-Pesa')
        AIRTEL_MONEY = 'airtel_money', _('Airtel Money')
        BANK_TRANSFER = 'bank_transfer', _('Bank Transfer')
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Debit/Credit Card')

    class Type(models.TextChoices):
        DEPOSIT = 'deposit', _('Deposit')
        FINAL = 'final', _('Final Payment')
        REFUND = 'refund', _('Refund')

    booking = models.ForeignKey(RentalBooking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=15, choices=Method.choices)
    payment_type = models.CharField(max_length=10, choices=Type.choices)
    transaction_id = models.CharField(max_length=200, unique=True)
    is_confirmed = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment #{self.transaction_id} — KES {self.amount}"


class OperatorPayout(models.Model):
    """Payout to operator after job completion."""
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        PAID = 'paid', _('Paid')
        FAILED = 'failed', _('Failed')

    operator = models.ForeignKey(OperatorProfile, on_delete=models.CASCADE, related_name='payouts')
    booking = models.OneToOneField(RentalBooking, on_delete=models.CASCADE, related_name='payout')
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    platform_fee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    platform_fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    payout_method = models.CharField(max_length=50, blank=True)
    payout_reference = models.CharField(max_length=200, blank=True)
    initiated_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout to {self.operator} — {self.net_amount}"


class BookingReview(models.Model):
    """Two-way review: farmer reviews operator, operator reviews farmer."""
    booking = models.ForeignKey(RentalBooking, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    punctuality_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    quality_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booking', 'reviewer')

    def __str__(self):
        return f"Review by {self.reviewer} for booking #{self.booking.pk}"


class MaintenanceLog(models.Model):
    """Maintenance records for equipment."""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_logs')
    service_date = models.DateField()
    service_type = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    performed_by = models.CharField(max_length=200, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='maintenance_docs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.name} — {self.service_type} on {self.service_date}"

    class Meta:
        ordering = ['-service_date']


class SupportTicket(models.Model):
    """Customer support for disputes or issues."""
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        IN_REVIEW = 'in_review', _('Under Review')
        RESOLVED = 'resolved', _('Resolved')
        CLOSED = 'closed', _('Closed')

    class Priority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')
        URGENT = 'urgent', _('Urgent')

    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    booking = models.ForeignKey(RentalBooking, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.pk}: {self.subject}"


class Notification(models.Model):
    """In-app and SMS notifications."""
    class Channel(models.TextChoices):
        IN_APP = 'in_app', _('In-App')
        SMS = 'sms', _('SMS')
        PUSH = 'push', _('Push Notification')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    is_read = models.BooleanField(default=False)
    related_booking = models.ForeignKey(RentalBooking, on_delete=models.SET_NULL, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.channel}] {self.title} → {self.user}"

    class Meta:
        ordering = ['-sent_at']