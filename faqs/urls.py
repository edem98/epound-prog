from django.urls import path
from .views import ListeSujetReponse, ask_question

app_name = 'faqs'

urlpatterns = [
    path('', ListeSujetReponse.as_view(),name="index"),
    path('ask-question/', ask_question,name="ask-question"),
]
