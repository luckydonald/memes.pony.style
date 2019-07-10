// Generated by CoffeeScript 1.9.1
window.SearchView = Backbone.View.extend({
  el: "#content",
  initialize: function(data) {
    this.template = tpl.get("search");
    return this.model = new FaceCollection();
  },
  render: function() {
    var loader, tags, to_template;
    tags = getUrlParam("tags") || getUrlParam("tag");
    this.updateMeta("Search for '" + tags + "' - MyLittleFaceWhen", "Search result for pony reaction tag '" + tags + "'");
    if (!tags) {
      to_template = {
        query: "Search by typing some tags into the searchbox __^",
        static_prefix: static_prefix
      };
      this.$el.html(Mustache.render(this.template, to_template));
      return this;
    }
    to_template = {
      query: tags,
      static_prefix: static_prefix
    };
    this.$el.html(Mustache.render(this.template, to_template));
    loader = this.$el.children("#loader");
    loader.show();
    this.model.fetch({
      data: {
        tags__all: tags,
        limit: 1000,
        order_by: "-id"
      },
      success: (function(_this) {
        return function(data) {
          var imgs, thumbs;
          thumbs = _this.$el.children("#thumbs");
          if (_this.model.models.length === 0) {
            thumbs.html("No search results");
          } else if (_this.model.models.length === 1) {
            app.navigate("/f/" + _this.model.models[0].attributes.id + "/", {
              trigger: true
            });
          } else {
            _.each(_this.model.models, function(model) {
              return $(thumbs).append(new Thumbnail({
                model: model
              }).render().el);
            });
            imgs = $('.lazy');
            imgs.removeClass('lazy').lazyload();
          }
          return loader.hide();
        };
      })(this),
      error: (function(_this) {
        return function() {
          _this.$el.children("h2").html("There was an error");
          return loader.hide();
        };
      })(this)
    });
    return this;
  }
});
