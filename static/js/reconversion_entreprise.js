jQuery(document).ready(function($){

  var montant_a_prelever = 0;
  var montant_a_reconvertir = 0;
  var montant_reconverti = 0;
  var montant_cfa = 0;
  var montant_virer = 0;
  var entreprise = 0;

  $("#id_beneficiaire").on('change',function(){
    if($("#id_beneficiaire").val() != entreprise){
       entreprise = $("#id_beneficiaire").val()
       $.ajax({
            type: 'GET',
            url: '/membre/retourner-entreprise-info',
            data:{
                   'id': entreprise,
                   },
            success: function(data,textStatus, jqxhr){
                      $("#id_epounds_disponible").val(data.epounds_dispo)
                    },
            error: function(data){
                     console.log(data)
                   }
            })
  }})


  $("#id_epounds_a_reconvertir").on('keyup', function(){
    if(!$(this).val()){
      console.log('pas de valeur')
    }
    else{
      montant_a_reconvertir = $(this).val()
      montant_a_prelever = parseInt((montant_reconverti*50)/100)
      montant_reconverti = montant_a_reconvertir - montant_a_prelever
      montant_cfa = parseInt((montant_reconverti*70)/100)
      montant_virer = montant_reconverti -montant_cfa
      $("#id_montant_a_prelever").val(montant_a_prelever);
      $("#id_montant_en_cfa").val(montant_cfa)
      $("#id_montant_virer_sur_compte_conso").val(montant_virer)
      montant_a_reconvertir = 0
      montant_a_prelever = 0
      montant_cfa = 0
      montant_virer = 0

    }

  });

  $("#id_epounds_a_reconvertir").on('focusout', function(){
        if(parseInt($(this).val()) >  parseInt($("#id_epounds_disponible").val())){
          alert('le bénéficiare ne dispose pas du montant destiné à la reconversion.Veuillez spécifiez une autre valeur');
          $("#id_montant_a_prelever").val(0)
          $("#id_montant_en_cfa").val(0)
          $("#id_montant_virer_sur_compte_conso").val(0)
        }
  });
});