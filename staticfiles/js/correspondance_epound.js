$(document).ready(function(){

	$("#id_montant_debouse").on('keyup',function(){
		var code_membre = $("#select2-id_beneficiaire-container").text()
		$.ajax({
                    type: 'GET',
                    url: '/membre/retourner-taux-membre/',
                    data:{
                       'code_membre': code_membre,
                    },
                    success: function(data,textStatus, jqxhr){
                       var taux = data.taux
                       montant_debouse = $("#id_montant_debouse").val()
                       montant_debouse = parseInt(montant_debouse)
                       epound_correspondant = ((montant_debouse*taux)/100)+montant_debouse
                       $('#id_unite_epound_correspondant').val(epound_correspondant)
                    },
                    error: function(data){
                       console.log(data)
                    }
              })
	})
});
	
