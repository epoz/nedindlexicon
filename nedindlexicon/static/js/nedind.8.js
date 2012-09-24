(function() {
  var booya, do_search;

  do_search = function() {
    var loc, sf, tf, wsf, _i, _j, _k, _len, _len2, _len3, _ref, _ref2, _ref3;
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
  };

  $('#q').keydown(function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      return do_search();
    }
  });

  $('.filterbox').click(function(event) {
    return do_search();
  });

  $('#searchbutton').click(function(event) {
    event.preventDefault();
    return do_search();
  });

  $('.wisfilter').click(function(event) {
    var f;
    event.preventDefault();
    f = $(this).attr('rel');
    $('.' + f + 'filter').attr('checked', false);
    return do_search();
  });

  booya = function() {
    if (typeof qparam !== 'undefined') {
      $('div').removeHighlight().highlight(qparam, false);
      $('.highlight').animate({
        backgroundColor: "#a7bf51"
      }, 800);
    }
    return $('#q').focus();
  };

  $(function() {
    return booya();
  });

}).call(this);
