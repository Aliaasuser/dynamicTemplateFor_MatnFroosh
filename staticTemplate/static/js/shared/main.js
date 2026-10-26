$('#hml-menu-inSP_button').on('click', function(){
    $('#hml-menu-inSP_back').removeClass('d-none').addClass('d-block').on('click', function(){
        $(this).removeClass('d-block').addClass('d-none');
    }).children('div').first().children().first().on('click', function(event){
        event.stopPropagation();
    });
    $(window).on('resize', function(){
        if ($(this).width() >= 768){
            $('#hml-menu-inSP_back').removeClass('d-block').addClass('d-none');
        }
    });
});

(function(){
    let temp = $('.my-rating-type1');
    for (let i = 0; i < temp.length; i++){
        let t = $(temp.get(i));
        t.css('clip-path', 'polygon(0% 0%, ' + t.attr('data-value') + '% 0%, ' + t.attr('data-value') + '% 100%, 0% 100%)')
            .parent().append(Number(t.attr('data-value')) / 20);
    }
})();

function createMyCarousel_cards(id, k, cItemClasses){
    let $cards = $('#' + id + ' .card').clone();
    let $myCarousel = $('#' + id).clone();
    $myCarousel.children('.carousel-inner').children().remove();
    let $myCInner = $myCarousel.children('.carousel-inner');
    let numOfSlides = Math.ceil($cards.length / k);

    for (let i = 0; i < numOfSlides; i++){
        $myCInner.append($('<div>', {class: 'carousel-item'})).children().last()
            .append($('<div>', {class: cItemClasses}));
        for (let j = 0; j < k && $cards.length > i * k + j; j++)
            $($cards.get(i * k + j)).appendTo($myCInner.find('.row').last());
    }
    $myCInner.children('.carousel-item').first().addClass('active');
    let $myCIndicators = $myCarousel.children('.carousel-indicators');
    let $Indicator = $myCIndicators.children().first().clone();
    $Indicator.removeClass('active');
    $myCIndicators.children().remove();
    for (let i = 0; i < numOfSlides; i++)
        $myCIndicators.append($Indicator.clone().attr('data-slide-to', i));
    $myCIndicators.children().first().addClass('active');
    $('#' + id).carousel('dispose');
    $myCarousel.carousel();
    $('#' + id).replaceWith($myCarousel);
}

function myCarousel(id, ic, nc){
    let myCarouselId = id;
    let itemClasses = ic;
    let xl = nc.xl;
    let lg = nc.lg;
    let md = nc.md;
    let sm = nc.sm;
    let xs = nc.xs;
    let numOfColsInItem;
    if ($(window).innerWidth() >= 1200) numOfColsInItem = xl;
    else if ($(window).innerWidth() >= 992) numOfColsInItem = lg;
    else if ($(window).innerWidth() >= 768) numOfColsInItem = md;
    else if ($(window).innerWidth() >= 576) numOfColsInItem = sm;
    else numOfColsInItem = xs;
    createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);

    $(window).on('resize', function(){
        if ($(this).width() >= 1200 && numOfColsInItem != xl){
            numOfColsInItem = xl;
            createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);
        }
        else if ($(this).width() < 1200 && $(this).innerWidth() >= 992 && numOfColsInItem != lg){
            numOfColsInItem = lg;
            createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);
        }
        else if ($(this).width() < 992 && $(this).innerWidth() >= 768 && numOfColsInItem != md){
            numOfColsInItem = md;
            createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);
        }
        else if ($(this).width() < 768 && $(this).innerWidth() >= 576 && numOfColsInItem != sm){
            numOfColsInItem = sm;
            createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);
        }
        else if ($(this).width() < 576 && numOfColsInItem != xs){
            numOfColsInItem = xs;
            createMyCarousel_cards(myCarouselId, numOfColsInItem, itemClasses);
        }
    });
}

let nc = {xl: 4, lg: 4, md: 3, sm: 2, xs: 1};
let ic1 = $('#myCarousel_num1 .carousel-item>div').attr('class');
let myCarousel_num1 = new myCarousel('myCarousel_num1', ic1, nc);
let ic2 = $('#myCarousel_num2 .carousel-item>div').attr('class');
let myCarousel_num2 = new myCarousel('myCarousel_num2', ic2, nc);

