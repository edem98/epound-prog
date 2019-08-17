from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from services.views import *
from . import settings
from django.conf.urls.static import static
from faqs.views import ListeSujetReponse
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()

router.register(r'ville', VilleViewSet)
router.register(r'quartier', QuartierViewSet)
router.register(r'membre', MembreViewSet)
router.register(r'particulier', ParticulierViewSet)
router.register(r'entreprise', EntrepriseViewSet)
router.register(r'trader', TraderViewSet)
router.register(r'vendeur', EntrepriseCommercialeViewSet)
router.register(r'besoin', BesoinViewSet)
router.register(r'specification', SpecificationViewSet)
router.register(r'produit', ProduitViewSet)
router.register(r'commandes', CommandeClientViewSet)
router.register(r'transaction-inter-consommateur', TransactionInterComsommateurViewSet)
router.register(r'transaction-commercial-consommateur', TransactionCommercialComsommateurViewSet)
router.register(r'conversion-trader', ConversionTraderViewSet)
router.register(r'reconversion-trader', ReconversionTraderViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'transfert-consommateur-entreprise', TransactionConsommateurCommercialViewSet)
router.register(r'payement-inter-entreprise', PayementInterCommercialViewSet)
router.register(r'payement-inter-entreprise-compte-conso', PayementInterCommercialAvecCompteConsommationViewSet)
router.register(r'creation-particulier-trader', CreationParticulierParTraderViewSet)
router.register(r'creation-particulier-trader-integrateur', CreationParticulierParTraderEtIntegrateurViewSet)
router.register(r'creation-entreprise-trader', CreationEntrepriseParTraderViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'vente-vendeur', VendeurVenteViewSet)
router.register(r'reactivation-client', ReactivationClientViewSet)
router.register(r'message-client', MessageClientViewSet)

urlpatterns = [

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
    path('', views.acceuil, name="acceuil"),
    path('vendeurs', views.ListEntreprise.as_view(), name="vendeurs"),
    path('about', views.about, name="about"),
    path('partenaires', views.partenaires, name="partenaires"),
    path('faqs', ListeSujetReponse.as_view(), name="faqs"),
    path('contact/', views.contact, name="contact"),
    path('politique-confidentialite/', views.politique, name="politique"),
    path('membre/', include('membre.urls'), ),
    path('api/', include(router.urls)),
    path('ecommerce/', include('ecommerce.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
