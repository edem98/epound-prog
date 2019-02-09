jQuery(document).ready(function($){
  var montant_a_prelever = 0;
  var montant_a_reconvertir = 0;
  var montant_cfa = 0;

  $("#id_beneficiaire").on('change',function(){
    var id = $(this).val();
    $.ajax({
              type: 'GET',
              url: '/membre/retourner-consommateur-info',
             data:{
                   'id': id,
                   },
            success: function(data,textStatus, jqxhr){
                      $("#id_epounds_disponible").val(data.epounds_dispo)
                    },
            error: function(data){
                     console.log(data)
                   }
            })
     code = 0;
  })

     $("#id_epounds_a_reconvertir").on('keyup', function(){
        montant_a_reconvertir = parseInt($(this).val())
        montant_a_prelever = (montant_a_reconvertir*40)/100
        montant_cfa = montant_a_reconvertir - montant_a_prelever

        $("#id_montant_a_prelever").val(montant_a_prelever)
        $("#id_montant_en_cfa").val(montant_cfa)

      });

    $("#id_epounds_a_reconvertir").on('focusout', function(){
        if(parseInt($(this).val()) >  parseInt($("#id_epounds_disponible").val())){
          alert('le bénéficiare ne dispose pas du montant destiné à la reconversion.Veuillez spécifiez une autre valeur');
          $("#id_montant_a_prelever").val(0)
          $("#id_montant_en_cfa").val(0)
        }
      });


});