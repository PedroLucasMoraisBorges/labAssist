import locale
from django.db.models import QuerySet
from collections import defaultdict
from .models import Reagent, ReagentBatch
from reports.models import *
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
    
    # Converte o QuerySet em uma lista
    reagents_list = list(queryset)

    # Ordena a lista com base no nome do reagente
    reagents_ordenados = sorted(reagents_list, key=lambda x: locale.strxfrm(x['info'].name))
    
    return reagents_ordenados

def normalizar_letra(letra):
    # Remove acentos e retorna a letra em maiúscula
    return unicodedata.normalize('NFKD', letra).encode('ASCII', 'ignore').decode('ASCII').upper()

def agrupar_reagents_por_letra(queryset):
    # Cria um dicionário para armazenar os grupos
    grupos = defaultdict(list)
    
    # Agrupa os reagentes pela letra inicial
    for reagent in queryset:
        letra_inicial = normalizar_letra(reagent['info'].name[0])  # Normaliza a primeira letra
        grupos[letra_inicial].append(reagent)
    
    # Converte o dicionário em uma lista de dicionários
    lista_formatada = [{letra: reagents} for letra, reagents in grupos.items()]
    
    return lista_formatada

def create_new_batch_by_movement(movement : Movement):
    reagentBatch = ReagentBatch.objects.create(
        amount = movement.amount,
        size = movement.size,
        validity = movement.validity,
        fk_reagent = movement.fk_reagent
    )
    reagentBatch.save()

def get_num_of_reagents(reagentBatches):
    count = 0
    for batch in reagentBatches:
        count += batch.amount

    return count

def remove_reagent_from_stock(movement : Movement):
    quantityOfItems = movement.amount
    reagentBatches = ReagentBatch.objects.filter(amount__gt=0, fk_reagent=movement.fk_reagent).order_by('-validity')

    if len(reagentBatches) > 0 and get_num_of_reagents(reagentBatches) >= quantityOfItems:
        for batch in reagentBatches:
            if batch.amount >= quantityOfItems:
                batch.amount -= quantityOfItems
                batch.save()
                break
            else:
                quantityOfItems -=  batch.amount
                batch.amount = 0
                batch.save()
    else:
        return False