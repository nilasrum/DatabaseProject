let carousels = document.getElementsByClassName('image-carousel');

[].forEach.call(carousels, function (c) {
    let next = c.getElementsByClassName('next')[0],
        prev = c.getElementsByClassName('prev')[0],
        inner = c.getElementsByClassName('inner')[0],
        imgs = inner.getElementsByClassName('recent'),
        currentImageIndex = 0,
        width = document.getElementsByClassName("inner")[0].clientWidth/imgs.length;


    function switchImg () {
        inner.style.left = -width * currentImageIndex + 'px';
    }

    next.addEventListener('click', function () {
        currentImageIndex++;

        if (currentImageIndex >= imgs.length) {
            currentImageIndex = 0;
        }

        switchImg();
    });

    prev.addEventListener('click', function () {
        currentImageIndex--;

        if (currentImageIndex < 0) {
            currentImageIndex = imgs.length - 1;
        }

        switchImg();
    });

    switchImg();
});
