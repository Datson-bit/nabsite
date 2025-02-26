from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import BursaryApplication, ApplicationComment
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib import messages
# def home(request):
#         return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .models import BursaryApplication

def bursary_form(request):
    if request.method == 'POST':
        # Personal Details
        full_name = request.POST.get('fullName')
        address = request.POST.get('Address-sch')
        place_of_birth = request.POST.get('nric')
        marital_status = request.POST.get('gender')
        state_of_origin = request.POST.get('stateOfOrigin')
        local_govt_origin = request.POST.get('origin-lga')
        ward = request.POST.get('ward')
        permanent_address = request.POST.get('homeAddress')
        village = request.POST.get('mailingAddress')
        whatsapp_tel = request.POST.get('resTel')
        telephone = request.POST.get('handphone')
        email = request.POST.get('email')

        # Convert Date Fields
        dob = request.POST.get('dob')
        commencement = request.POST.get('commencement')
        completion = request.POST.get('completion')

        dob = datetime.strptime(dob, '%Y-%m-%d').date() if dob else None
        commencement = datetime.strptime(commencement, '%Y-%m-%d').date() if commencement else None
        completion = datetime.strptime(completion, '%Y-%m-%d').date() if completion else None

        country_birth = request.POST.get('countryBirth')

        # Course & Institution Details
        institution_type = request.POST.get('appType')
        course_name = request.POST.get('courseName')
        institution = request.POST.get('institution')
        course_duration = request.POST.get('courseDuration')
        inst_address = request.POST.get('instAddress')
        portal_link = request.POST.get('portal_link')  
        matric_no = request.POST.get('matric_no')     
        portal_username = request.POST.get('portal_username')
        portal_password = request.POST.get('portal_password')
        councilor = request.POST.get('councilor')

        # File Uploads
        photo = request.FILES.get('photo')
        support_docs = request.FILES.get('supportDocs')

        id_card = request.FILES.get('idCard')
        admission_letter = request.FILES.get('admissionLetter')
        academic_result = request.FILES.get('academicResult')
        nabwes_receipt = request.FILES.get('nabwesReceipt')
        radio_tv_license = request.FILES.get('radioTvLicense')
        letter_of_oba = request.FILES.get('letterOfOba')
        origin_certificate = request.FILES.get('originCertificate')

        # Create and Save Application
        application = BursaryApplication.objects.create(
            full_name=full_name,
            photo=photo,
            address=address,
            place_of_birth=place_of_birth,
            marital_status=marital_status,
            state_of_origin=state_of_origin,
            local_govt_origin=local_govt_origin,
            ward=ward,
            permanent_address=permanent_address,
            village=village,
            whatsapp_tel=whatsapp_tel,
            telephone=telephone,
            email=email,
            dob=dob,
            country_birth=country_birth,
            institution_type=institution_type,
            course_name=course_name,
            institution=institution,
            course_duration=course_duration,
            inst_address=inst_address,
            portal_link=portal_link,
            matric_no=matric_no,
            portal_username=portal_username,
            portal_password=portal_password,
            commencement=commencement,
            completion=completion,
            councilor=councilor,
            support_docs=support_docs,
            declaration=('declaration' in request.POST),
            id_card=id_card,
            admission_letter=admission_letter,
            academic_result=academic_result,
            nabwes_receipt=nabwes_receipt,
            radio_tv_license=radio_tv_license,
            letter_of_oba=letter_of_oba,
            origin_certificate=origin_certificate,
        )

        # Send email with reference code
        send_mail(
            "Your Application Reference Code",
            f"Dear {application.full_name},\n\nYour application has been received!\nYour tracking code: {application.reference_code}\nUse this code to check your status.",
            "bursary@nabwes.com.ng",
            [email],
            fail_silently=False
        )

        messages.success(request, "Application submitted! Check your email for the tracking code.")
        
        # Redirect properly to success page
        return redirect("application_success", reference_code=application.reference_code)

    return render(request, 'bursary_form.html')

