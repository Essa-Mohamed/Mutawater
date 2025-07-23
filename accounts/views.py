from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

def enter_name(request):
    """
    الصفحة الأولى: يطلب فيها الاسم ثم يُعيد توجيه المستخدم لصفحة home.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            request.session['student_name'] = name
            return redirect('home')
    return render(request, 'accounts/enter_name.html')

def home(request):
    """
    الصفحة الرئيسية: ترحب بالمستخدم باسمه المخزّن في الجلسة.
    إذا لم يكن هناك اسم في الجلسة، يعيد التوجيه لصفحة enter_name.
    """
    name = request.session.get('student_name')
    if not name:
        return redirect('enter_name')
    return render(request, 'home.html', {'student_name': name})

def logout(request):
    """
    عند الضغط على خروج: نُخرج المستخدم (إذا كنت تستخدم auth)
    ثم نعيد توجيهه إلى صفحة إدخال الاسم.
    """
    auth_logout(request)
    return redirect('enter_name')
