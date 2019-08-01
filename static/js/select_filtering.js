$(document).ready(function(){
    $('#entreprisecommerciale_form > div > fieldset.module.aligned.module_1.initialized.selected > div.form-row.field-besoin_gere > div > div > span')
    .on('mouseenter',function(){
        var besoin = $('#id_besoin_fondamental').val()
        var specification = $('#id_besoin_gere').val()
        if(besoin){
            $.get( '/ecommerce/specification-besoin',{ 'besoin': besoin, })
              .done(function(data) {
                $('#id_besoin_gere').find('option').remove()
                data.specifications.forEach(function(specification,index){
                    $('#id_besoin_gere').append(new Option(specification.label, specification.id, true,true));
                })
                console.log(data.specifications);
              })
              .fail(function() {
                alert( "error" );
              })
          }
        else{
            alert("Veillez selectioner un domaine d'activite en premier")
        }
    })

});