$(window).scroll(function() {
    var windscroll = $(window).scrollTop();

    if (windscroll >= 200) {
        
        $('.content .pad-section').each(function(i) {
            if ($(this).position().top <= windscroll) {
                $('.nav li.active').removeClass('active');
                $('.nav li').eq(i).addClass('active');
            }
        });

    } else {

        $('nav').removeClass('fixed');
        $('nav a.active').removeClass('active');
        $('nav a:first').addClass('active');
    }

}).scroll();

$('body').delegate('nav a', 'click', function(){
  event.preventDefault();
    $('html,body').stop().animate({
          scrollTop: $($(this).attr('href')).offset().top - $("nav")[0].getBoundingClientRect().bottom
        }, 500, 'easeInOutCubic');
        
});