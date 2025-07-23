from django.urls import path

from StarInTheKitchen.app_users.views import RegisterUserView, LoginUserView, ProfileDeleteView, ProfileView, \
    logout_view, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register-user"),
    path('login/', LoginUserView.as_view(), name="login-user"),
    path('logout/', logout_view, name="logout-user"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile-details"),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit-profile'),
    path('delete_profile/<int:pk>/', ProfileDeleteView.as_view(), name="delete-profile"),

]