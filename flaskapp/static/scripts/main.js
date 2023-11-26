
$(document).ready(function () {
    $('#home').click(function (event) {
        $('#about').removeClass("active");
        $('#contact').removeClass("active");
        $('#home').addClass("active");
        let homeOffset = 0;
        $('html,body').animate({ scrollTop: homeOffset });
        event.preventDefault();
    });

    $('#about').click(function (event) {
        $('#home').removeClass("active");
        $('#contact').removeClass("active");
        $('#about').addClass("active");
        let aboutOffset = $('#about_offset').offset().top - 110;
        $('html,body').animate({ scrollTop: aboutOffset });
        event.preventDefault();
    });

    $('#contact').click(function (event) {
        $('#about').removeClass("active");
        $('#home').removeClass("active");
        $('#contact').addClass("active");
        let contactOffset = $('#contact_offset').offset().top;
        $('html,body').animate({ scrollTop: contactOffset });
        event.preventDefault();
    });


    $(window).scroll(function () {

        let aboutOffset = $('#about_offset').offset().top - 110;
        let scrollPosition = $(window).scrollTop();
        let contactOffset = $('#contact_offset').offset().top - 110;
        if (scrollPosition >= 0 && scrollPosition < aboutOffset) {
            $('#about').removeClass("active");
            $('#contact').removeClass("active");
            $('#home').addClass("active");
        }
        else if (scrollPosition >= aboutOffset && scrollPosition < contactOffset) {
            $('#home').removeClass("active");
            $('#contact').removeClass("active");
            $('#about').addClass("active");
        }
        else if (scrollPosition >= contactOffset) {
            $('#about').removeClass("active");
            $('#home').removeClass("active");
            $('#contact').addClass("active");
        }
        $('#scrollPosition').text('Vertical Scroll Position: ' + scrollPosition);
        if (scrollPosition === 0) {
            $('#navbar').removeClass('navbar_onscroll');
            $('#navbar').addClass('navbar');
        }
        else {
            $('#navbar').removeClass('navbar');
            $('#navbar').addClass('navbar_onscroll');
        }
    });

    $('#discover_more').click(function () {
        window.location.href = '/books';
    });

    $('#buy_button').click(function () {
        window.location.href = '/login';
    });

    $('#buy_button_authenticated').click(function () {
        window.location.href = '/books';
    });

    $('#publish_button').click(function () {
        window.location.href = '/login';
    });

    $('#publish_button_authenticated').click(function () {
        window.location.href = '/dashboard';
    });


    function isElementVisible(element) {
        return $(element).is(':visible');
    }

    function hideElementAfterDelay(element, delay) {
        setTimeout(function () {
            if (isElementVisible(element)) {
                $(element).hide();
            }
        }, delay);
    }

    var myDiv = $('#alert');
    hideElementAfterDelay(myDiv, 3000);

   
});
