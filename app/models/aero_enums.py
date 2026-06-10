from enum import Enum


class UserRole(str, Enum):
    RIDER = "rider"
    DRIVER = "driver"
    ADMIN = "admin"
    REVIEWER = "reviewer"


class VehicleType(str, Enum):
    SEDAN = "sedan"
    SUV = "suv"
    VAN = "van"
    TRUCK = "truck"
    LUXURY = "luxury"


class BookingStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    ENROUTE = "enroute"
    ARRIVED = "arrived"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class DocumentType(str, Enum):
    DRIVER_LICENSE = "driver_license"
    VEHICLE_REGISTRATION = "vehicle_registration"
    INSURANCE = "insurance"
    BACKGROUND_CHECK = "background_check"
