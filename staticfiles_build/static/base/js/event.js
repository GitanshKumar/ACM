const slides = document.querySelectorAll(".slide");
let maxSlide = slides.length - 1;
let curSlide = Math.floor(maxSlide / 2);
let timeId;
var transformvals = []
for (let i = 0; i < slides.length; i++) {
    var pos = i - curSlide;
    if (-3 < pos && pos < 3){
        transformvals.push([pos * (40 - 10 * Math.abs(pos)), 1 - 0.3 * Math.abs(pos), 10 - Math.abs(pos), 1 - 0.3 * Math.abs(pos)])
    }
    else {
        transformvals.push([pos * 50, 1 - 0.3 * Math.abs(pos), 10 - Math.abs(pos), 0])
    }
}

function arrange() {
    slides.forEach((slide, i) => {
        var val = transformvals[i];
        slide.setAttribute("style", `transform:translateX(${val[0]}%) scale(${val[1]});z-index:${val[2]};opacity:${val[3]};`);
    });
}

function startLoop(auto) {
    clearTimeout(timeId);
    if (auto === 1) {
        transformvals.unshift(transformvals.pop())
    }
    arrange();
    timeId = setTimeout(function() {startLoop(1)}, 5000);
}

const nextslide = document.querySelector(".btn-next");
nextslide.addEventListener("click", function () {
    transformvals.unshift(transformvals.pop())
    startLoop(0);
});

const prevslide = document.querySelector(".btn-prev");
prevslide.addEventListener("click", function () {
    transformvals.push(transformvals.shift())
    startLoop(0);
});

startLoop(0);