from django import forms
from .models import Students


class StudentForm(forms.ModelForm):

    class Meta:
        model = Students
        fields = [
            # Personal
            'name', 'father_name', 'mother_name',
            'date_of_birth', 'gender', 'blood_group',
            'nationality', 'religion', 'profile_picture',
            # Academic
            'semester', 'roll', 'reg', 'session', 'shift', 'section',
            # Contact
            'mobile_number', 'alternate_mobile', 'email',
            'present_address', 'permanent_address',
            # Emergency
            'emergency_contact_name', 'emergency_contact_number',
        ]
        widgets = {
            'date_of_birth':      forms.DateInput(attrs={'type': 'date'}),
            'present_address':    forms.Textarea(attrs={'rows': 3}),
            'permanent_address':  forms.Textarea(attrs={'rows': 3}),
            'gender':             forms.Select(),
            'shift':              forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' form-control').strip()
            field.widget.attrs.setdefault('autocomplete', 'off')