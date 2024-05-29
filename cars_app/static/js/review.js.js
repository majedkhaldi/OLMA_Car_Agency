document.querySelectorAll('.thumbnails a').forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', function(event) {
        event.preventDefault();
        showSlide(index);
    });
});

const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
let currentIndex = 0;

function showSlide(index) {
    if (index < 0) {
        index = slideCount - 1;
    } else if (index >= slideCount) {
        index = 0;
    }
    currentIndex = index;
    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
}

// Optional auto-slide functionality
setInterval(() => {
    showSlide(currentIndex + 1);
}, 5000);
