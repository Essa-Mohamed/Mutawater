from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.enter_name, name='enter_name'),
    path('home/', accounts_views.home, name='home'),
    path('logout/', accounts_views.logout, name='logout'),

    path('admin/', admin.site.urls),
    path('exams/', include(('exams.urls', 'exams'), namespace='exams')),
    path('complaints/', include(('complaints.urls', 'complaints'), namespace='complaints')),
    # لو عندك إحصائيات أيضاً:
    path('stats/', include(('stats.urls', 'stats'), namespace='stats')),
]
