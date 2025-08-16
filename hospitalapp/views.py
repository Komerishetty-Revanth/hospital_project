from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import Hospital, Receiver, BloodSample, BloodRequest, Campaign, DonorRegistration
from .forms import HospitalRegistrationForm, ReceiverRegistrationForm, BloodSampleForm, CampaignForm


# ----------------- HOME -----------------
def home(request):
    samples = BloodSample.objects.all().order_by('-date_added')
    return render(request, 'hospitalapp/home.html', {'samples': samples})


# ----------------- REGISTRATION -----------------
def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Hospital.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                location=form.cleaned_data['location'],
                specialization=form.cleaned_data['specialization'],
                contact_number=form.cleaned_data['contact_number']
            )
            messages.success(request, "Hospital registered successfully. Please login.")
            return redirect('login')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'hospitalapp/hospital_register.html', {'form': form})


def receiver_register(request):
    if request.method == 'POST':
        form = ReceiverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Receiver.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                blood_group=form.cleaned_data['blood_group'],
                contact_number=form.cleaned_data['contact_number']
            )
            messages.success(request, "Receiver registered successfully. Please login.")
            return redirect('login')
    else:
        form = ReceiverRegistrationForm()
    return render(request, 'hospitalapp/receiver_register.html', {'form': form})


# ----------------- BLOOD SAMPLE (Hospital only) -----------------
@login_required
def add_blood_info(request):
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return render(request, "hospitalapp/not_hospital.html")

    if request.method == 'POST':
        form = BloodSampleForm(request.POST)
        if form.is_valid():
            blood_sample = form.save(commit=False)
            blood_sample.hospital = hospital
            blood_sample.save()
            messages.success(request, "Blood sample added successfully.")
            return redirect('available_samples')
    else:
        form = BloodSampleForm()
    return render(request, 'hospitalapp/add_blood_info.html', {'form': form})


@login_required
def available_samples(request):
    samples = BloodSample.objects.all()

    requested_samples_ids = []
    if hasattr(request.user, 'receiver'):
        requested_samples_ids = list(
            BloodRequest.objects.filter(receiver=request.user).values_list('blood_sample_id', flat=True)
        )

    return render(request, 'hospitalapp/available_samples.html', {
        'samples': samples,
        'requested_samples_ids': requested_samples_ids
    })


# ----------------- BLOOD REQUESTS (Receiver only) -----------------
@login_required
def request_sample(request, sample_id):
    sample = get_object_or_404(BloodSample, id=sample_id)

    # Only receivers can request
    if not hasattr(request.user, 'receiver'):
        return render(request, 'hospitalapp/not_receiver.html')

    # Prevent duplicate requests
    if BloodRequest.objects.filter(receiver=request.user, blood_sample=sample).exists():
        return render(request, 'hospitalapp/already_requested.html', {'sample': sample})

    BloodRequest.objects.create(
        receiver=request.user,
        blood_sample=sample,
        status="Pending"
    )
    messages.success(request, "Request submitted successfully.")
    return redirect('available_samples')


# ----------------- HOSPITAL REQUEST MANAGEMENT -----------------
@login_required
def view_requests(request):
    try:
        hospital = request.user.hospital
    except Hospital.DoesNotExist:
        return render(request, 'hospitalapp/not_hospital.html')

    requests = BloodRequest.objects.filter(blood_sample__hospital=hospital)
    return render(request, 'hospitalapp/view_request.html', {'requests': requests})


@login_required
def update_request_status(request, request_id, status):
    req = get_object_or_404(BloodRequest, id=request_id)

    if hasattr(request.user, 'hospital') and req.blood_sample.hospital == request.user.hospital:
        if status in ['Approved', 'Rejected']:
            req.status = status
            req.save()
            messages.success(request, f"Request {status.lower()} successfully.")
        else:
            messages.error(request, "Invalid status.")
    else:
        messages.error(request, "You are not authorized to perform this action.")

    return redirect('view_requests')


# ----------------- CAMPAIGNS -----------------
def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "hospitalapp/campaign.html", {"campaigns": campaigns})

# Create campaign
def campaign_create(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("campaign_list")
    else:
        form = CampaignForm()
    return render(request, "hospitalapp/add_campaign.html", {"form": form})

# Campaign detail view (optional)
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    return render(request, "hospitalapp/campaign_detail.html", {"campaign": campaign})

# ----------------- LOGOUT -----------------
def logout_view(request):
    logout(request)
    return render(request, 'hospitalapp/logout.html')