def track_application(request):
    reference_code = request.GET.get("reference_code", "").upper()

    if not reference_code:  
        # If no reference code is provided, show the input form
        return render(request, "track_application.html")

    application = BursaryApplication.objects.filter(reference_code=reference_code).first()

    if application:
        return render(request, "application_status.html", {"application": application})
    else:
        messages.error(request, "Invalid reference code. Please try again.")
        return render(request, "track_application.html")  # Render instead of redirect


def success_page(request, reference_code):
    full_name = request.GET.get('full_name', '')  # Get full_name from query params
    return render(request, 'success_page.html', {'full_name': full_name, 'reference_code': reference_code})



@login_required
def dashboard(request):
    """Main dashboard view with role-based filtering."""
    user_role = request.user.role  # Assuming we are using a custom user model

    # Show applications based on user role
    if user_role == "ICT":
        applications = BursaryApplication.objects.filter(status="submitted")
    elif user_role == "COUNCILOR":
        applications = BursaryApplication.objects.filter(status="ict_cleared")
    elif user_role == "HOD":
        applications = BursaryApplication.objects.filter(status="council_reviewed")
    elif user_role == "CHAIRMAN":
        applications = BursaryApplication.objects.filter(status="hod_approved")
    else:
        applications = BursaryApplication.objects.filter(applicant=request.user)  # Show only the applicant’s submission

    context = {
        "applications": applications,
        "user_role": user_role
    }
    return render(request, "dashboard1.html", context)


@login_required
def application_detail(request, application_id):
    """Detailed view of a bursary application."""
    application = get_object_or_404(BursaryApplication, id=application_id)

    if request.method == "POST":
        comment_text = request.POST.get("comment", "").strip()
        if comment_text:
            ApplicationComment.objects.create(
                application=application,
                stage=request.user.role,
                comment=comment_text,
                author=request.user
            )
            messages.success(request, "Comment added successfully!")

    comments = application.comments.all()
    return render(request, "application_detail.html", {"application": application, "comments": comments})


def approve_application(request, application_id):
    application = get_object_or_404(BursaryApplication, id=application_id)

    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        action = request.POST.get("action")  # "approve" or "disapprove"

        # Determine new status based on current status, user role, and action.
        if request.user.role == "ICT" and application.status == "submitted":
            new_status = "ict_cleared"
            stage = "ICT"
        elif request.user.role == "COUNCILOR" and application.status == "ict_cleared":
            new_status = "council_reviewed"
            stage = "Councilors"
        elif request.user.role == "HOD" and application.status == "council_reviewed":
            new_status = "hod_approved"
            stage = "HOD"
        elif request.user.role == "CHAIRMAN" and application.status == "hod_approved":
            # Chairman makes the final decision
            final_remark = request.POST.get("final_remark")
            if final_remark in ["qualified", "disqualified"]:
                new_status = final_remark
                stage = "Final"
            else:
                messages.error(request, "Invalid final decision.")
                return redirect("dashboard")
        else:
            messages.error(request, "You are not authorized to update this application.")
            return redirect("dashboard")

        # Update application status
        application.status = new_status
        application.save()

        # Save comment if provided
        if comment:
            ApplicationComment.objects.create(
                application=application,
                stage=stage,
                comment=comment,
                author=request.user
            )

        # Send email notification
        send_mail(
            subject=f"Bursary Application Update - {application.get_status_display()}",
            message=f"Dear {application.full_name},\n\nYour application status has been updated to {application.get_status_display()}.\n\nBest regards,\nBursary Committee",
            from_email="bursary@nabwes.com.ng",  # Replace with your email
            recipient_list=[application.email],
            fail_silently=True,
        )

        messages.success(request, "Application updated successfully.")
        return redirect("dashboard")

    return redirect("dashboard")


@login_required
def disapprove_application(request, application_id):
    application = get_object_or_404(BursaryApplication, id=application_id)

    # Only allow roles to disapprove
    if request.user.role in ["ICT", "HOD", "COUNCILOR", "CHAIRMAN"]:
        application.status = "disqualified"
        application.save()
        messages.success(request, "Application has been disqualified.")
    else:
        messages.error(request, "You are not authorized to disapprove this application.")

    return redirect('application_detail', application_id=application.id)