function convertHMLType1(hml){
    let t = hml.clone();
    t.get(0).innerHTML = t.text();
    t.removeClass().addClass('btn btn-link btn-block text-right');
    let container = $('<div>', {class: 'card'}).append($('<div>', {class: 'card-header p-1'}));
    container.children('div').append(t);
    return container;
}

function convertHMLType2(hml){
    let t = hml.clone();
    let a = t.children('a').removeClass().addClass('btn btn-link text-right col-10');
    a.get(0).innerHTML = a.text();
    let container = $('<div>', {class: 'card'}).append($('<div>', {class: 'card-header p-1'}))
        .append($('<div>', {class: 'card-body collapse p-3'}));
    container.children('.card-header').append(a).append($('<button>', {
        class: 'btn btn-secondary dropdown-toggle',
        type: 'button',
        'data-toggle': 'collapse'
    }));
    a = t.children('div').children('div').children();
    for (let i = 0; i < a.length; i++){
        if ($(a.get(i)).is('a')) container.children('.card-body').append(convertHMLType1($(a.get(i))));
        else if ($(a.get(i)).is('div')) container.children('.card-body').append(convertHMLType2($(a.get(i))));
    }
    return container;
}

(function(){
    let t = $('#header-main-links').children('a, div');
    let menu = $('#hml-menu-inSP');
    menu.children().remove();
    for (let i = 0; i < t.length; i++){
        if ($(t.get(i)).is('a')) menu.append(convertHMLType1($(t.get(i))));
        else if ($(t.get(i)).is('div')) menu.append(convertHMLType2($(t.get(i))));
    }
})();

$('#hml-menu-inSP button').on('click', function(){
    if($(this).attr('data-toggle') === 'collapse'){
        let t = $(this).parent().parent().children('.collapse');
        if (t.hasClass('show')){
            t.collapse('hide');
            t.find('.collapse').collapse('hide');
        }
        else{
            t.parent().parent().find('.collapse').collapse('hide');
            t.collapse('show');
        }
    }
});

(function(){
    let moreHMLButton = $('#more-hml');
    moreHMLButton.children('div').children().remove();
    let temp = $('#header-main-links').children('a, div').clone();
    for (let i = 0; i < temp.length; i++){
        let t = $(temp.get(i));
        if (t.is('a')){
            t.get(0).innerHTML = t.text();
            t.removeClass().addClass('dropdown-item text-white d-none')
                .appendTo(moreHMLButton.children('div'));
        }
        else{
            t.removeClass().addClass('dropdown-item dropleft text-white pt-0 pb-0 pr-0 pl-5 d-none')
                .children('a').removeClass().addClass('btn-block full-glass d-inline-block pt-1 pb-1 pr-4 text-white');
            t.children('div').removeClass().addClass('dropdown-toggle has-menu full-glass d-inline-block pr-4 pl-2 border-right border-white');
            t.appendTo(moreHMLButton.children('div'));
        }
    }
    moreHMLButton.find('div.dropdown-item').removeClass('dropleft').addClass('dropright').children('a').removeClass('pr-4').addClass('pr-2');
    moreHMLButton.find('a.dropdown-item').addClass('pr-5');
    temp = moreHMLButton.find('div.dropdown-toggle').removeClass('pr-4 pl-2 border-right').addClass('pr-2 pl-3 border-left');
    for (let i = 0; i < temp.length; i++)
        $(temp.get(i)).prependTo($(temp.get(i)).parent());
})();

function myIsWraped(container, selector = ''){
    let cw = 0;
    for (let i = 0; i < container.children(selector).length; i++)
        cw += $(container.children().get(i)).outerWidth(true);
    return (cw >= container.width() * (2 / 3));
}

