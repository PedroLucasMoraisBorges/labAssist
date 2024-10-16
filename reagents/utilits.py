import locale
from django.db.models import QuerySet
from collections import defaultdict
from .models import Reagent
import unicodedata
from django.db.models import Q

def search_for_reagent(search, state):
    passives = Reagent.objects.filter(
        (Q(name__startswith=search) | Q(classification__startswith=search) | Q(formula__startswith=search)) &
        Q(state=state) &
        Q(is_active=False)
    )
    actives = Reagent.objects.filter(
        (Q(name__startswith=search) | Q(classification__startswith=search) | Q(formula__startswith=search)) &
        Q(state=state) &
        Q(is_active=True)
    )

    return {
        'passives' : passives,
        'actives' : actives
    }

def ordenar_lista(queryset: QuerySet):
    # Define a localidade para que os acentos sejam considerados corretamente
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Converte o QuerySet em uma lista e ordena
    reagents_list = list(queryset)
    reagents_ordenados = sorted(reagents_list, key=lambda x: locale.strxfrm(x.name))
    
    return reagents_ordenados

def normalizar_letra(letra):
    # Remove acentos e retorna a letra em maiúscula
    return unicodedata.normalize('NFKD', letra).encode('ASCII', 'ignore').decode('ASCII').upper()

def agrupar_reagents_por_letra(queryset):
    # Cria um dicionário para armazenar os grupos
    grupos = defaultdict(list)
    
    # Agrupa os reagentes pela letra inicial
    for reagent in queryset:
        letra_inicial = normalizar_letra(reagent.name[0])  # Normaliza a primeira letra
        grupos[letra_inicial].append(reagent)
    
    # Converte o dicionário em uma lista de dicionários
    lista_formatada = [{letra: reagents} for letra, reagents in grupos.items()]
    
    return lista_formatada