from django.views.generic import ListView, FormView
from django.urls import  reverse_lazy
from buddies.models import Buddy
from buddies.forms import BuddyCreationForm
from forum.views import LoginRequiredMixin


# Create your views here.
class BuddiesView(ListView):
    context_object_name = "buddies_list"
    template_name = "buddies.html"

    def get_queryset(self):
        return Buddy.objects.all() # Buddy.objects.filter(owner=self.request.user.member)

class CreateBuddyView(FormView, LoginRequiredMixin      ):
    form_class = BuddyCreationForm
    template_name = "create_buddy.html"
    success_url = reverse_lazy("buddies")