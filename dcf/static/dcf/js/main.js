/**
 * Created by evgen on 9/15/16.
 */
jQuery(function($){

  $("span.star").on("click", function(){
      if ($(this).hasClass("glyphicon-star-empty")) {
          $(this).toggleClass("glyphicon-star-empty glyphicon-star");

          $.ajax({
            type: "POST",
            url: "/add_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            success: function(data) {
                data.msg;
            }
          });
      } else {
          $(this).toggleClass("glyphicon-star glyphicon-star-empty");

          $.ajax({
            type: "POST",
            url: "/del_favorites/",
            dataType: "json",
            data: { "item": $(this).attr("id") },
            success: function(data) {
                data.msg
            }
          });
      }
  });
});