import random, string
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseServerError, HttpRequest
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.db.models import Q
from django.contrib.auth import login, logout
from . import forms, models

# Create your views here.

class Register_view(FormView):
    template_name = 'account_module/register.html'
    form_class = forms.Register_form
    success_url = reverse_lazy('login_page')

    def form_valid(self, form: forms.Register_form):
        if form.cleaned_data.get('password') != form.cleaned_data.get('confirm_password'):
            form.add_error('confirm_password', error='کلمه عبور و تایید کلمه عبور باهم نابرابر هستند! لطفا دوباره امتحان کنید.')
            return self.form_invalid(form)
        if models.User.objects.filter(Q(username=form.cleaned_data.get('username')) | Q(email=form.cleaned_data.get('email'))):
            form.add_error(None, error='نام کاربری یا نشانی ایمیل وارد شده قبلا در این سایت ثبت شده و تکراری هستند. نمیتوانید برای ثبت نام از نام کاربری یا نشانی ایمیل تکراری استفاده کنید. چنانچه کلمه عبور خود را فراموش کرده اید، از بخش "فراموشی کلمه عبور" اقدام نمایید.')
            return self.form_invalid(form)
        user = models.User(username=form.cleaned_data.get('username'), email=form.cleaned_data.get('email'))
        user.set_password(form.cleaned_data.get('password'))
        flag = False
        for i in range(5):
            email_active_code = ''.join(random.choices(string.ascii_letters + string.digits, k=75))
            user.email_active_code = email_active_code
            try:
                user.save()
                flag = True
                break
            except:
                pass
        if not flag:
            form.add_error(None, error='در روند ثبت نام مشکلی پیش آمد! لطفا بعدا دوباره امتحان کنید.')
            return self.form_invalid(form)
        # TODO : send email
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard_page')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard_page')
        return super().post(request, *args, **kwargs)

class Login_view(FormView):
    template_name = 'account_module/login.html'
    form_class = forms.Login_form
    success_url = reverse_lazy('dashboard_page')

    def form_valid(self, form: forms.Login_form):
        user = models.User.objects.filter(email=form.cleaned_data.get('email')).last()
        if not user or not user.check_password(form.cleaned_data.get('password')):
            form.add_error(None, 'نام کاربری یا کلمه عبور اشتباه میباشد! چنانچه کلمه عبور خود را فراموش نموده اید، میتوانید از قسمت فراموشی کلمه عبور اقدام کنید.')
            return self.form_invalid(form)
        if not user.is_active:
            form.add_error(None, 'حساب کاربری هنوز فعال نشده است. لطفا به ایمیل خود مراجعه کنید و یا از قسمت فراموشی کلمه عبور اقدام کنید.')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('home_page')

def account_activation(request, email_active_code):
    user = models.User.objects.filter(email_active_code=email_active_code).last()
    if not user:
        raise Http404()
    flag = False
    for i in range(5):
        user.email_active_code = ''.join(random.choices(string.ascii_letters + string.digits, k=75))
        user.is_active = True
        try:
            user.save()
            flag = True
            break
        except:
            pass
    if not flag:
        return HttpResponseServerError()
    return redirect('login_page')

class ForgotPassword_view(View):
    send_email_template_name = 'account_module/forgot_password_send_email.html'
    edit_password_template_name = 'account_module/forgot_password_edit_password.html'

    # def get(self, request: HttpRequest):
    #     if request.user.is_authenticated:
    #         return redirect('dashboard_page')
    #     form = forms.ForgotPassword_form()
    #     return render(request, self.send_email_template_name, context={'form' : form})

    # def post(self, request: HttpRequest):
    #         if request.user.is_authenticated:
    #             return redirect('dashboard_page')
    #         form = forms.ForgotPassword_form(request.POST)
    #         if form.is_valid():
    #             user = models.User.objects.filter(email=form.cleaned_data.get('email')).last()
    #             if user:
    #                 if user.email_active_code:
    #                     # TODO : send email
    #                     pass
    #                 else:
    #                     return render(request, self.send_email_template_name, context={'cant_active' : True})
    #             return render(request, self.send_email_template_name)
    #         return render(request, self.send_email_template_name, context={'form' : form})

    def get(self, request: HttpRequest, email_active_code: str | None = None):
        if email_active_code is not None:
            if request.user.is_authenticated or email_active_code == '':
                raise Http404()
            user = models.User.objects.filter(email_active_code=email_active_code).last()
            if not user:
                raise Http404()
            form = forms.EditPassword_form()
            return render(request, self.edit_password_template_name, context={'form' : form})
        
        # email active code didn't enter
        if request.user.is_authenticated:
            return redirect('dashboard_page')
        form = forms.ForgotPassword_form()
        return render(request, self.send_email_template_name, context={'form' : form})
        
    def post(self, request: HttpRequest, email_active_code: str | None = None):
        if email_active_code is not None:
            if request.user.is_authenticated or email_active_code == '':
                raise Http404()
            form = forms.EditPassword_form(request.POST)
            if form.is_valid():
                if form.cleaned_data.get('password') != form.cleaned_data.get('confirm_password'):
                    form.add_error('confirm_password', 'کلمه عبور و تایید کلمه عبور باهم نابرابر هستند! لطفا دوباره امتحان کنید.')
                    return render(request, self.edit_password_template_name, context={'form' : form})
                user = models.User.objects.filter(email_active_code=email_active_code).last()
                if user:
                    user.set_password(form.cleaned_data.get('password'))
                    for i in range(5):
                        try:
                            user.email_active_code = ''.join(random.choices(string.ascii_letters + string.digits, k=75))
                            user.is_active = True
                            user.save()
                        except:
                            user.is_active = False
                    if not user.is_active:
                        return render(request, self.edit_password_template_name)
                    return redirect('login_page')
                raise Http404()
            return render(request, self.edit_password_template_name, context={'form' : form})

        # email active code didn't enter
        if request.user.is_authenticated:
            return redirect('dashboard_page')
        form = forms.ForgotPassword_form(request.POST)
        if form.is_valid():
            user = models.User.objects.filter(email=form.cleaned_data.get('email')).last()
            if user:
                if user.email_active_code:
                    # TODO : send email
                    pass
                else:
                    return render(request, self.send_email_template_name, context={'cant_active' : True})
            return render(request, self.send_email_template_name)
        return render(request, self.send_email_template_name, context={'form' : form})
