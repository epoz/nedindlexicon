$('#q').keydown (event) ->    
    if event.keyCode == 13
        event.preventDefault()

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

$('.filterbox').click (event) -> $('#q').focus()

booya = () ->
    if typeof(qparam) != 'undefined'
        console.log('Ja! q was ' + qparam)
        $('div').removeHighlight().highlight(qparam, false)
        $('.highlight').animate({ backgroundColor: "#a7bf51"}, 800);

$ ->
  booya()