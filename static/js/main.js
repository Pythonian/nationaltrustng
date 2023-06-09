(function ($) {
  "use strict";

  /*------------------------------------
  // Header
  ------------------------------------*/
  // humburger
  $(".humburger").on("click", function () {
    $(".humburger").toggleClass("active");
  });

  /*-------------------------------------
  // Trending slider
  ------------------------------------*/
  const rtTrendingSlider1 = new Swiper(".rt-treding-slider1", {
    slidesPerView: 1,
    loop: true,
    slideToClickedSlide: true,
    direction: "vertical",
    autoplay: {
      delay: 4000,
    },
    speed: 800,
  });

  /*================================== start Utilities ========================================*/

  /*------------------------------
   // Tooltip
   ------------------------------*/
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  /*------------------------------------
  //  Offcanvas Menu activation code
  -----------------------------------*/
  $("#wrapper").on("click", ".offcanvas-menu-btn", function (e) {
    e.preventDefault();
    const $this = $(this),
      wrapper = $(this).parents("body").find(">#wrapper"),
      wrapMask = $("<div />").addClass("offcanvas-mask"),
      offCancas = $("#offcanvas-wrap"),
      position = offCancas.data("position") || "left";

    if ($this.hasClass("menu-status-open")) {
      wrapper.addClass("open").append(wrapMask);
      $this.removeClass("menu-status-open").addClass("menu-status-close");
      offCancas.css({
        transform: "translateX(0)",
      });
    } else {
      removeOffcanvas();
    }

    function removeOffcanvas() {
      wrapper.removeClass("open").find("> .offcanvas-mask").remove();
      $this.removeClass("menu-status-close").addClass("menu-status-open");
      if (position === "left") {
        offCancas.css({
          transform: "translateX(-105%)",
        });
      } else {
        offCancas.css({
          transform: "translateX(105%)",
        });
      }
    }
    $(".offcanvas-mask, .offcanvas-close").on("click", function () {
      removeOffcanvas();
    });

    return false;
  });

  /*-------------------------------
   //  Back to Top
  -------------------------------*/
  const backToTop = document.getElementById("back-to-top");
  window.onscroll = function () {
    scrollFunction();
  };
  function scrollFunction() {
    if (backToTop !== null) {
      if (
        document.body.scrollTop > 80 ||
        document.documentElement.scrollTop > 80
      ) {
        backToTop.style.display = "block";
      } else {
        backToTop.style.display = "none";
      }
    }
  }
  if (backToTop !== null) {
    backToTop.addEventListener("click", (e) => {
      e.preventDefault();
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    });
  }

})(jQuery);
