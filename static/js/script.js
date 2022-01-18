var menu_btn = document.querySelector("#menu-btn");
menu_btn.style.display = "none";
var sidebar = document.querySelector("#sidebar");
var container = document.querySelector(".my-container");
var sociallink = document.querySelector(".sociallink");
menu_btn.addEventListener("click", () => {
  sidebar.classList.toggle("active-nav");
  container.classList.toggle("active-cont");
  sociallink.classList.toggle("hide-sociallink");
});

var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
if (isMobile) {
  menu_btn.style.display = "block";
  sociallink.style.bottom = "34px";
  var swiper = new Swiper(".mySwiper", {
    slidesPerView: 2,
    spaceBetween: 30,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
}else{
  var swiper = new Swiper(".mySwiper", {
    slidesPerView: 5,
    spaceBetween: 30,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
}

function changeUrl(src){
  iframe = document.getElementById('embeded');
    iframe.src = src;
}
function changeVideoUrl(src){
  iframe = document.getElementById('embededVideo');
    iframe.src = src;
}
function changeImgUrl(src){
  img = document.getElementById('model-img');
  img.src = src;
}

var Allslide = document.querySelectorAll('.swiper-slide');
Allslide.forEach(function(slide) {

  slide.addEventListener('click', function(e) {
    Allslide.forEach(function(sliderr) {
      if(sliderr.classList.contains('clickActive')){
        sliderr.classList.remove('clickActive');
      }
    });
    slide.classList.add('clickActive');
  });
});
