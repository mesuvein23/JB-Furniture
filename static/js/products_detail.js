document.addEventListener("DOMContentLoaded", function () {
  const carousel = document.getElementById("productCarousel");
  if (!carousel) return;

  const thumbs = document.querySelectorAll("#pdpThumbs .pdp-thumb");
  const counter = document.getElementById("currentSlide");

  // Runs every time the carousel finishes moving to a new slide
  carousel.addEventListener("slid.bs.carousel", function (event) {
    thumbs.forEach((thumb) => thumb.classList.remove("active"));

    const activeThumb = thumbs[event.to];
    if (activeThumb) {
      activeThumb.classList.add("active");
      activeThumb.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" });
    }

    if (counter) counter.textContent = event.to + 1;
  });
});