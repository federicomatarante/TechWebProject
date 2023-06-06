from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, FormView

from GymApp.models import Notifications
from GymApp.utils import isPersonalTrainer
from bullettinboard.forms import MessageForm
from bullettinboard.models import Message


class BullettinBoardView(LoginRequiredMixin, ListView, FormView):
    model = Message
    template_name = 'bullettinboardpage.html'
    form_class = MessageForm
    success_url = reverse_lazy('bullettinboard')
    context_object_name = 'messages'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        if not isPersonalTrainer(request.user):
            return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        Notifications.objects.filter(pk=self.request.user.notifications.pk).update(bullettinboard=False)
        return Message.objects.all().order_by('-creation_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = context['page_obj'].number
        total_pages = context['page_obj'].paginator.num_pages
        if total_pages <= 5:
            context['navigator_numbers'] = [i for i in range(1, total_pages + 1)]
        elif page_number + 5 <= total_pages:
            context['navigator_numbers'] = [i for i in range(page_number, page_number + 5)]
        else:
            context['navigator_numbers'] = [i for i in range(total_pages - 4, total_pages + 1)]
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        Notifications.objects.exclude(pk=self.request.user.notifications.pk).update(bullettinboard=True)
        return super().form_valid(form)


@require_POST
@login_required
@user_passes_test(isPersonalTrainer)
def message_delete(request, id: int):
    message = get_object_or_404(Message, id=id)
    message.delete()
    return redirect('bullettinboard')
