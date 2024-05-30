from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import SignUpForm, AddBlogForm
from django.contrib.auth.decorators import login_required
from .models import Blog
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.views.generic import DetailView
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'blogg/registration/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'blogg/registration/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form, 'error': 'Invalid username or password'})

class DashboardView(TemplateView):
    template_name = 'blogg/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['blogs'] = Blog.objects.all()  # Retrieve all blogs
        return context

def custom_logout(request):
    if request.method == 'POST':
        #perform the logout
        logout(request)
    return redirect('home') 
    

# Create your views here.
def home(request):
    return render(request, 'blogg/home.html')

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = AddBlogForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            print("New blog saved successfully:", new_blog.title)  
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            print("Form is not valid:", form.errors)
    else:
        form = AddBlogForm()
    return redirect('dashboard')


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog.")

    if request.method == 'POST':
        form = AddBlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddBlogForm(instance=blog)
    
    return render(request, 'blogg/edit_blog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog.")

    if request.method == 'POST':
        blog.delete()
        return redirect('dashboard')
    
    return render(request, 'blogg/confirm_delete.html', {'blog': blog})

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'blogg/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogg/blogpage.html'
    context_object_name = 'blog'