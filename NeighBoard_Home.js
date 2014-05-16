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

$("#make-post").on('click', function() {
    console.log('new post button pressed');
    console.log($("#board-names").children());
});

$("#make-board").on('click', function() {
    console.log('new board button pressed');
});

