function sendDelete(id) {
    console.log(org_id); 
    
    //makes the request
    let request = $.ajax({
        type: "POST",
        url: urls.delete_item, 
        contentType: "application/json", 
        dataType: "json",
        data: JSON.stringify({
            org_id: org_id, 
            id: id, 
        }),  
    }); 

    request.done(function( msg ) { //success
        console.log(msg) //console logs

        $(`#assessment-at-${id}`).prop('hidden', true); //hides the html element that corresponds to the assessment
    }); 

    request.fail(function( jqXHR, textStatus ) {
        console.log(jqXHR)
    }); 
} 
$(document).ready(function() {
    $('.deleter-button').click(function(e) { //le event for when you click dat delete button
        let id = this.getAttribute('will-delete'); //each of these buttons has this attribute, specifying which assessment to delete

        sendDelete(id); 
    }); 

    $('.full-assessment-toggle').click(function(e) { //when you click anywhere on the assessment header thing
        //console.log(this.children); 
        let id = this.getAttribute('toggles'); 

        $(`#full-assessment-${id}`).slideToggle(); //toggles the s l i d e
    }); 
}); 