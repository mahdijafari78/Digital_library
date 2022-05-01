/*
 Template Name: GoSofto - Software Landing Page Responsive HTML Template
 Description: Gosofto is a powerful 100% Responsive Multipurpose Software landing page template.
 Version: 1.0
 Author: https://themeforest.net/user/htmllover/portfolio
 */
$(document).ready(function () {

    // PRELOADER
    $('#preloader').delay(500).fadeOut('slow'); // will fade out the white DIV that covers the website.

    // SCROLL ANIMATION
    smoothScroll.init({
        speed: 1000,
        easing: 'easeInOutCubic',
        updateURL: false,
        offset: 0,
        callbackBefore: function(toggle, anchor) {},
        callbackAfter: function(toggle, anchor) {}
    });

}); // document ready end


