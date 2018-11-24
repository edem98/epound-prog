from compte.models import CompteAlpha, CompteGrenier, CompteBeta

def compte_alpha(request):
	return {'compte_alpha': CompteAlpha.load()}

def compte_grenier(request):
	return {'compte_grenier': CompteGrenier.load()}

def compte_beta(request):
	return {'compte_beta': CompteBeta.load()}