from django.shortcuts import render, redirect
from .forms import ScopeForm

def select_scope(request):
    if request.method == 'POST':
        form = ScopeForm(request.POST)
        if form.is_valid():
            # خزّن الاختيارات في السِّشن عشان تستخدمها في الـ steps اللي بعدها
            request.session['scope'] = {
                'juzs':     [j.id for j in form.cleaned_data['juzs']],
                'hizbs':    [h.id for h in form.cleaned_data['hizbs']],
                'quarters': [q.id for q in form.cleaned_data['quarters']],
            }
            return redirect('exams:select_type')
    else:
        form = ScopeForm()

    return render(request, 'exams/select_scope.html', {'form': form})
