# from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views import generic
from leads.models import Lead, Agent
from .forms import AgentModelForm
from .mixins import OrganzierAndLoginRequiredMixin


class AgentListView(OrganzierAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        #only get agents under current user's organization
        return Agent.objects.filter(organization=organization)
         

    context_object_name = 'agents'


class AgentCreateView(OrganzierAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        form.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganzierAndLoginRequiredMixin, generic.DetailView):
    
    template_name = 'agents/agent_detail.html'
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        #only show agents details under current user's organization
        return Agent.objects.filter(organization=organization)

    context_object_name = 'agent'


class AgentUpdateView(OrganzierAndLoginRequiredMixin, generic.UpdateView):
    
    template_name = 'agents/agent_update.html'
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        #only update agents data under current user's organization
        return Agent.objects.filter(organization=organization)

    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(OrganzierAndLoginRequiredMixin, generic.DeleteView):
    
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        #only delete agents under current user's organization
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse("agents:agent-list")


