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

$('.edit-filter').on('click', function(){
    let filterName = $(this).attr('data-filter-name');
    let filterValue = $(this).attr('data-filter-value');
    let olds = decodeURI(window.location.search).substring(1);
    let startFilter = olds.search(filterName + '=');
    if (olds && startFilter === -1)
        $(this).attr('href', '?' + olds + '&' + filterName + '=' + filterValue);
    else if (olds){
        let endFilter = olds.indexOf('&', startFilter);
        if (endFilter === -1){
            olds = olds.substring(0, startFilter);
            if (olds[olds.length - 1] === '&')
                olds = olds.substring(0, olds.length - 1);
        }
        else
            olds = olds.substring(0, startFilter) + olds.substring(endFilter + 1);
        if (olds) olds = olds + '&';
        $(this).attr('href', '?' + olds + filterName + '=' + filterValue);
    }
    else
        $(this).attr('href', '?' + filterName + '=' + filterValue);
});