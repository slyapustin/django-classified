/**
 * Created by evgen on 9/15/16.
 */
jQuery(function($){

  $("span.star").on("click", function(){
      if ($(this).hasClass("glyphicon-star-empty")) {
          var that = this
          $.ajax({
            type: "POST",
            url: "/add_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            success: function() {
                // dont know why 'this' not work, use var that
                $(that).toggleClass("glyphicon-star-empty glyphicon-star");
            }
          });
      } else {
          var that = this
          $.ajax({
            type: "POST",
            url: "/del_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            success: function() {
                $(that).toggleClass("glyphicon-star glyphicon-star-empty");
            }
          });
      }
  });
});