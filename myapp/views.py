from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages
from .models import Patient
from .forms import PatientForm
from predict import predict_disease
from django.shortcuts import get_object_or_404
from rf_predict import predict_rf
from gradcam import generate_gradcam
from report_generator import generate_medical_report

def register_view(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            messages.success(
                request,
                'Registration Successful!'
            )            

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, 'login.html')

def home_view(request):

    total_patients = Patient.objects.count()

    normal_count = Patient.objects.filter(
        rf_disease='Normal Uterus'
    ).count()

    fibroid_count = Patient.objects.filter(
        rf_disease='Fibroid'
    ).count()

    adenomyosis_count = Patient.objects.filter(
        rf_disease='Adenomyosis'
    ).count()

    cancer_count = Patient.objects.filter(
        rf_disease='Endometrial Cancer'
    ).count()

    patients = Patient.objects.all()

    recent_patients = Patient.objects.order_by(
        '-created_at'
    )[:10]

    context = {
        'total_patients': total_patients,
        'normal_count': normal_count,
        'fibroid_count': fibroid_count,
        'adenomyosis_count': adenomyosis_count,
        'cancer_count': cancer_count,
        'patients': patients,
        'recent_patients': recent_patients,
    }

    return render(
        request,
        'home.html',
        context
    )

def logout_view(request):
    logout(request)
    return redirect('login')

def add_patient(request):

    if request.method == 'POST':

        form = PatientForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            patient = form.save(commit=False)

            patient.save()

            form.save_m2m()

            if patient.image:

                cnn_prediction = predict_disease(
                    patient.image.path
                )

                rf_prediction,confidence_score = predict_rf(
                    patient.image.path
                )

                if rf_prediction != "Normal Uterus":
                    gradcam_path = generate_gradcam(patient.image.path)
                    patient.gradcam_image = gradcam_path


                patient.disease = cnn_prediction
                patient.rf_disease = rf_prediction
                patient.confidence_score = confidence_score
                patient.save()

            return redirect('view_patient',id=patient.id)

    else:
        form = PatientForm()

    return render(
        request,
        'add_patient.html',
        {'form': form}
    )

def view_patients(request):
    patients = Patient.objects.all().order_by('-created_at')

    return render(
        request,
        'view_patients.html',
        {'patients': patients}
    )

def view_patient(request, id):

    patient = Patient.objects.get(id=id)

    return render(
        request,
        'view_patient.html',
        {'patient': patient}
    )
def edit_patient(request, id):

    patient = Patient.objects.get(id=id)

    if request.method == 'POST':

        form = PatientForm(
            request.POST,
            request.FILES,
            instance=patient
        )

        if form.is_valid():

            updated_patient = form.save(commit=False)

            if request.FILES.get('image'):

                updated_patient.image = request.FILES['image']

            else:

                updated_patient.image = patient.image

            updated_patient.save()

            form.save_m2m()

            if updated_patient.image:

                cnn_prediction = predict_disease(
                    patient.image.path
                )

                rf_prediction, confidence_score = predict_rf(
                    patient.image.path
                )

                if rf_prediction != "Normal Uterus":
                    gradcam_path = generate_gradcam(patient.image.path)
                    patient.gradcam_image = gradcam_path


                patient.disease = cnn_prediction

                patient.rf_disease = rf_prediction
                patient.confidence_score = confidence_score

                updated_patient.save()

            return redirect('view_patient',id=patient.id)

    else:

        form = PatientForm(instance=patient)

    return render(
        request,
        'edit_patient.html',
        {
            'form': form,
            'patient': patient
        }
    )



def delete_patient(request, id):

    patient = Patient.objects.get(id=id)
    patient.delete()
    return redirect('view_patients')


def generate_report(request, id):

    patient = Patient.objects.get(id=id)

    report = generate_medical_report(patient)

    patient.ai_report = report
    patient.save()

    return redirect('report_view', id=id)

def report_view(request, id):

    patient = Patient.objects.get(id=id)

    return render(
        request,
        'report.html',
        {'patient': patient}
    )