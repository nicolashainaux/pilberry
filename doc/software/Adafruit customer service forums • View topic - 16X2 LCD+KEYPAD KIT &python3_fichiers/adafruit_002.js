;(function( $, window, document, undefined ){

  var transform_prop = window.Modernizr.prefixed('transform'),
    transition_prop = window.Modernizr.prefixed('transition'),
    transition_end = (function() {
      var props = {
          'WebkitTransition' : 'webkitTransitionEnd',
          'MozTransition'    : 'transitionend',
          'OTransition'      : 'oTransitionEnd otransitionend',
          'msTransition'     : 'MSTransitionEnd',
          'transition'       : 'transitionend'
      };
      return props.hasOwnProperty(transition_prop) ? props[transition_prop] : false;
    })();

  var MobileMenu = function( elem, options ){
      this.elem = elem;
      this.$elem = $(elem);
      this.options = options;

      this.metadata = this.$elem.data( 'plugin-options' );

      this._init = false;
      this.menu_open = false;
    };

  // the plugin prototype
  MobileMenu.prototype = {
    defaults: {
      message: 'Mobile Menu Enabled'
    },



    init: function() {
      if (this._init) {
        return;
      }
      this._init = true;
      // Introduce defaults that can be extended either
      // globally or using an object literal.
      this.config = $.extend({}, this.defaults, this.options, this.metadata);

      this.enable_menu();

      return this;
    },

    enable_menu: function() {
      var that = this;
      $(document.documentElement).addClass('js-ready');

      //opening the menu
      $(document).on('touchstart click', '#small-header-menu-button', $.proxy(this.toggle_menu, this));
      //closing the menu
      $(document).on('touchstart click', '#small-nav-close-button', $.proxy(this.toggle_menu, this));
      
      //touching outside the nav
      $(document).on('touchstart click', function(e) {
        var has_parent = $('#small-header-nav').has(e.target).length > 0 || $(e.target).is('#small-header-nav');
        if (that.menu_open && !has_parent) {
          e.preventDefault();
          that.close_menu.call(that);
        }
      });
    },

    toggle_menu: function(e) {
      if (e) {
        e.preventDefault();
      }

      if (this.menu_open) {
        this.close_menu.call(this);
      } else {
        this.open_menu.call(this);
        e.stopPropagation();
      }
    },

    open_menu: function(e) {
      $(document.documentElement).addClass('js-nav');
      this.menu_open = true;
    },

    close_menu: function() {
      var that = this;
      function close_action(e) {
        if (e && $(e.target).is('#inner-wrapper')) {
          $(document).off(transition_end, '#inner-wrapper', close_action);
        }

        that.menu_open = false;
      }

      var duration = (transition_end && transition_prop) ? parseFloat($('#inner-wrapper').css(transition_prop + 'Duration')) : 0;

      if (duration > 0) {
        $(document).on(transition_end, '#inner-wrapper', close_action);
      } else {
        close_action(null);
      }

      $(document.documentElement).removeClass('js-nav');
    }

  };


  MobileMenu.defaults = MobileMenu.prototype.defaults;

  $.fn.mobile_menu = function(options) {
    return new MobileMenu(this, options).init();
  };

})( jQuery, window , document );