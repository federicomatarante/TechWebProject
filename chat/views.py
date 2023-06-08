from django.views.generic import TemplateView


# Create your views here.
class UserChatView(TemplateView):
    template_name = 'chat.html'
