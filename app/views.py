from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Students,Additional_information
from .forms import StudentForm
import pandas as pd
from django.contrib.auth.decorators import login_required
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Students

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")  # username or email
        password = request.POST.get("password")

        if not identifier or not password:
            messages.error(request, "All fields are required")
            return redirect("login")

        # Check if input is email
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials")
                return redirect("login")
        else:
            username = identifier

  
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    login_image = Additional_information.objects.all()
    return render(request, "login.html",{"login_page_images":login_image})

   # we'll define this below



@login_required(login_url="/login/")
def home(request):
    qs = Students.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(father_name__icontains=q) |
            Q(mother_name__icontains=q) |
            Q(email__icontains=q) |
            Q(mobile_number__icontains=q) |
            Q(roll__icontains=q) |
            Q(reg__icontains=q) |
            Q(session__icontains=q)
        )

    semester = request.GET.get('semester', '').strip()
    if semester:
        qs = qs.filter(semester=semester)

    shift = request.GET.get('shift', '').strip()
    if shift:
        qs = qs.filter(shift=shift)
   

    gender = request.GET.get('gender', '').strip()
    if gender:
        qs = qs.filter(gender=gender)

    blood_group = request.GET.get('blood_group', '').strip()
    if blood_group:
        qs = qs.filter(blood_group=blood_group)

    session = request.GET.get('session', '').strip()
    if session:
        qs = qs.filter(session__icontains=session)

    religion = request.GET.get('religion', '').strip()
    if religion:
        qs = qs.filter(religion__icontains=religion)

    dob_from = request.GET.get('dob_from', '').strip()
    if dob_from:
        parsed = parse_date(dob_from)
        if parsed:
            qs = qs.filter(date_of_birth__gte=parsed)

    dob_to = request.GET.get('dob_to', '').strip()
    if dob_to:
        parsed = parse_date(dob_to)
        if parsed:
            qs = qs.filter(date_of_birth__lte=parsed)

    # ── Default ordering ──
    sort_by = request.GET.get('sort', 'name')
    allowed_sort = {
        'name', 'roll', 'reg', 'semester', 'session',
        'date_of_birth', 'created_at', 'shift', 'gender'
    }
    sort_dir = request.GET.get('dir', 'asc')
    if sort_by not in allowed_sort:
        sort_by = 'name'
    order_field = sort_by if sort_dir != 'desc' else f'-{sort_by}'
    qs = qs.order_by(order_field)

    context = {
        'students': qs,
        'total_count': qs.count(),
        'current_sort': sort_by,
        'current_dir': sort_dir,
        'current_q': q,
    }
    return render(request, 'home.html', context)



def safe_value(val, default=None):
    """Safely extract value from pandas Series"""
    if val is None:
        return default
    if pd.isna(val):
        return default
    if val == "":
        return default
    return val