function setMyMoreHMLButton(){
    while(!myIsWraped($('#header-main-links'), 'a.d-md-inline-block, div.d-md-inline-block')){
        let moreHMLButton_item1 = $('#more-hml').children('div').children(':not(.d-none)').first();
        if (moreHMLButton_item1.length === 0) break;
        $('#header-main-links').children('a:not(.d-md-inline-block), div:not(.d-md-inline-block)').first().addClass('d-md-inline-block');
        moreHMLButton_item1.addClass('d-none');
    }
    while(myIsWraped($('#header-main-links'), 'a.d-md-inline-block, div.d-md-inline-block')){
        $('#header-main-links').children('a.d-md-inline-block, div.d-md-inline-block').last().removeClass('d-md-inline-block');
        $('#more-hml').children('div').children('.d-none').last().removeClass('d-none');
    }
    if($('#more-hml').children('div').children(':not(.d-none)').length === 0)
        $('#more-hml').removeClass('d-md-inline-block');
    else $('#more-hml').addClass('d-md-inline-block');
}

setMyMoreHMLButton();

$(window).on('resize', setMyMoreHMLButton);

$('.check-group').find('input[type="checkbox"]').on('change', function(){
    if ($(this).parent().hasClass('all-checked')){
        if ($(this).prop('checked'))
            $($(this).parents('.check-group').get(0)).find('input[type="checkbox"]').prop('checked', true);
        else
            $($(this).parents('.check-group').get(0)).find('input[type="checkbox"]').prop('checked', false);
    }
    if ($(this).prop('checked')){
        for (let i = 0; i < $(this).parents('.check-group').length; i++){
            let checks = $($(this).parents('.check-group').get(i)).find('input[type="checkbox"]');
            let flag = true;
            for (let j = 0; j < checks.length; j++)
                if (!$(checks.get(j)).prop('checked') && !$(checks.get(j)).parent().hasClass('all-checked')){
                    flag = false;
                    break;
                }
            if (flag)
                $($(this).parents('.check-group').get(i)).children('.all-checked').children('input[type="checkbox"]').prop('checked', true);
        }
    }
    else
        for (let i = 0; i < $(this).parents('.check-group').length; i++)
            $($(this).parents('.check-group').get(i)).children('.all-checked').children('input[type="checkbox"]').prop('checked', false);
});

function updateMyRange(obj){
    let temp1 = $(obj).children('input[type="range"][data-role="min"]');
    let min = ((temp1.val() - temp1.prop('min')) / (temp1.prop('max') - temp1.prop('min'))) * 100;
    let temp2 = $(obj).children('input[type="range"][data-role="max"]');
    let max = ((temp2.val() - temp2.prop('min')) / (temp2.prop('max') - temp2.prop('min'))) * 100;
    if (max < min){
        let dr = temp1.attr('data-role');
        temp1.attr('data-role', temp2.attr('data-role'));
        temp2.attr('data-role', dr);
    }
    $(obj).children('div[data-role="highlight-interval"]').css('clip-path', 'polygon(' + min + '% 0%, ' + min + '% 100%, ' + max + '% 100%, ' + max + '% 0%)');
}

function updateMyRangeDetails(obj){
    let t = $(obj).parent().children('.my-range').children('input[type="range"][data-role="min"]').val();
    $(obj).children('input[type="number"][data-role="min"]').val(t);
    t = $(obj).parent().children('.my-range').children('input[type="range"][data-role="max"]').val();
    $(obj).children('input[type="number"][data-role="max"]').val(t);
}

(function(){
    let temp = $('.my-range');
    for (let i = 0; i < temp.length; i++)
        updateMyRange(temp.get(i));
    temp.children('input[type="range"]').on('mousemove change', function(){
        updateMyRange($(this).parent());
        updateMyRangeDetails($(this).parent().parent().children('.my-range-details'));
    });
})();

(function(){
    let temp = $('.my-range-details');
    for (let i = 0; i < temp.length; i++)
        updateMyRangeDetails(temp.get(i));
    temp.children('input[type="number"]').on('change', function(){
        $(this).parent().parent().children('.my-range')
            .children('input[type="range"][data-role="' + $(this).attr('data-role') + '"]')
            .val($(this).val()).change();
    });
})();

(function(){
    let temp = $('#price-filter .has-panel input[type="radio"][checked]');
    $('#price-filter [data-owner-id="' + temp.attr('id') + '"]').removeClass('d-none');
    $('#price-filter input[type="radio"]').on('change', function(){
        if($(this).parent().hasClass('has-panel') && $(this).prop('checked')) $('#price-filter [data-owner-id="' + $(this).attr('id') + '"]').removeClass('d-none');
        else $('#price-filter .panel').addClass('d-none');
    })
})();

