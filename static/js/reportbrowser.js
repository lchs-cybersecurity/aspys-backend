function sendDelete(id) {
    //makes the request
    let request = $.ajax({
        type: "POST",
        url: "{{ url_for('delete_item') }}", 
        contentType: "application/json", 
        dataType: "json",
        data: JSON.stringify({
            id: id, 
        }),  
    }); 

    request.done(function( msg ) { //success
        console.log(msg) //console logs

        $(`#report-at-${id}`).prop('hidden', true); //hides the html element that corresponds to the report
    }); 

    request.fail(function( jqXHR, textStatus ) {
        console.log(jqXHR)
    }); 
} 

function sendBlacklist(address) {
    let request = $.ajax({
        type: 'POST', 
        url: "{{ url_for('blacklist_address') }}", 
        contentType: 'application/json', 
        dataType: 'json', 
        data: JSON.stringify({
            address: address, 
        })
    }); 

    request.done(function(msg) {
        console.log(msg); 
    }); 

    request.fail(function( jqXHR, textStatus ) {
        console.log(jqXHR)
    }); 
} 

function createPopup($this) {
    const href = $this.attr('href'); // gets the href of the a element

    let el = $(`
    <div class="veritas-link-confirm">
        <div class="veritas-icon"></div>
        <p class='link-confirm-text'>Since this is a potential phising email, the links may lead to malicious sites! Proceed with caution. This link goes to: </p>
        <p class='link-confirm-href'>${href}</p> 
        </br>
        <div class="veritas-buttons">
            <button class="veritas-cancel">Cancel</button>
            <button class="veritas-proceed">Proceed</button>
        </div>
    </div>
    `); // creates the popup element
    
    el.insertAfter($this); // places it after the a element

    el.find('.veritas-cancel').click(function(e) { // when you click the cancel button
        el.remove(); 
    }); 

    el.find('.veritas-proceed').click(function(e) { //when you click the proceed button
        window.open(href); 

        el.remove(); 
    })
}

function neuterLinks() {
    let as = $('.report-body').find('a'); // finds all the a elements in each report body

    //console.log(as); 

    as.click(function(e) {
        let $this = $(this); 

        e.preventDefault(); // prevents the click from opening the link (the default behavior) 

        const next = $this.next('.veritas-link-confirm'); // does it already have a corresponding popup? 

        //console.log(next); 

        if (!next.length) { // if not, create one
            createPopup($this); 
        }
    })
} 

$(document).ready(function() {
    $('.deleter-button').click(function(e) { //le event for when you click dat delete button
        let id = this.getAttribute('will-delete'); //each of these buttons has this attribute, specifying which report to delete

        sendDelete(id); 
    }); 

    $('.blacklist-button').click(function(e) {
        let address = this.getAttribute('blacklists'); 

        sendBlacklist(address); 
    })

    $('.full-report-toggle').click(function(e) { //when you click anywhere on the report header thing
        //console.log(this.children); 
        let id = this.getAttribute('toggles'); 

        $(`#full-report-${id}`).slideToggle(); //toggles the s l i d e
    }); 

    neuterLinks(); 
}); 