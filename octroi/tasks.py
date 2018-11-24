from celery.decorators import task
from membre.models import EntrepriseCommerciale
from dashboard.models import Remboursement
from octroi.models import OctroiCredit


@task
def remboursemment_automatique():
    entreprises = EntrepriseCommerciale.objects.filter(compte_entreprise_commercial__credit = 1)

    for entreprise in entreprises:
        octroi = OctroiCredit.objects.get(beneficiaire=entreprise)
        montant_a_rembourser = octroi.montant_pret / octroi.delais_rembousement
        montant_rembourser = 0
        reste = 0
        gap = montant_a_rembourser - entreprise.compte_entreprise_commercial.compte_business.solde
        if gap < 0:
            montant_rembourser = montant_a_rembourser
            entreprise.compte_entreprise_commercial.compte_business.solde -= montant_rembourser
            entreprise.compte_entreprise_commercial.compte_business.save()
            reste = entreprise.compte_entreprise_commercial.credit - montant_rembourser
            entreprise.compte_entreprise_commercial.credit -= montant_rembourser
            entreprise.compte_entreprise_commercial.save()
        else :
            montant_rembourser = montant_a_rembourser - gap
            entreprise.compte_entreprise_commercial.compte_business.solde -= montant_rembourser
            entreprise.compte_entreprise_commercial.compte_business.save()
            reste = entreprise.compte_entreprise_commercial.credit - montant_rembourser
            entreprise.compte_entreprise_commercial.credit -= montant_rembourser
            entreprise.compte_entreprise_commercial.save()
        Remboursement.objects.create(entreprise = entreprise,montant_emprunter = octroi.montant_pret,
                                     credit_actuel = entreprise.compte_entreprise_commercial.credit,
                                     montant_rembourser = montant_rembourser,reste = reste)


