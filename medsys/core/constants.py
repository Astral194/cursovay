ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
REGEX_PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
REGEX_PHONE_PATTERN = r'^\+?\d{1,3}?[-\s]?\(?\d{1,4}?\)?[-\s]?\d{3,4}[-\s]?\d{2,4}$'
STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )