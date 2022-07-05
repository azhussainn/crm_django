from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Lead, Agent
from .forms import LeadModelForm, CustomUserCreateForm
from agents.mixins import OrganzierAndLoginRequiredMixin



class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreateForm

    def get_success_url(self):
        return reverse("login")


class LandingView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(OrganzierAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        #Todo send email notification
        send_mail(
            subject="Lead has been created successfully",
            message=f"Go to the site to view the new lead",
            from_email='test@test.com',
            recipient_list=["test@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganzierAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganzierAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

