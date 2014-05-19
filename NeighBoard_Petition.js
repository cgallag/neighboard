        
$(".petition-list").on('click', 'a', function() {
    $('a.active').removeClass('active');
    $(this).addClass('active');
});

