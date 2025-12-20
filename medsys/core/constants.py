ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
REGEX_PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
REGEX_PHONE_PATTERN = r'(\+7|8)\d{10}'
STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
ADD_ALLOWED_TABLES = {
    "patients",
    "visits",
    "medical_records",
    "lab_tests",
    "diagnoses",
    "prescriptions",
    "medications",
    "prescription_medications",
}