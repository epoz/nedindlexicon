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

booya = () -> console.log('Ja! Page loaded')

$ ->
  booya()