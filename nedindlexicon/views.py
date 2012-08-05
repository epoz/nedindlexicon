from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator
from django.conf import settings
import pyes
import urllib

def get_search_results(q, extra_filter=None, sort='trefwoord'):
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
        doc_types=['trefwoord'], sort=sort)
    return results


def home(request):
    return direct_to_template(request, "homepage.html")

def balance_quotes(val):
    count = len([x for x in val if x == '"'])
    if (count % 2) == 1:
        val = val + '"'
    return val

def search(request):
    q = request.GET.get('q', u'')
    q = balance_quotes(q)
    
    start = int(request.GET.get('start', 0))
    size = int(request.GET.get('size', 100))
    page = request.GET.get('page', 1)
    sort = request.GET.get('sort', 'trefwoord')

    filters, filtercheckboxes, filterurl = {}, {}, []
    for fname in ('taal', 'sfeer', 'woordsoort'):
        filterlist = request.GET.getlist(fname)
        if filterlist:
            filters[fname] = pyes.ORFilter([pyes.TermFilter(fname, fl) for fl in filterlist])
            filtercheckboxes[fname] = filterlist
            for filterlistitem in filterlist:
                filterurl.append('%s=%s' % (fname, filterlistitem))
    if filters:
        filters = pyes.ANDFilter(filters.values())
    pageurl = '?q=%s' % urllib.quote_plus(q)
    if filterurl:
        pageurl += '&'
        pageurl += '&'.join(filterurl)
    pageurl_nosort = pageurl
    pageurl += '&sort=' + sort


    results = get_search_results(q, extra_filter=filters, sort=sort)
    pagi = Paginator(results, size)
    data = pagi.page(page)    
    pagerange = pagi.page_range[int(page)-1:min(int(page)+9, int(pagi.num_pages))]

    return direct_to_template(request, "search.html",
        {'results': results, 'data': data, 'paginator': pagi, 'page': page,
         'q': q, 'filters': filtercheckboxes, 'start': start, 'size': size,
         'pageurl': pageurl, 'pageurl_nosort': pageurl_nosort, 'pagerange': pagerange})


def trefwoordview(request, trefnum):
    q = request.GET.get('q')
    es = pyes.ES(settings.ELASTIC_SEARCH)
    results = es.search(pyes.TermQuery("trefnum", trefnum),
        'nedind', 'trefwoord')
    if results.count() < 1:
        raise Exception('We need a 404')
    return direct_to_template(request, "trefwoord.html",
        {'lemma': results.next(), 'q': q})