$('#my-search-form-container input[type="search"]').on('keydown paste cut change', function(event){
    setTimeout(() => {
        if($(this).prop('value').length > 0){
            $(this).parents('#my-search-form-container').addClass('bg-light').children('div').removeClass('d-none');
        }
        else{
            $(this).parents('#my-search-form-container').removeClass('bg-light').children('div').addClass('d-none');
        }
    }, 0);
    if(event.key === 'ArrowDown') $(this).parents('#my-search-form-container').find('select').focus();
});

$('#my-search-form-container select').on('click mousemove focus touchend', function(){
    setTimeout(() => {
        let temp = $(this).children('option').filter((index, element) => $(element).prop('selected'));
        if (temp.length === 1) $(this).parents('#my-search-form-container').find('input[type="search"]').val(temp.text());
        else if (temp.length > 1){
            let t = '';
            for (let i = 0; i < temp.length; i++)
                t += $(temp.get(i)).text() + ' ';
            $(this).parents('#my-search-form-container').find('input[type="search"]').val(t);
        }
    }, 0);
});

$('#my-search-form-container select').on('keypress', function(){
    let t = $(this).parents('#my-search-form-container').find('input[type="search"]').focus();
    if (k != undefined) t.val(t.val() + k);
});

$('#my-search-form-container select').on('keydown', function(event){
    if ((event.key === 'ArrowUp' && $($(this).children('option').get(0)).prop('selected')) || (event.key === 'Enter'))
        $(this).keypress();
    else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') setTimeout(() => {$(this).click()}, 0);
});

new (function(inpId){
    let dl = $('label[for="' + inpId + '"]').text();
    $('#' + inpId).on('change', function(){
        if ($(this).val())
            $('label[for="' + inpId + '"]').text($(this).val());
        else
            $('label[for="' + inpId + '"]').text(dl);
    });
})('ed-profile-image');

$('#clear-pi-uploaded').on('click', function(){
    $('#ed-profile-image').val('').change();
});

$('#ed-profile-information').find('button[type="reset"]').on('click', function(){
    $('#clear-pi-uploaded').click();
});

$('#discountCheck').on('change', function(){
    setTimeout(() => {
        if ($(this).prop('checked')) $('#discountPanel').collapse('show');
        else $('#discountPanel').collapse('hide');
    }, 500);
});

function myCpiToNext(myCpi){
    let temp = $(myCpi);
    let mainSlideCopy = temp.children('.cpi-main-slide').children('div').last().clone();
    let mscSRC = mainSlideCopy.children('img').attr('src'),
        mscALT = mainSlideCopy.children('img').attr('alt');
    let firstAdditionalSlideCopy = temp.children('.cpi-additional-slides').children('.slide').first().clone();
    let fascSRC = firstAdditionalSlideCopy.find('img').attr('src'),
        fascALT = firstAdditionalSlideCopy.find('img').attr('alt');
    mainSlideCopy.children('img').attr('src', fascSRC);
    mainSlideCopy.children('img').attr('alt', fascALT);
    firstAdditionalSlideCopy.find('img').attr('src', mscSRC);
    firstAdditionalSlideCopy.find('img').attr('alt', mscALT);
    temp.children('.cpi-main-slide').addClass('overflow-hidden justify-content-end');
    temp.children('.cpi-additional-slides').addClass('overflow-hidden');
    temp.children('.cpi-main-slide').prepend(mainSlideCopy);
    temp.children('.cpi-additional-slides').append(firstAdditionalSlideCopy);
    temp.children('.cpi-main-slide').addClass('slide-to-left');
    temp.children('.cpi-additional-slides').addClass('slides-to-right');
    setTimeout(() => {
        temp.children('.cpi-main-slide').children().last().remove();
        temp.children('.cpi-additional-slides').children().first().remove();
        temp.children('.cpi-main-slide').removeClass('overflow-hidden justify-content-end slide-to-left');
        temp.children('.cpi-additional-slides').removeClass('overflow-hidden slides-to-right');
    }, 900);
}

