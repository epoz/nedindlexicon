do_search = () ->
    # First the MAIN URL
    loc = "/search/?q=" + encodeURI($('#q').val())
    # TAAL
    for tf in $('.taalfilter:checked')
        loc += '&taal=' + $(tf).attr('data')
    # SFEER
    for sf in $('.sfeerfilter:checked')
        loc += '&sfeer=' + $(sf).attr('data')
    # WOORDSOORT
    for wsf in $('.woordsoortfilter:checked')
        loc += '&woordsoort=' + $(wsf).attr('data')
    document.location = loc

$('#q').keydown (event) ->    
    if event.keyCode == 13
        event.preventDefault()
        do_search()

$('.filterbox').click (event) ->
    do_search()

$('#searchbutton').click (event) ->
    event.preventDefault()
    do_search()

$('.wisfilter').click (event) ->
    event.preventDefault()
    f = $(this).attr('rel')
    $('.'+f+'filter').attr('checked', false)
    do_search()

booya = () ->
    if typeof(qparam) != 'undefined'
        $('div').removeHighlight().highlight(qparam, false)
        $('.highlight').animate({ backgroundColor: "#a7bf51"}, 800);
    $('#q').focus()

$ ->
  booya()