'use strict';

const links = document.querySelectorAll('section > a');

links.forEach(link => {
    link.addEventListener('click', evento => {
        evento.preventDefault();
        const filter = evento.target.dataset.categoriapiatto;
        console.log(filter);
        const cards = document.querySelectorAll('.card-recensione');
        for (let card of cards) {
            if (filter !== 'Tutte' && filter !== card.querySelector('.card > span').textContent.trim()) {
                card.classList.add('hide');
                console.log(card.querySelector('.card > span').textContent.trim());
            } else {
                card.classList.remove('hide');
            }

        }
        
    });
});
