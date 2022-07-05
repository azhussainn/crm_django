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
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            #all leads of the organization
            return Lead.objects.filter(organization=user.userprofile)
        else:
            #leads of the current agent

            #todo: --> check why we need the commented line
            # queryset = Lead.objects.filter(organization=user.agent.organization)

            return Lead.objects.filter(agent__user=user)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            #all leads of the organization
            return Lead.objects.filter(organization=user.userprofile)
        else:
            #leads of the current agent

            #todo: --> check why we need the commented line
            # queryset = Lead.objects.filter(organization=user.agent.organization)

            return Lead.objects.filter(agent__user=user)


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
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganzierAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

