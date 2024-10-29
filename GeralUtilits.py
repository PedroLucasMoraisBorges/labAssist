from django.core.paginator import Paginator
import locale

# Retorna erros de formulários
def getErrors(Forms):
        errors = []
        for form in Forms:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field.title()}: {error}")
        return errors

def paginate(querySet, request):
        '''
        Paginação das telas.
        '''
        vaga_paginator = Paginator(querySet, 12)
        page = request.GET.get('page')
        return vaga_paginator.get_page(page)

def ordenar_array(array):
    # Define a localidade para que os acentos sejam considerados corretamente
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Ordena o array
    array_ordenado = sorted(array, key=locale.strxfrm)
    return array_ordenado