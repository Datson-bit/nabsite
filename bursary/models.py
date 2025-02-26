from django.db import models
from django.conf import settings  # Use the custom user model dynamically
from datetime import date
import uuid

class BursaryApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('ict_cleared', 'Cleared by ICT'),
        ('council_reviewed', 'Reviewed by Councilors'),
        ('hod_approved', 'HOD Approved'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified'),
    ]
    reference_code = models.CharField(max_length=10, unique=True, default="")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  
    full_name = models.CharField(max_length=255, default="")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    address = models.CharField(max_length=255, default="")
    place_of_birth = models.CharField(max_length=255, default="")
    marital_status = models.CharField(max_length=50, default="")
    state_of_origin = models.CharField(max_length=50, default="")
    local_govt_origin = models.CharField(max_length=50, default="")
    ward = models.CharField(max_length=10, default="")
    permanent_address = models.CharField(max_length=255, default="")
    village = models.CharField(max_length=255, default="")
    whatsapp_tel = models.CharField(max_length=20, default="")
    telephone = models.CharField(max_length=20, default="")
    email = models.EmailField(default="")
    dob = models.DateField(default=date.today, null=True, blank=True)
    country_birth = models.CharField(max_length=100, default="")

    # Course & Institution Details
    institution_type = models.CharField(max_length=100, default="")
    course_name = models.CharField(max_length=255, default="")
    institution = models.CharField(max_length=255, default="")
    course_duration = models.CharField(max_length=50, default="")
    inst_address = models.CharField(max_length=255, default="")
    portal_link = models.CharField(max_length=255, default="")
    matric_no = models.CharField(max_length=50, default="")
    portal_username = models.CharField(max_length=100, default="")
    portal_password = models.CharField(max_length=100, default="")
    commencement = models.DateField(default=date.today, null=True, blank=True)
    completion = models.DateField(default=date.today, null=True, blank=True)
    councilor = models.CharField(max_length=255, default="")

    # Education Qualifications
    education = models.JSONField(blank=True, null=True)

    # Declaration and Supporting Documents
    declaration = models.BooleanField(default=False)
    support_docs = models.FileField(upload_to='support_docs/', blank=True, null=True)
    id_card = models.FileField(upload_to='id_cards/', blank=True, null=True)
    admission_letter = models.FileField(upload_to='admission_letters/', blank=True, null=True)
    academic_result = models.FileField(upload_to='academic_results/', blank=True, null=True)
    nabwes_receipt = models.FileField(upload_to='nabwes_receipts/', blank=True, null=True)
    radio_tv_license = models.FileField(upload_to='radio_tv_licenses/', blank=True, null=True)
    letter_of_oba = models.FileField(upload_to='letter_of_oba/', blank=True, null=True)
    origin_certificate = models.FileField(upload_to='origin_certificates/', blank=True, null=True)

    # Workflow fields
    document = models.FileField(upload_to='bursary_documents/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = str(uuid.uuid4().hex[:8]).upper()  # Generates a unique 8-character code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.get_status_display()}"


class ApplicationComment(models.Model):
    STAGE_CHOICES = [
        ('ICT', 'ICT Department'),
        ('Councilors', 'Councilors'),
        ('HOD', 'HOD'),
        ('Chairman', 'Chairman'),
        ('Final', 'Final Remark'),
    ]
    
    application = models.ForeignKey(BursaryApplication, on_delete=models.CASCADE, related_name='comments')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    comment = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.full_name} - {self.get_stage_display()} Comment"
