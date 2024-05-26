$(document).ready(function() {
    function wrapLetters(element) {
        const text = element.text();
        let newHtml = '';
        for (let i = 0; i < text.length; i++) {
            if (text[i] === ' ') {
                newHtml += '<span>&nbsp;</span>';
            } else {
                newHtml += `<span>${text[i]}</span>`;
            }
        }
        element.html(newHtml);
    }

    function animateLetters(element) {
        element.find('span').each(function(i) {
            $(this).delay(i * 100).animate({
                opacity: 1,
                top: 0
            }, 600);
        });
    }

    const h1 = $('.header-content h1');
    wrapLetters(h1);
    animateLetters(h1);
    $('.btn').hover(
        function() {
            $(this).animate({
                width: '+=10px',
                height: '+=5px',
                backgroundColor: '#ff9800'
            }, 200);
        },
        function() {
            $(this).animate({
                width: '-=10px',
                height: '-=5px',
                backgroundColor: 'rgba(197, 110, 110, 0.5)'
            }, 200);
        }
    );
    
    $('.btn').click(function() {
        $(this).animate({
            top: '+=5px'
        }, 100, function() {
            // Animation complete.
            $(this).animate({
                top: '-=5px'
            }, 100);
        });
    });
});
