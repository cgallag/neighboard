/* The new post and new board modals are forms that appear
/ in front of the rest of the page, which is shaded and unusable
/ when the "new post" or "new board" button is clicked. So it
/ needs to be triggered when the user clicks on the button. The
/ modals are part of the NeighBoard_Home.html page, so the buttons
/ cannot just link to forms on other pages.
*/
$("#new-post").on('click', function() {
    $("#new-post-modal").modal(); 
});

$("#new-board").on('click', function() {
   $("#new-board-modal").modal();
});
        
$(".list-group").on('click', 'a', function() {
    $('a.active').removeClass('active');
    $(this).addClass('active');
});

