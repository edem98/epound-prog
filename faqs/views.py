#from django.shortcuts import render
from django.views.generic import ListView
from .models import *

class ListeSujetReponse(ListView):
	model = Sujet
	template_name = "faqs/faqs.html"
	context_object_name = "sujets"
	paginate_by = 15
	queryset = Sujet.objects.all()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		question_reponse = ProblemeSolution.objects.all()
		context['sujet_items'] = question_reponse
		return context
