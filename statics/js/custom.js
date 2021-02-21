$(document).ready(function(){
    
    setTimeout(function() {
        if ($('#info-message-form,#info-message-page').length > 0) {
        $('#info-message-form').fadeOut('slow',function(){
        $('#info-message-form').remove(); 
        });
        } 
    }, 5000);
    
});