function sendList(url, list) { // for blacklists and whitelists alike
    let request = $.ajax({ // the request
        type: 'POST', 
        url: url, 
        contentType: 'application/json', 
        dataType: 'json', 
        data: JSON.stringify({
            org_id: org_id, 
            list: list, 
        })
    }); 

    request.done(function(msg) { // success
        console.log(msg); 
    }); 

    request.fail(function( jqXHR, textStatus ) { // failure
        console.log(jqXHR)
    }); 
} 

function writeListInput(sel, list) { // write "starting text" to a textarea
    const list_str = list.join('\n'); 
    const $sel = $(sel); 

    $sel.val(list_str); // sets value
    $sel.trigger('input'); // triggers input event (since stuff was written to the field) 
}

function loadListReq(url) { // the request for GETting black/whitelist
    console.log(url); 

    let request = $.ajax({
        type: "GET",
        url: url, 
        dataType: 'json', 
        data: {
            org_id: org_id, 
        }, 
    }); 

    return request; 
} 

function loadList(url, sel) { // loads black/whitelist setting and writes to page
    let req = loadListReq(url); // the request
    let list; 

    req.done(function(msg) {
        console.log(msg); 

        list = msg.data; 

        writeListInput(sel, list); // writes to page
    }); 

    req.fail(function( jqXHR, textStatus ) {
        console.log(jqXHR); 
        console.log(textStatus); 
    }); 
} 

function validEmail(address) {
    let valid; 

    const bannedChars = [' ']; // characters that aren't possible in an email address

    let hasBannedChar = false; 

    for (let char of bannedChars) {
        if (address.indexOf(char) >= 0) {
            hasBannedChar = true; 

            break; 
        }
    } 

    if (!hasBannedChar) {
        let split = address.split('@'); 

        if (split.length === 2) { // there can only be one @ symbol
            let [first, second] = split; 

            valid = first.length && second.length; // both sides must be not empty
        } else {
            valid = false; 
        } 
    } else {
        valid = false; 
    }

    return valid; 
}

function requireValidEmail(inputSel, buttonSel, formatErrorMsg) { // adds an event that disables/enables the submit button depending on whether the emails entered are valid
    let $input = $(inputSel); 
    let $button = $(buttonSel); 

    $input.on('input', function(e) {
        //console.log('e'); 

        let $this = $(this); 

        let val = $this.val(); // the value in the field
        let valid = true; 

        if (val) {
            let list = val.split('\n'); 

            for (let address of list) {
                valid = validEmail(address); 

                if (!valid) {
                    break; 
                }
            } 
        } 

        $button.attr('disabled', !valid); 
        $(formatErrorMsg).css('display', (valid?'none':'initial'));
    })
}

$(document).ready(function() {
    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
    }).on('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    }); // resizes the text box with every input

    requireValidEmail('#blacklist_input', '#blacklist_submit', '#blacklist_format_error_msg'); 
    requireValidEmail('#whitelist_input', '#whitelist_submit', '#whitelist_format_error_msg'); 
    requireValidEmail('#testaddrlist_input', '#testaddrlist_submit', '#testaddrlist_format_error_msg'); 

    $('#blacklist_submit').click(function(e) { // what happens when you click the blacklist submit
        let input = $('#blacklist_input').val(); 
        let blacklist = input ? input.split('\n') : []; 

        sendList(urls.set_blacklist, blacklist); 
    }); 

    $('#whitelist_submit').click(function(e) { // what happens when you click the whitelist submit
        let input = $('#whitelist_input').val(); 
        let whitelist = input ? input.split('\n') : []; 

        sendList(urls.set_whitelist, whitelist); 
    }); 

    $('#testaddrlist_submit').click(function(e) { // what happens when you click the testaddrlist submit
        let input = $('#testaddrlist_input').val(); 
        let testaddrlist = input ? input.split('\n') : []; 

        sendList(urls.set_testaddrlist, testaddrlist); 
    }); 

    loadList(urls.get_blacklist, '#blacklist_input'); 
    loadList(urls.get_whitelist, '#whitelist_input'); 
    loadList(urls.get_testaddrlist, '#testaddrlist_input'); 
}); 