from django import forms
from django.core.validators import EmailValidator
from my_validators import my_validators

class Register_form(forms.Form):
    username = forms.CharField(min_length=3, max_length=35, required=True, label='نام کاربری :', widget=forms.TextInput(attrs={
            'minlength' : 3, 'maxlength' : 35,
            'required' : True,
            'placeholder' : 'نام کاربری',
            'class' : 'form-control ltr-just-me',
        }),
        validators=[
            my_validators.validate_username,
        ],
        error_messages={
            'min_length' : 'تعداد حروف نام کاربری نمیتواند کمتر از 3 باشد.',
            'max_length' : 'تعداد حروف نام کاربری نمیتواند بیشتر از 35 باشد.',
            'required' : 'ورود نام کاربری اجباری میباشد.',
            'validators' : 'نام کاربری معتبر نیست! برای ساخت نام کاربری تنها از حروف انگلیسی کوچک و بزرگ، ارقام 0 تا 9، - و _ میتوان استفاده نمود.\nتوجه کنید که حرف اول نام کاربری نمیتواند رقم باشد.',
        })
    email = forms.EmailField(max_length=45, required=True, label='نشانی ایمیل :', widget=forms.TextInput(attrs={
            'maxlength' : 45,
            'required' : True,
            'placeholder' : 'example@example.com',
            'class' : 'form-control ltr-just-me',
        }),
        validators=[
            EmailValidator,
        ],
        error_messages={
            'max_length' : 'تعداد حروف نشانی ایمیل نمیتواند بیشتر از 45 باشد.',
            'required' : 'ورود نشانی ایمیل اجباری میباشد.',
            'validators' : 'نشانی ایمیل به الگوی درستی وارد نشده است! لطفا یک ایمیل معتبر وارد کنید.',
        })
    password = forms.CharField(max_length=60, required=True, label='کلمه عبور :', widget=forms.PasswordInput(attrs={
            'maxlength' : 60,
            'required' : True,
            'placeholder' : 'کلمه عبور',
            'class' : 'form-control',
        }),
        validators=[
            my_validators.validate_password,
            my_validators.is_safe_password,
        ],
        error_messages={
            'max_length' : 'تعداد حروف کلمه عبور نمیتواند بیشتر از 60 باشد.',
            'required' : 'ورود کلمه عبور اجباری میباشد.',
        })
    confirm_password = forms.CharField(max_length=60, required=True, label='تایید کلمه عبور :', widget=forms.PasswordInput(attrs={
            'maxlength' : 60,
            'required' : True,
            'placeholder' : 'تایید کلمه عبور',
            'class' : 'form-control',
        }))

class Login_form(forms.Form):
    email = forms.EmailField(max_length=45, required=True, label='نشانی ایمیل :', widget=forms.TextInput(attrs={
            'maxlength' : 45,
            'required' : True,
            'placeholder' : 'example@example.com',
            'class' : 'form-control ltr-just-me',
        }),
        validators=[
            EmailValidator,
        ],
        error_messages={
            'max_length' : 'تعداد حروف نشانی ایمیل نمیتواند بیشتر از 45 باشد.',
            'required' : 'ورود نشانی ایمیل اجباری میباشد.',
            'validators' : 'نشانی ایمیل به الگوی درستی وارد نشده است! لطفا یک ایمیل معتبر وارد کنید.',
        })
    password = forms.CharField(max_length=60, required=True, label='کلمه عبور :', widget=forms.PasswordInput(attrs={
            'maxlength' : 60,
            'required' : True,
            'placeholder' : 'کلمه عبور',
            'class' : 'form-control',
        }),
        error_messages={
            'max_length' : 'تعداد حروف کلمه عبور نمیتواند بیشتر از 60 باشد.',
            'required' : 'ورود کلمه عبور اجباری میباشد.',
        })

class ForgotPassword_form(forms.Form):
    email = forms.EmailField(max_length=45, required=True, label='نشانی ایمیل :', widget=forms.TextInput(attrs={
            'maxlength' : 45,
            'required' : True,
            'placeholder' : 'example@example.com',
            'class' : 'form-control ltr-just-me',
        }),
        validators=[
            EmailValidator,
        ],
        error_messages={
            'max_length' : 'تعداد حروف نشانی ایمیل نمیتواند بیشتر از 45 باشد.',
            'required' : 'ورود نشانی ایمیل اجباری میباشد.',
            'validators' : 'نشانی ایمیل به الگوی درستی وارد نشده است! لطفا یک ایمیل معتبر وارد کنید.',
        })

class EditPassword_form(forms.Form):
    password = forms.CharField(max_length=60, required=True, label='کلمه عبور :', widget=forms.PasswordInput(attrs={
            'maxlength' : 60,
            'required' : True,
            'placeholder' : 'کلمه عبور',
            'class' : 'form-control',
        }),
        validators=[
            my_validators.validate_password,
            my_validators.is_safe_password,
        ],
        error_messages={
            'max_length' : 'تعداد حروف کلمه عبور نمیتواند بیشتر از 60 باشد.',
            'required' : 'ورود کلمه عبور اجباری میباشد.',
        })
    confirm_password = forms.CharField(max_length=60, required=True, label='تایید کلمه عبور :', widget=forms.PasswordInput(attrs={
            'maxlength' : 60,
            'required' : True,
            'placeholder' : 'تایید کلمه عبور',
            'class' : 'form-control',
        }))