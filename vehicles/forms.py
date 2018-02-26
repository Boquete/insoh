from django import forms

from django.forms.models import inlineformset_factory
from .models import Vehicle, Battery


class VehicleCreateForm(forms.ModelForm):
    batteries_number = forms.IntegerField()

    class Meta:
        model = Vehicle
        exclude = ['']

    def save(self, commit=True):
        if commit:
            self.instance.save()
            for i in range(self.cleaned_data.get('batteries_number')):
                Battery.objects.create(vehicle=self.instance)
        else:
            return super().save(commit)
        return self.instance


class VehicleUpdateForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        exclude = ['']

    def save(self, commit=True):
        if commit:
            self.instance.save()
        else:
            return super().save(commit)
        return self.instance


BatteryFormSet = inlineformset_factory(Vehicle, Battery, form=VehicleUpdateForm, extra=1)
