from django import forms
from .models import *

class ReagentForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='NOME DO ITEM*',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )   
    )

    formula = forms.CharField(
        required=True,
        label='FÓRMULA QUÍMICA*',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )   
    )

    classification = forms.CharField(
        required=True,
        label='CLASSIFICAÇÃO QUÍMICA*',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        ) 
    )

    state = forms.ChoiceField(
        required=True,
        label='CLASSIFIQUE O ITEM*',
        choices=[('Líquido/Sólido' , '')] + statesChoices,
        widget=forms.Select(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    amount = forms.IntegerField(
        required= False,
        label='QUANTIDADE',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    size = forms.IntegerField(
        required=False,
        label='TAMANHO DO FRASCO',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    limit = forms.IntegerField(
        required=True,
        label='LIMITE PARA AVISO*',
        widget = forms.TextInput(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    validity = forms.DateField(
        required=False,
        label='VALIDADE',
        widget=forms.DateInput(
            attrs={
                'type' : 'date',
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    control = forms.ChoiceField(
        label='CONTROLADO*',
        required=True,
        choices=controlChoices,
        widget=forms.Select(
            attrs={
                'class' : 'shadow-lg text-sm rounded-full focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:focus:border-primary-500'
            }
        )
    )

    incompatibility = forms.ModelMultipleChoiceField(
        required=False,
        label='INCOMPATÍVEL COM',
        queryset=Reagent.objects.all(),
        widget= forms.SelectMultiple(attrs={'class':'form-control input-search js-example-basic-multiple'})
    )

    is_active = forms.BooleanField(
        required=False,
        label='É ativo?'
    )
    
    class Meta():
        model = Reagent
        fields = ['name', 'formula', 'classification', 'state', 'control', 'incompatibility', 'limit', 'is_active']

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