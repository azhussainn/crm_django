from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm



def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, 'leads/lead_list.html', context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = { "lead": lead }
    return render(request, 'leads/lead_detail.html', context)


def lead_create(request):
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect("/leads")


    context = {
        "form": LeadModelForm()
    }
    return render(request, 'leads/lead_create.html', context)