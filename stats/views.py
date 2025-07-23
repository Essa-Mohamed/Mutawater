from django.shortcuts import render

def overview(request):
    # لاحقاً هنجيب بيانات الإحصائيات الفعلية من الـ models
    return render(request, 'stats/overview.html', {
        # تمرير أي بيانات أولية هنا
    })
