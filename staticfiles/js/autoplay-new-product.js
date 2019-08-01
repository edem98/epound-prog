$(document).ready(function() {

  var owl = $("#product-slide");

  owl.owlCarousel({
      items : 5, //10 items above 1000px browser width
      itemsDesktop : [1000,3], //5 items between 1000px and 901px
      itemsDesktopSmall : [900,2], // betweem 900px and 601px
      itemsTablet: [600,1], //2 items between 600 and 0
      itemsMobile : false // itemsMobile disabled - inherit from itemsTablet option
  });

    owl.trigger('owl.play',1000); //owl.play event accept autoPlay speed as second parameter

});