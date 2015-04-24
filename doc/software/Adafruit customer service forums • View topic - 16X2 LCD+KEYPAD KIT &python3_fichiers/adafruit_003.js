;(function( $, window, document, undefined ) {
  window.toggleExpandCodeBox = function(el) {
    /* get the code block relative to this link element
     * ...<dt><a>TOGGLE</a></dt><dd><code></code></dd>... */
    $el = $(el.parentElement.nextElementSibling.children[0]);
    if($el.css('max-height') !== 'none') {
      $el.attr('data-orig-height', $el.css('max-height'));
      $el.css('max-height', 'none');
    } else {
      $el.css('max-height', $el.attr('data-orig-height'));
    }
  }
})( jQuery, window, document );
