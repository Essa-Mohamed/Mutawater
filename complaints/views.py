# complaints/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Complaint
from .forms import ComplaintForm


@login_required
def create_complaint(request):
    """
    عرض نموذج كتابة شكوى وحفظها.
    """
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()
            return redirect('complaints:list_complaints')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/create.html', {
        'form': form
    })


@login_required
def list_complaints(request):
    """
    عرض قائمة الشكاوى الخاصة بالمستخدم الحالي.
    """
    complaints = Complaint.objects.filter(student=request.user).order_by('-created')
    return render(request, 'complaints/list.html', {
        'complaints': complaints
    })
