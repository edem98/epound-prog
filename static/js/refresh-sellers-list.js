$(document).ready(function(){
    $('.needs').on('click', function(e){
        e.preventDefault();
        $('#sellers').hide(500);
        $('#sellers').empty();
        $('#search-animation').show(1000);
        $.ajax({
            url: $(this).attr('href'),
            success: function(result){
                var vendeurs = result.vendeurs
                if (vendeurs === undefined || vendeurs.length == 0) {
                    $('#sellers').append(
                        '<div class="text-center" style="color: green;">'+
                        '<h2 style="color: green;">Aucun vendeur ne couvre ce besoin actuellement</h2>'+
                        '</div>'
                    );
                }
                else {
                    var i;
                    for (i = 0; i < vendeurs.length; i++) {
                      if (vendeurs[i].localisation != "" && vendeurs[i].objet_social != ""){
                        $('#sellers').append(
                            '<li class="list-group-item align-items-center">'+
                                '<div class="row">'+
                                      '<div class="col-lg-3 col-md-3 col-sm-12 text-center">'+
                                          '<img src="'+ vendeurs[i].banniere_principal+'" alt="Sellers image" '+
                                            'style="border-radius: 10px;max-width: 200px; max-height: 120px;width: 100%;height: auto;"/>'+
                                          '<h6 class="mt-3">'+ vendeurs[i].nom +'</h6>'+
                                  '</div>'+
                                      '<div class="mt-2 col-lg-3 col-md-3 col-sm-12">'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">Tel: '+ vendeurs[i].telephone + '</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">' + vendeurs[i].email +'</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">siège: '+ vendeurs[i].emplacement +'</p>' +
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">'+
                                        '<a href="'+vendeurs[i].localisation+'" style="text-decoration: none;" target="_blank">Voir sur google maps</a>'+
                                        '</p>'+
                                      '</div>'+
                                      '<div class="col-lg-6 col-md-6 col-sm-12 text-success">'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green; text-align: justify;">'+
                                        '<h5>Object social:</h5>' + vendeurs[i].objet_social + ''+
                                        '</p>'+
                                      '</div>'+
                                  '</div>'+
                            '</li>'
                        );
                      }
                      else if(vendeurs[i].localisation != ""){
                        $('#sellers').append(
                            '<li class="list-group-item align-items-center">'+
                                '<div class="row">'+
                                      '<div class="col-lg-3 col-md-3 col-sm-12 text-center">'+
                                          '<img src="'+ vendeurs[i].banniere_principal+'" alt="Sellers image" '+
                                            'style="border-radius: 10px;max-width: 200px; max-height: 120px;width: 100%;height: auto;"/>'+
                                          '<h6 class="mt-3">'+ vendeurs[i].nom +'</h6>'+
                                  '</div>'+
                                      '<div class="mt-2 col-lg-3 col-md-3 col-sm-12">'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">Tel: '+ vendeurs[i].telephone + '</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">' + vendeurs[i].email +'</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">siège: '+ vendeurs[i].emplacement +'</p>' +
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">'+
                                        '<a href="'+vendeurs[i].localisation+'" style="text-decoration: none;" target="_blank">Voir sur google maps</a>'+
                                        '</p>'+
                                      '</div>'+
                                      '<div class="col-lg-6 col-md-6 col-sm-12 text-success">'+

                                      '</div>'+
                                  '</div>'+
                            '</li>'
                        );
                      }
                      else if(vendeurs[i].objet_social != ""){
                        $('#sellers').append(
                            '<li class="list-group-item align-items-center">'+
                                '<div class="row">'+
                                      '<div class="col-lg-3 col-md-3 col-sm-12 text-center">'+
                                          '<img src="'+ vendeurs[i].banniere_principal+'" alt="Sellers image" '+
                                            'style="border-radius: 10px;max-width: 200px; max-height: 120px;width: 100%;height: auto;"/>'+
                                          '<h6 class="mt-3">'+ vendeurs[i].nom +'</h6>'+
                                  '</div>'+
                                      '<div class="mt-2 col-lg-3 col-md-3 col-sm-12">'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">Tel: '+ vendeurs[i].telephone + '</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">' + vendeurs[i].email +'</p>'+
                                        '<p style="font-family: Ubuntu, sans-serif;color: green;">siège: '+ vendeurs[i].emplacement +'</p>' +
                                      '</div>'+
                                      '<div class="col-lg-6 col-md-6 col-sm-12 text-success">'+

                                      '</div>'+
                                  '</div>'+
                            '</li>'
                        );
                      }
                    }
                }

                $('#search-animation').hide(1000);
                $('#sellers').show(1000)

            },
            error: function(result){
                console.log(result);
            }
          });

    })

});