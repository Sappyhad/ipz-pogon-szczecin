from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView
from .models import PdfFile
from django.urls import reverse_lazy
from django import forms
from django.http import HttpResponseRedirect
from .scripts import konwerter as kw
from .scripts import scrape_csv as scrape
from django.http import FileResponse
from django.http import JsonResponse
import os
from django.conf import settings

# def index(request):
#     return render(request, 'ipz/index.html')
# class PdfFileModelForm(forms.ModelForm):
#     success_url = reverse_lazy('success')
#     class Meta:
#         model = PdfFile
#         fields = "__all__"
#         widgets = {
#             'pdf': forms.ClearableFileInput()
#         }

class CsvScraperForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())



# def download_csv(sender, instance, **kwargs):
#     # if created:
#     try:
#         print(settings.BASE_DIR)
#         path_norm = os.path.normpath(instance.pdf.url[1:])
#         pdf_path = os.path.join(settings.BASE_DIR, path_norm)
#         print("Pdf: ", pdf_path)
#         csv_path = 'csvs\\' + path_norm.split("\\")[-1].split('.')[0]
#         csv_path = os.path.join(settings.BASE_DIR, csv_path)
#         print("csv_path: ", csv_path)
#         csv_file_path = kw.convert(pdf_path, csv_path)
#         print("file_path: ", csv_file_path)
#         csv_file_name = csv_file_path.split("\\")[-1]
#         print("file_name: ", csv_file_name)
#         response = FileResponse(open(csv_file_path, 'rb'), as_attachment=True)
#         response['Content-Disposition'] = 'attachment; filename="{}"'.format(csv_file_name)
#         response['Content-Type'] = "application/csv"
#         return response
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# class pdfView(TemplateView):
#     template_name = "ipz/pdf.html"

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context['form'] = PdfFileModelForm
#         return context

    # def post(self, request, *args, **kwargs):
    #     form = PdfFileModelForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         pdf = form.cleaned_data['pdf']
    #         PdfFile_obj = PdfFile(pdf=pdf)
    #         PdfFile_obj.save()
    #         response = download_csv(None, PdfFile_obj)
    #         return response
        
class successView(TemplateView):
    template_name ="ipz/success.html"

class downloadCsvView(FormView):
    template_name = "ipz/dcv.html"
    form_class = CsvScraperForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        #scrape.scrapeTracab(username, password, settings.BASE_DIR)
        scrape.concatenate_csvs(settings.BASE_DIR)
        scrape.add_transfermarkt(settings.BASE_DIR)
        return super().form_valid(form)

# class PdfFileCreateView(CreateView):
#     model = PdfFile
#     fields = "__all__"

#     success_url = reverse_lazy('index')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class=form_class)
#         form.fields['pdf'].widget = forms.ClearableFileInput()
#         return form
