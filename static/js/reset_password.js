$(document).ready(function(){
    //recuperer le formulaire
    $('.password').on('click',function(e){
        e.preventDefault();
        var user = $(this);
        user.html('mise a jour');
        $.post(user.attr('href'), user.id)
        .done(function(data,text,jqxhr){
                user.closest('td').siblings('.field-mdp').html(data.password)
                user.html('Générer mot de passe');
         })
        .fail(function(jqxhr){
            console.log(jqxhr);
         })
        .always(function(){
            user.html('Générer mot de passe');
        })
    })
});