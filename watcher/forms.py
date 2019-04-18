from django import forms
from .models import Room

class RoomForm(forms.ModelForm):

    contact = forms.BooleanField(help_text="가맹점은 체크하세요",required=False)
    class Meta:
        model = Room
        fields = ('name', 'address', 'contact','latitude', 'longitude', 'notice', 'spec')


