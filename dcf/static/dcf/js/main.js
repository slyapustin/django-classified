/**
 * Created by evgen on 9/15/16.
 */
jQuery(function($){

  $("span.glyphicon").on("click", function(){
      if (this.id === 'unmark') {
          $("span.glyphicon").toggleClass("glyphicon-star-empty glyphicon-star")
          this.id = 'mark';

          $.ajax({
            type: "POST",
            url: "/add_favorites/",
            dataType: "json",
            data: { "item": document.getElementById("for_mark").value },
            success: function() {
            }
          });
      } else {
          $("span.glyphicon").toggleClass("glyphicon-star glyphicon-star-empty")
          this.id = 'unmark';

          $.ajax({
            type: "POST",
            url: "/del_favorites/",
            dataType: "json",
            data: { "item": document.getElementById("for_mark").value },
            success: function() {
            }
          });
      }
  });
});