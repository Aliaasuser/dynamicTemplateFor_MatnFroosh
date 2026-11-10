$('.add-filter').on('click', function(event){
    let newFilter = $(this).attr('data-filter');
    let olds = window.location.search;
    let newSearch = ''
    if (olds && olds.search(encodeURI(newFilter)) === -1)
        newSearch = olds + '&' + newFilter;
    else if (!olds)
        newSearch = '?' + newFilter;
    else{
        event.preventDefault();
        return;
    }
    $(this).attr('href', newSearch);
});