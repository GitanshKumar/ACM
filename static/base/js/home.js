const slides = document.querySelectorAll(".slide");
let maxSlide = slides.length - 1;
let curSlide = 0;
let timeId;

function arrange() {
    slides.forEach((slide, i) => {
        slide.setAttribute("style", `transform:translateX(${100*(i - curSlide)}%)`);
    });
}

function startLoop(auto) {
    clearTimeout(timeId);
    if (auto === 1) {
        if (curSlide == maxSlide) {
            curSlide = 0;
        }
        else {
            curSlide += 1;
        }
    }
    arrange();
    timeId = setTimeout(function() {startLoop(1)}, 5000);
}

const nextslide = document.querySelector(".btn-next");
nextslide.addEventListener("click", function () {
    if (curSlide == maxSlide) {
        curSlide = 0;
    }
    else {
        curSlide += 1;
    }
    startLoop(0);
});

const prevslide = document.querySelector(".btn-prev");
prevslide.addEventListener("click", function () {
    if (curSlide == 0) {
        curSlide = maxSlide;
    }
    else {
        curSlide -= 1;
    }
    startLoop(0);
});

startLoop(0);