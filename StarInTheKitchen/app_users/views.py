from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from StarInTheKitchen.app_users.forms import AppUserForm, EditAppUserForm
from StarInTheKitchen.app_users.models import Profile

AppUserModel = get_user_model()


class RegisterUserView(UserPassesTestMixin, CreateView):
    model = AppUserModel
    form_class = AppUserForm
    template_name = 'app_users/register_page.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class LoginUserView(UserPassesTestMixin, LoginView):
    template_name = 'app_users/login_page.html'
    success_url = reverse_lazy('home-page')


class ProfileView(LoginRequiredMixin, UpdateView, DetailView):
    model = Profile
    form_class = EditAppUserForm

    def get_template_names(self):
        user = self.request.user

        if user.profile.id == self.kwargs['pk']:
            return ['app_users/edit_profile.html']

        return ['app_users/profile_page.html']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['form'].fields['email'].initial = self.request.user.email
#         context['emergency_events'] = get_emergency_events()
#         context['video_url'] = config('VIDEO_URL')
#
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('profile-details-update', kwargs={
#             'pk': self.object.id
#         })
#
#
# def delete_profile_view(request):
#     if not request.user.is_authenticated:
#         raise Http404()
#
#     user_profile = request.user.profile
#     form = DeleteAppUserForm(instance=user_profile)
#     form.fields['email'].initial = user_profile.user.email
#
#     if request.method == "POST":
#         request.user.delete()
#         return redirect('home-page')
#
#     context = {
#         'form': form,
#         'emergency_events': get_emergency_events(),
#         'video_url': config('VIDEO_URL')
#     }
#
#     return render(request, 'app_users/delete_profile.html', context=context)
#
#
# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#
#     return redirect('home-page')
#
#
