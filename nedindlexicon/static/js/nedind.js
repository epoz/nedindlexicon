(function() {
  var booya;

  $('#q').keydown(function(event) {
    var loc, sf, tf, wsf, _i, _j, _k, _len, _len2, _len3, _ref, _ref2, _ref3;
    if (event.keyCode === 13) {
      event.preventDefault();
      loc = "/search/?q=" + encodeURI($('#q').val());
      _ref = $('.taalfilter:checked');
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        tf = _ref[_i];
        loc += '&taal=' + $(tf).attr('data');
      }
      _ref2 = $('.sfeerfilter:checked');
      for (_j = 0, _len2 = _ref2.length; _j < _len2; _j++) {
        sf = _ref2[_j];
        loc += '&sfeer=' + $(sf).attr('data');
      }
      _ref3 = $('.woordsoortfilter:checked');
      for (_k = 0, _len3 = _ref3.length; _k < _len3; _k++) {
        wsf = _ref3[_k];
        loc += '&woordsoort=' + $(wsf).attr('data');
      }
      return document.location = loc;
    }
  });

  $('.filterbox').click(function(event) {
    return $('#q').focus();
  });

  booya = function() {
    if (typeof qparam !== 'undefined') {
      console.log('Ja! q was ' + qparam);
      $('div').removeHighlight().highlight(qparam, false);
      return $('.highlight').animate({
        backgroundColor: "#a7bf51"
      }, 800);
    }
  };

  $(function() {
    return booya();
  });

}).call(this);
