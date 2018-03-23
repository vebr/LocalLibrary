from django.forms import ModelForm, DateInput, Select
from .models import BookInstance

class BorrowForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ('status', 'due_back')
        widgets = {
        	'status' : Select(attrs={'id': 'filesB'}),
            'due_back' : DateInput(format='%d/%m/%Y',attrs={'id': 'datepicker'}),
        }