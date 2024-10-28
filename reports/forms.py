from django import forms
from .models import *
from reagents.models import *
from django.db.models import Q

class MovementForm(forms.ModelForm):
    motivation = forms.CharField(
        required=True,
        label='Motivação',
        widget=forms.Textarea()
    )

    amount = forms.IntegerField(
        required=True,
        label='Quantidade',
        widget=forms.NumberInput(attrs={'min' : 1})
    )

    movement_type = forms.ChoiceField(
        required=True,
        choices=typeMovementChoices,
        label='Tipo de movimentação',
        widget=forms.Select()
    )

    fk_reagent = forms.ModelChoiceField(
        required=True,
        queryset=Reagent.objects.filter(Q(amount__gt=0)),
        widget=forms.Select()
    )

    class Meta:
        model=Movement
        fields=['motivation', 'amount', 'movement_type', 'fk_reagent']

class LicenseForm(forms.ModelForm):
    pdf = forms.FileField(
        label='Licensa',
        required=True,
        widget=forms.FileInput(attrs={'accept' : '.pdf'})
    )

    class Meta:
        model=License
        fields=['pdf']
    
class MovementForm(forms.ModelForm):
    motivation = forms.CharField(
        label='Motivação',
        required=True,
        widget=forms.Textarea()
    )

    amount = forms.IntegerField(
        label='Quantidade',
        required=True,
        widget=forms.NumberInput()
    )

    movement_type = forms.ChoiceField(
        label='Tipo de movimentação',
        required=True,
        choices=[('', 'Selecione um tipo')] + typeMovementChoices,
        widget=forms.Select()
    )

    fk_reagent = forms.ModelChoiceField(
        label='Reagente',
        required=True,
        queryset=Reagent.objects.filter(Q(amount__gt=0))
    )

    validity = forms.DateField(
        label='Validade',
        widget=forms.DateInput(attrs={'type' : 'date'})
    )

    class Meta:
        model=Movement
        fields=['motivation', 'amount', 'movement_type', 'fk_reagent', 'validity']