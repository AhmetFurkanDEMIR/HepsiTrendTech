from django import forms

class RegisterForm(forms.Form):

    username = forms.CharField(max_length=50, required=True, label="Ad")
    user_surname = forms.CharField(max_length=50, required=True, label="Soyad")
    user_email = forms.EmailField(max_length=50, required=True, label="Mail adresi")
    user_phone = forms.CharField(max_length=50, required=True, label="Telefon numarası")

    erken_erisim = forms.CharField(max_length=50, required=True, label="Erken erişim kodu")

    password = forms.CharField(max_length=30, label="Şifre", widget=forms.PasswordInput, required=True)
    confirm = forms.CharField(max_length=30, label="Şifreyi doğrula", widget=forms.PasswordInput, required=True)

    def clean(self):

        username = self.cleaned_data.get("username")
        user_surname = self.cleaned_data.get("user_surname")
        user_email = self.cleaned_data.get("user_email")
        user_phone = self.cleaned_data.get("user_phone")
        erken_erisim = self.cleaned_data.get("erken_erisim")

        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        
        if password and confirm and password != confirm:

            raise forms.ValidationError("Şifreler eşleşmiyor.")

        values = {

            "username" : username,
            "user_surname" : user_surname,
            "user_email" : user_email,
            "user_phone" : user_phone,
            "password" : password,
            "erken_erisim" : erken_erisim
        }

        return values

class LoginForm(forms.Form):

    user_email = forms.CharField(max_length=50, label="Mail adresi")
    password = forms.CharField(max_length=30, label="Şifre", widget=forms.PasswordInput)


class UpdateUser(forms.Form):

    username = forms.CharField(max_length=50, required=True, label="Ad")
    user_surname = forms.CharField(max_length=50, required=True, label="Soyad")

    password = forms.CharField(max_length=20, label="Şifre", widget=forms.PasswordInput, required=True)

    user_email = forms.EmailField(max_length=50, required=False, disabled = True, label="Mail adresi")
    user_phone = forms.CharField(max_length=50, required=False, disabled = True, label="Telefon numarası")
    