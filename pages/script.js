$(this).ready(function() {
    $('.toggler').click(function(e) {
        let element = $(e.target); 
        let index = element.attr('index'); 

        $(`.toggleable[index=${index}]`).toggleClass('hidden')
    }); 

    $('')
}); 