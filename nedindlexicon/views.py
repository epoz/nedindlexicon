from django.views.generic.simple import direct_to_template
from django.conf import settings
import pyes


def get_search_results(q, extra_filter=None):
    es = pyes.ES(settings.ELASTIC_SEARCH)
    if q:
        q1 = pyes.StringQuery(q)
    else:
        q1 = pyes.MatchAllQuery()
    if extra_filter:
        q2 = q1.search(filter=extra_filter)
    else:
        q2 = q1.search()
    q2.facet.add_term_facet('taal')
    q2.facet.add_term_facet('woordsoort')
    q2.facet.add_term_facet('sfeer', size="30")

    results = es.search(query=q2, indices='nedind',
        doc_types=['trefwoord'], size=50)
    return results


def home(request):
    return direct_to_template(request, "homepage.html")


def search(request):
    q = request.GET.get('q')

    filters, filtercheckboxes = {}, {}
    for fname in ('taal', 'sfeer', 'woordsoort'):
        filterlist = request.GET.getlist(fname)
        if filterlist:
            filters[fname] = pyes.ORFilter([pyes.TermFilter(fname, fl) for fl in filterlist])
            filtercheckboxes[fname] = filterlist
    if filters:
        filters = pyes.ANDFilter(filters.values())

    results = get_search_results(q, extra_filter=filters)

    return direct_to_template(request, "search.html",
        {'results': results, 'q': q, 'filters': filtercheckboxes})


def trefwoordview(request, trefnum):
    q = request.GET.get('q')
    es = pyes.ES(settings.ELASTIC_SEARCH)
    results = es.search(pyes.TermQuery("trefnum", trefnum),
        'nedind', 'trefwoord')
    if results.count() < 1:
        raise Exception('We need a 404')
    return direct_to_template(request, "trefwoord.html",
        {'lemma': results.next(), 'q': q})
