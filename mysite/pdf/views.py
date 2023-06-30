from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponseServerError

# Create your views here.
def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
        profile = Profile.objects.create(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,university=university,previous_work=previous_work,skills=skills)
        if profile:
            return resume(profile.id)
    else:
        return render(request,'pdf/accept.html')

def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

def resume(id):
    user_profile = Profile.objects.get(pk=id)
    pdf = html_to_pdf('pdf/resume.html', {'user_profile': user_profile})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "resume.pdf"
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    else:
        return HttpResponseServerError("Error generating PDF")
    
#     template = loader.get_template('pdf/resume.html')
#     html = template.render({'user_profile':user_profile})
#     options ={
#         'page-size': 'Letter',
#         'encoding': "UTF-8",
#     }
#     pdf = pdfkit.from_string(html,False,options)
#     response = HttpResponse(pdf,content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment'
#     filename = 'resume.pdf'
#     return response

# def accept(request):
#     return render(request,'pdf/accept.html')