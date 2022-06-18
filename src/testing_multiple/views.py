from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Topic, Details

# Create your views here.
class Testing(View):
    template_name= "teee.html"

    def get(self, request, *args, **kwargs):
        qs= Topic.objects.all()
        context = {
            "qs":qs
        }
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        topics = request.POST.getlist("subject")

        a = Details.objects.create(name="ram")
        a.topic.set(topics)
        a.save()
        print(a.topic.all())
        
        return HttpResponse("AAAAA")
        