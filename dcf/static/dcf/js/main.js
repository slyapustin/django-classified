/**
 * Created by evgen on 9/15/16.
 */
jQuery(function($){

  $("img.favorit").on("click", function(){
      if (this.id === 'unmark') {
          $('img.favorit').attr('src', '/static/dcf/img/icon-check-mark.png');
          this.id = 'mark';


          $.ajax({
            type: "POST",
            url: "/add_favorites/",
            dataType: "json",
            data: { "item": document.getElementById("for_mark").value },
            success: function() {
                alert('good');
            }
          });



      } else {
          $('img.favorit').attr('src', '/static/dcf/img/icon-check-unmark.png');
          this.id = 'unmark';

          $.ajax({
            type: "POST",
            url: "/del_favorites/",
            dataType: "json",
            data: { "item": document.getElementById("for_mark").value },
            success: function() {
                alert('good');
            }
          });
      }
  });
});