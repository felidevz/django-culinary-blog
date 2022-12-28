from django.core.paginator import Paginator


def paginate(request, object_list):
    paginator = Paginator(object_list, 4)
    page_nr = request.GET.get('page', 1)
    try:
        page_nr = int(page_nr)
        if page_nr < 1:
            page_nr = 1
        elif page_nr > paginator.num_pages:
            page_nr = paginator.num_pages
    except ValueError:
        page_nr = 1
    page_obj = paginator.get_page(page_nr)
    page_range = paginator.get_elided_page_range(page_nr, on_each_side=2, on_ends=1)
    return {'page_obj': page_obj, 'page_range': page_range}