function myCpiToPrevious(myCpi){
    let temp = $(myCpi);
    let mainSlideCopy = temp.children('.cpi-main-slide').children('div').first().clone();
    let mscSRC = mainSlideCopy.children('img').attr('src'),
        mscALT = mainSlideCopy.children('img').attr('alt');
    let firstAdditionalSlideCopy = temp.children('.cpi-additional-slides').children('.slide').last().clone();
    let fascSRC = firstAdditionalSlideCopy.find('img').attr('src'),
        fascALT = firstAdditionalSlideCopy.find('img').attr('alt');
    mainSlideCopy.children('img').attr('src', fascSRC);
    mainSlideCopy.children('img').attr('alt', fascALT);
    firstAdditionalSlideCopy.find('img').attr('src', mscSRC);
    firstAdditionalSlideCopy.find('img').attr('alt', mscALT);
    temp.children('.cpi-main-slide').addClass('overflow-hidden');
    temp.children('.cpi-additional-slides').addClass('overflow-hidden justify-content-end');
    temp.children('.cpi-main-slide').append(mainSlideCopy);
    temp.children('.cpi-additional-slides').prepend(firstAdditionalSlideCopy);
    temp.children('.cpi-main-slide').addClass('slide-to-right');
    temp.children('.cpi-additional-slides').addClass('slides-to-left');
    setTimeout(() => {
        temp.children('.cpi-main-slide').children().first().remove();
        temp.children('.cpi-additional-slides').children().last().remove();
        temp.children('.cpi-main-slide').removeClass('overflow-hidden slide-to-right');
        temp.children('.cpi-additional-slides').removeClass('overflow-hidden slides-to-left justify-content-end');
    }, 900);
}

new (function(repeatInterval){
    let myCpi = $('#carousel-product-images');
    let flag = false;
    let nextRepeat = setInterval(() => {myCpi.find('.next-btn').click()}, repeatInterval);
    myCpi.find('.next-btn').on('click', function(){
        if (!flag){
            flag = true;
            clearInterval(nextRepeat);
            myCpiToNext($(this).parents('#carousel-product-images'));
            setTimeout(() => {
                flag = false;
                nextRepeat = setInterval(() => {myCpi.find('.next-btn').click()}, repeatInterval);
            }, 1000);
        }
    });
    myCpi.find('.prev-btn').on('click', function(){
        if (!flag){
            flag = true;
            clearInterval(nextRepeat);
            myCpiToPrevious($(this).parents('#carousel-product-images'));
            setTimeout(() => {
                flag = false;
                nextRepeat = setInterval(() => {myCpi.find('.next-btn').click()}, repeatInterval);
            }, 1000);
        }
    });
})(3000);

$('#product-features').on('shown.bs.collapse', function(){
    $('button[data-toggle="collapse"][data-target="#product-features"]')
        .removeClass('rounded-bottom')
        .children('i, svg').removeClass('fa-angle-down').addClass('fa-angle-up');
}).on('hidden.bs.collapse', function(){
    $('button[data-toggle="collapse"][data-target="#product-features"]')
        .addClass('rounded-bottom')
        .children('i, svg').removeClass('fa-angle-up').addClass('fa-angle-down');
}).collapse('show');

$('#my-rate-input').children('span[data-role="star"]').on('click', function(){
    let val = Number($(this).attr('data-value'));
    let stars = $('#my-rate-input').children('span[data-role="star"]');
    for (let i = 0; i < stars.length; i++){
        if (i < val) stars.get(i).innerHTML = '<i class="fa-solid fa-star"></i>';
        else stars.get(i).innerHTML = '<i class="fa-regular fa-star"></i>';
    }
    $('#my-rate-input').children('input[type="hidden"]').val(val);
});

$('#my-rate-input').children('button.eraser').on('click', function(){
    let stars = $('#my-rate-input').children('span[data-role="star"]');
    for (let i = 0; i < stars.length; i++)
        stars.get(i).innerHTML = '<i class="fa-regular fa-star"></i>';
    $('#my-rate-input').children('input[type="hidden"]').val(0);
})