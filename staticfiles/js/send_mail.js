$(document).ready(function(){
    //recuperer le formulaire
    $('#mail_form').on('submit',function(e){
        e.preventDefault();
        var form = $(this);
        form.find('button').text('Chargement');
        $.post(form.attr('action'),form.serializeArray())
        .done(function(data,text,jqxhr){
                console.log(jqxhr);
         })
        .fail(function(jqxhr){
            console.log(jqxhr);
         })
        .always(function(){
            form.find('button').text('Envoyer');
        })
    })
});