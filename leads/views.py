from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Lead, Agent, Category
from .forms import (
    LeadModelForm, CustomUserCreateForm, 
    AssignAgentForm, LeadCategoryUpdateForm
)
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
            return Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=False
            )
        else:
            #leads of the current agent

            #todo: --> check why we need the commented line
            # queryset = Lead.objects.filter(organization=user.agent.organization)

            return Lead.objects.filter(agent__user=user)
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


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
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
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


class AssignAgentView(OrganzierAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        agent = form.cleaned_data["agents"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.organization = agent.organization
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'

    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):

        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organizer:
            queryset =  Lead.objects.filter(
                organization=user.userprofile,
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization,
            )
            
        context.update({
            "unassigned_lead_count" : queryset.filter(category__isnull=True).count()
        })

        return context


    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            return Category.objects.filter(
                organization=user.userprofile,
            )
        else:
            return Category.objects.filter(
                organization=user.agent.organization,
            )


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'

    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            return Category.objects.filter(
                organization=user.userprofile,
            )
        else:
            return Category.objects.filter(
                organization=user.agent.organization,
            )


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            #all leads of the organization
            return Lead.objects.filter(organization=user.userprofile)
        else:
            #leads of the current agent
            return Lead.objects.filter(agent__user=user)

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={'pk': self.kwargs['pk']})