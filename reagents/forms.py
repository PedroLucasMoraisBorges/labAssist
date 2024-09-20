from django import forms
from .models import *

class ReagentForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='NOME DO ITEM',
    )

    formula = forms.CharField(
        required=True,
        label='FÓRMULA QUÍMICA'
    )

    classification = forms.CharField(
        required=True,
        label='CLASSIFICAÇÃO QUÍMICA'
    )

    state = forms.ChoiceField(
        required=True,
        label='CLASSIFIQUE O ITEM',
        choices=[('Líquido/Sólido' , '')] + statesChoices,
        widget=forms.Select()
    )

    amount = forms.IntegerField(
        required= True,
        label='QUANTIDADE'
    )

    size = forms.IntegerField(
        required=True,
        label='TAMANHO DO FRASCO'
    )

    limit = forms.IntegerField(
        required=True,
        label='LIMITE PARA AVISO'
    )

    validity = forms.DateField(
        required=True,
        label='VALIDADE',
        widget=forms.DateInput()
    )

    control = forms.ChoiceField(
        label='CONTROLADO',
        choices=controlChoices,
        widget=forms.Select()
    )

    incompatibility = forms.ModelMultipleChoiceField(
        required=False,
        label='INCOMPATÍVEL COM',
        queryset=Reagent.objects.all(),
        widget= forms.SelectMultiple(),
    )

    is_active = forms.BooleanField(
        required=True,
        label='É ativo?'
    )
    
    class Meta():
        model = Reagent
        fields = ['name', 'formula', 'classification', 'state', 'amount', 'validity', 'control', 'incompatibility', 'size', 'limit', 'is_active']

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Salvar a instâcia
        if commit:
            instance.save()
        
        # Processar incompatibilidades
        incompatible_reagents = self.cleaned_data.get('incompatibility')
        if incompatible_reagents:
            for reagent in incompatible_reagents:
                reagent.incompatibility.add(instance)
                reagent.save()
        
        return instance