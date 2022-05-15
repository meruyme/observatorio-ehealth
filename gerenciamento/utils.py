from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginar_registros(request, registros, qtd_por_pagina):
    paginator = Paginator(registros, qtd_por_pagina)
    page = request.GET.get('page')

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def decode_utf8(line_iterator):
    for line in line_iterator:
        yield line.decode('utf-8-sig')


def get_id(class_name, name):
    if name:
        dict_season = dict(class_name.CHOICES)
        ids = [id for id, value in dict_season.items() if value == name]
        if ids:
            return ids[0]
