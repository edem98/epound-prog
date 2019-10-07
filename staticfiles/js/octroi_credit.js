$(document).ready(function(){
  var montant_a_prelever = 0;
  var montant_a_reconvertir = 0;
  var montant_cfa = 0;

  $("#id_beneficiaire").on('change',function(){
    $.ajax({
              type: 'GET',
              url: '/membre/retourner-entreprise-info',
             data:{
                   'code_membre': $(this).text(),
                   },
            success: function(data,textStatus, jqxhr){ 
                      $("#id_epounds_disponible").val(data.epounds_dispo)
                    },
            error: function(data){
                     console.log(data)
                   }
            })
  })

     $("#id_montant_pret").on('keyup', function(){
        pret = parseInt($(this).val())
        $("#id_montant_prelever_sur_beta").val(pret)
      });

})