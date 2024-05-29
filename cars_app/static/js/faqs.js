document.addEventListener('DOMContentLoaded', () => {
    const faqs = document.querySelectorAll('.faq-question');

    faqs.forEach(faq => {
        faq.addEventListener('click', () => {
            faq.classList.toggle ('active');
            const answer = faq.nextElementSibling;
            if (faq.classList.contains('active')) {
                answer.style.display = 'block';
            } else {
                answer.style.display = 'none';
            }
        });
    });
});