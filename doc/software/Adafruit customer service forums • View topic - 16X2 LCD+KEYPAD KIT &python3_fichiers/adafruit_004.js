;(function( $, window, document, undefined ){

  var HoverMenu = function( elem, options ){
    //only include elements that contain flyouts
    this.elem = $.grep(elem, function(el) {
      return $(el).has('.flyouts').length > 0;
    });

    this.$elem = $(this.elem);
    this.options = options;

    this.metadata = this.$elem.data( 'plugin-options' );

    this._init = false;
    this.menu_open = false;
    this.menu_timeout = null;

    if (this.$elem.length === 0) {
      //no elements to bind to...don't setup menu.
      this._init = true;
    }
  };

  // the plugin prototype
  HoverMenu.prototype = {
    defaults: {
      message: 'Menu Enabled'
    },

    templates: {},

    init: function() {
      if (this._init) {
        return;
      }

      this._init = true;

      // Introduce defaults that can be extended either
      // globally or using an object literal.
      this.config = $.extend({}, this.defaults, this.options, this.metadata);

      //this.set_column_height();
      this.enable_menu();

      return this;
    },

    set_column_height: function($elem) {
        var $columns = $('.column', $elem);
        var tallest_height = 0;

        $columns.each(function () {
          var this_height = $(this).height();

          if(this_height > tallest_height) {
            tallest_height = this_height;
          }
        });
        $columns.height(tallest_height);

    },

    enable_menu: function() {
      var that = this;
      var $hover_menu = $(".hover-menu");

      //use touch events to open and close the hover menu on tablets.
      this.$elem.children('a').bind('touchstart', function(event) {
        event.preventDefault();
        event.stopPropagation();

        if (that.menu_open) {
          that.close_menu.call($(this).parents('li'), that);
        } else {
          that.open_menu.call($(this).parents('li'), that);
        }
      });

      this.$elem.children('a').bind('touchstart', function(event) {
        event.preventDefault();
        event.stopPropagation();
      });

      $(document).on('touchend', function(event) {
        if (that.menu_open) {

          if (!$hover_menu.is(event.target) && $hover_menu.has(event.target).length === 0) {
              that.close_menu.call($('#navigation ul > li.active'), that);
          }
        }
      });

      this.$elem.hoverIntent({
        interval: 50,
        sensitivity: 5,
        over: function () {
          that.open_menu.call(this, that);
        },

        out: function() {
          that.close_menu.call(this, that);
        }
      });
    },

    open_menu: function(that) {
      window.clearTimeout(that.menu_timeout);
      $('#navigation ul > li').removeClass('active');
      $(this).addClass('active');
      
      if (that.menu_open) {
        $('.flyout.active').stop(true,true).hide().removeClass('active');
        $('.flyout', this).show();
        that.set_column_height($('.flyout', this));
        $('.flyout', this).addClass('active');
      } else {
        that.menu_open = true;
        var elem = this;
        $('.flyout', elem).addClass('active');
        $('.flyout', elem).slideDown(50, function() {
          that.set_column_height($('.flyout', elem));
          $(elem).stop(true,true);
        });
      }
    },

    close_menu: function(that) {
      var hover_element = this;

      window.clearTimeout(that.menu_timeout);
      that.menu_timeout = setTimeout(function() {
        $('.flyout', hover_element).slideUp(50, function() {
          $('#navigation ul > li').removeClass('active');
          $('.flyout.active').removeClass('active');
          that.menu_open = false;
          $(hover_element).stop(true,true);
        });
      }, 600);
    }
  };

  HoverMenu.defaults = HoverMenu.prototype.defaults;

  $.fn.hover_menu = function(options) {
    return new HoverMenu(this, options).init();
  };

})( jQuery, window , document );