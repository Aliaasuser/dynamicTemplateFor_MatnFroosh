function getMoreComments(url){
    $.get(
        url + '?show-more-than=' + $('.comments-container .my-comment').length,
        function(data, status){
            if (status === 'success'){
                $("#comments-container [id^='comment_num_']").remove();
                $('#comments-container').prepend(data.htmlResponse);
                let temp = $('#comments-container .my-rating-type1');
                for (let i = 0; i < temp.length; i++){
                    let t = $(temp.get(i));
                    t.css('clip-path', 'polygon(0% 0%, ' + t.attr('data-value') + '% 0%, ' + t.attr('data-value') + '% 100%, 0% 100%)')
                        .parent().append(Number(t.attr('data-value')) / 20);
                };
                if (data.is_complete)
                    $('#more-comments').remove();
            }
        },
        'json'
    );
}