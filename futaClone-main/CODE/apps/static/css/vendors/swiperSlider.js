const swiper = new Swiper('.swiper', {
    loop: true,
    speed: 500,
    autoplay: {
        delay: 2500,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    // breakpoints: {
    //     // when window width is >= 320px
    //     320: {
    //         slidesPerView: 1,
    //         spaceBetween: 0
    //     },
    //     // when window width is >= 480px
    //     480: {
    //         slidesPerView: 1,
    //         spaceBetween: 0
    //     },
    //     // when window width is >= 640px
    //     640: {
    //         slidesPerView: 1,
    //         spaceBetween: 0
    //     }
    // }
});

const secondSwiper = new Swiper('.recommend-swiper', {
    direction: 'horizontal',
    loop: true,
    centeredSlides: true,
    speed: 800,
    autoplay: {
        delay: 2000,
    },

    breakpoints: {
        // when window width is >= 1200px
        1200: {
            slidesPerView: 7,
            spaceBetween: 70
        },
        // when window width is >= 1024px
        1024: {
            slidesPerView: 6,
            spaceBetween: 50
        },
        // when window width is >= 768px
        768: {
            slidesPerView: 5,
            spaceBetween: 70
        },
        // when window width is >= 480px
        480: {
            slidesPerView: 4,
            spaceBetween: 50
        },
        400: {
            slidesPerView: 3,
            spaceBetween: 50
        },
        350: {
            slidesPerView: 3,
            spaceBetween: 20
        }

    },
    // If we need pagination


    // Navigation arrows
    navigation: {
        nextEl: '.recommend-swiper-button-next',
        prevEl: '.recommend-swiper-button-prev',
    },
});

const thirdSwiper = new Swiper(".new-swiper", {
    loop: true,
    speed: 500,
    autoplay: {
        delay: 2500,
    },


    breakpoints: {
        // when window width is >= 1200px
        600: {
            slidesPerView: 3,
            spaceBetween: 10,
        },
        480: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
        0: {
            slidesPerView: 1,
            spaceBetween: 10,
        }
    }
})