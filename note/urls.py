from django.urls import path
from .views import *
from . import views
from django.contrib.auth.views import LogoutView

app_name = "note"
urlpatterns = [
    # path('get_notes/', NoteGetView.as_view(), name='get_notes'),
    path('update_note/<int:pk>/', NoteUpdateView.as_view(), name='update_note'),
    path('delete_note/<int:pk>/', NoteDeleteView.as_view(), name='delete_note'),
    path('base/', LoginService.as_view(), name='base'),
    path('logout/', LogoutView.as_view(next_page="authentication:login"), name="logout"),
    path('home/', HomeView.as_view(), name='home'),
    path('get_notes/<str:noteBoardName>/', NoteGetView.as_view(), name='get_notes'),
    path('<str:board>/', NoteView.as_view(), name='note'),
]
