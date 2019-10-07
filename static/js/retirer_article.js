$(document).ready(function(){
    //recuperer le formulaire
    $('#article_form').on('submit',function(e){
        e.preventDefault();
        var form = $(this);
        checkboxes = [];
        $(".form-check").each(function(){
           if($(this).prop("checked") == true){
                checkboxes.push(parseInt($(this).attr("id")));
            }
        });
        $.post(form.attr('action'),{'checkboxes': checkboxes})
        .done(function(data,text,jqxhr){
                console.log(jqxhr);
                location.reload(true);
         })
        .fail(function(jqxhr){
            console.log(jqxhr);
         })
    })
});