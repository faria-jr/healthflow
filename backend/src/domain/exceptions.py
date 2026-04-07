"""Domain exceptions."""


class DomainError(Exception):
    """Base domain error."""

    pass


class ValidationError(DomainError):
    """Validation error."""

    pass


class NotFoundError(DomainError):
    """Resource not found error."""

    pass


class ConflictError(DomainError):
    """Conflict error."""

    pass


class UnauthorizedError(DomainError):
    """Unauthorized error."""

    pass


class ForbiddenError(DomainError):
    """Forbidden error."""

    pass


# Patient exceptions
class PatientNotFoundError(NotFoundError):
    """Patient not found."""

    pass


class PatientAlreadyExistsError(ConflictError):
    """Patient already exists."""

    pass


class InvalidCPFError(ValidationError):
    """Invalid CPF."""

    pass


# Doctor exceptions
class DoctorNotFoundError(NotFoundError):
    """Doctor not found."""

    pass


class DoctorAlreadyExistsError(ConflictError):
    """Doctor already exists."""

    pass


class InvalidCRMError(ValidationError):
    """Invalid CRM."""

    pass


# Appointment exceptions
class AppointmentNotFoundError(NotFoundError):
    """Appointment not found."""

    pass


class AppointmentConflictError(ConflictError):
    """Appointment time conflict."""

    pass


class InvalidAppointmentTimeError(ValidationError):
    """Invalid appointment time."""

    pass


class AppointmentStatusError(DomainError):
    """Invalid appointment status transition."""

    pass


# Medical record exceptions
class MedicalRecordNotFoundError(NotFoundError):
    """Medical record not found."""

    pass


class MedicalRecordAlreadyExistsError(ConflictError):
    """Medical record already exists for appointment."""

    pass


# Payment exceptions
class PaymentNotFoundError(NotFoundError):
    """Payment not found."""

    pass


class PaymentAlreadyExistsError(ConflictError):
    """Payment already exists for appointment."""

    pass


# Review exceptions
class ReviewNotFoundError(NotFoundError):
    """Review not found."""

    pass


class ReviewAlreadyExistsError(ConflictError):
    """Review already exists for appointment."""

    pass