@csrf_exempt
@require_http_methods(["GET", "POST"])
def upload_students(request):
    """Handle student data upload from CSV/Excel/JSON files"""
    
    if request.method == "GET":
        # Return the HTML template for GET requests
        return render(request, "upload.html")
    
    # Handle POST request for file upload
    try:
        file = request.FILES.get("file")
        
        if not file:
            return JsonResponse({
                "status": "error",
                "message": "No file selected. Please choose a file to upload."
            }, status=400)
        
        # Check file size (max 10MB)
        if file.size > 100 * 1024 * 1024:
            return JsonResponse({
                "status": "error",
                "message": "File too large. Maximum size is 10MB."
            }, status=400)
        
        # Read file based on extension
        file_extension = file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file)
            elif file_extension == 'json':
                df = pd.read_json(file)
            else:
                return JsonResponse({
                    "status": "error",
                    "message": f"Unsupported file format: {file_extension}. Please use CSV, XLSX, or JSON."
                }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Error reading file: {str(e)}"
            }, status=400)
        
        if df.empty:
            return JsonResponse({
                "status": "error",
                "message": "The file is empty. Please upload a file with data."
            }, status=400)
        
        # Expected columns
        expected_columns = [
            'name', 'father_name', 'mother_name', 'date_of_birth', 'gender', 
            'blood_group', 'semester', 'roll', 'reg', 'session', 'shift', 
            'section', 'mobile_number', 'alternate_mobile', 'email', 
            'present_address', 'permanent_address', 'emergency_contact_name', 
            'emergency_contact_number', 'nationality', 'religion'
        ]
        
        # Check for missing columns
        actual_columns = [col.lower() for col in df.columns]
        missing_columns = [col for col in expected_columns if col.lower() not in actual_columns]
        
        if missing_columns:
            return JsonResponse({
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns[:5])}",
                "missing_columns": missing_columns
            }, status=400)
        
        # Process each row
        students_created = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Parse date of birth
                dob_value = safe_value(row.get("date_of_birth"))
                dob = None
                if dob_value:
                    try:
                        dob = pd.to_datetime(dob_value).date()
                    except Exception as e:
                        errors.append(f"Row {index + 2}: Invalid date format '{dob_value}'")
                        continue
                
                # Create student object
                student = Students(
                    name=str(safe_value(row.get("name"), ""))[:100],
                    father_name=str(safe_value(row.get("father_name"), ""))[:100],
                    mother_name=str(safe_value(row.get("mother_name"), ""))[:100],
                    date_of_birth=dob,
                    gender=safe_value(row.get("gender"), "O")[:1] if safe_value(row.get("gender"), "O") else "O",
                    blood_group=str(safe_value(row.get("blood_group"), ""))[:5] if safe_value(row.get("blood_group")) else None,
                    semester=int(safe_value(row.get("semester"), 0)),
                    roll=int(safe_value(row.get("roll"), 0)),
                    reg=int(safe_value(row.get("reg"), 0)),
                    session=str(safe_value(row.get("session"), ""))[:20],
                    shift=str(safe_value(row.get("shift"), "Day"))[:10],
                    section=str(safe_value(row.get("section"), ""))[:5] if safe_value(row.get("section")) else None,
                    mobile_number=str(safe_value(row.get("mobile_number"), ""))[:15],
                    alternate_mobile=str(safe_value(row.get("alternate_mobile"), ""))[:15] if safe_value(row.get("alternate_mobile")) else None,
                    email=str(safe_value(row.get("email"), ""))[:254] if safe_value(row.get("email")) else None,
                    present_address=str(safe_value(row.get("present_address"), ""))[:500],
                    permanent_address=str(safe_value(row.get("permanent_address"), ""))[:500],
                    emergency_contact_name=str(safe_value(row.get("emergency_contact_name"), ""))[:100],
                    emergency_contact_number=str(safe_value(row.get("emergency_contact_number"), ""))[:15],
                    nationality=str(safe_value(row.get("nationality"), "Bangladeshi"))[:50],
                    religion=str(safe_value(row.get("religion"), ""))[:30] if safe_value(row.get("religion")) else None,
                )
                
                # Validate required fields
                if not student.name:
                    errors.append(f"Row {index + 2}: Name is required")
                    continue
                    
                if student.roll == 0:
                    errors.append(f"Row {index + 2}: Roll number is required")
                    continue
                    
                if student.reg == 0:
                    errors.append(f"Row {index + 2}: Registration number is required")
                    continue
                
                if not student.email:
                    errors.append(f"Row {index + 2}: Email is required")
                    continue
                
                # Check for duplicates before saving
                if Students.objects.filter(roll=student.roll).exists():
                    errors.append(f"Row {index + 2}: Roll number {student.roll} already exists")
                    continue
                    
                if Students.objects.filter(reg=student.reg).exists():
                    errors.append(f"Row {index + 2}: Registration number {student.reg} already exists")
                    continue
                    
                if student.email and Students.objects.filter(email=student.email).exists():
                    errors.append(f"Row {index + 2}: Email {student.email} already exists")
                    continue
                
                student.save()
                students_created.append(student)
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
                continue
        
        # Return response
        if students_created:
            return JsonResponse({
                "status": "success",
                "message": f"Successfully uploaded {len(students_created)} students!",
                "count": len(students_created),
                "total_rows": len(df),
                "errors": errors[:10],  # Show first 10 errors
                "error_count": len(errors)
            })
        else:
            error_msg = "No students could be uploaded. " + (errors[0] if errors else "Please check your file format.")
            return JsonResponse({
                "status": "error",
                "message": error_msg,
                "errors": errors[:10]
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, status=500)