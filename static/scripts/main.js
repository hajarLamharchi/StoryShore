
$(document).ready(function() {
    $('ul li a').click(function(event) {
        thisAttrHref = $(this).attr('href');
        thisAttrHrefOffset = $(thisAttrHref).offset().top;
        $('html,body').animate({scrollTop:thisAttrHrefOffset});
        event.preventDefault();
       
    });
});

   
