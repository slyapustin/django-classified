jQuery(function($){

  $("span.star").on("click", function(){
      if ($(this).hasClass("glyphicon-star-empty")) {
          $.ajax({
            type: "POST",
            url: "/add_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            context: this, 
            success: function() {
                $(this).toggleClass("glyphicon-star-empty glyphicon-star");
            }
          });
      } else {
          $.ajax({
            type: "POST",
            url: "/del_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            context: this,
            success: function() {
                $(this).toggleClass("glyphicon-star glyphicon-star-empty");
            }
          });
      }
  });
});
