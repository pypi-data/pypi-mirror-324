from django import forms

class TelegramAuthenticationForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите username или Telegram ID'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Требуется указать username или Telegram ID')
        return cleaned_data