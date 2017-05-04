from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginator_wrapper(request, object_list, per_page, url='page', orphans=0, allow_empty_first_page=True):
    """wrap paginator function including exceptions."""
    paginator = Paginator(object_list, per_page)
    page = request.GET.get(url)
    try:
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
    return page_object
