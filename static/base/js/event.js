const slides = document.querySelectorAll(".slide");
let maxSlide = slides.length - 1;
let curSlide = Math.floor(maxSlide / 2);
let timeId;

function arrange() {
    slides.forEach((slide, i) => {
        var pos = i - curSlide;
        slide.setAttribute("style", `transform:translateX(${pos * 40}%) scale(${1 - 0.3 * Math.abs(pos)});z-index:${10 - Math.abs(pos)};`);
    });
}

function startLoop(auto) {
    clearTimeout(timeId);
    if (auto === 1) {
        if (curSlide === maxSlide) {
            curSlide = 0;
        } else {
            curSlide++;
        }
    }
    arrange();
    timeId = setTimeout(function() {startLoop(1)}, 5000);
}

const nextslide = document.querySelector(".btn-next");
nextslide.addEventListener("click", function () {
    if (curSlide === maxSlide) {
        curSlide = 0;
    } else {
        curSlide++;
    }
    startLoop(0);
});

const prevslide = document.querySelector(".btn-prev");
prevslide.addEventListener("click", function () {
    if (curSlide === 0) {
        curSlide = maxSlide;
    } else {
        curSlide--;
    }
    startLoop(0);
});

startLoop(0);