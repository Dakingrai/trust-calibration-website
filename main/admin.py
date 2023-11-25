from django.contrib import admin
from .models import Study, Samples, Spider_db, db_test, Hyperparameters, SqlExplanation, UserTransaprency, TrainingSamples, TrainingStudy, UserTrust, UserAgreement, JianTrustScale
from django.urls import path
from django.shortcuts import render
from django import forms
import pdb
import ast
import json
from django.http import HttpResponseRedirect
from django.contrib import messages

class JsonUploadForm(forms.Form):
    json_file = forms.FileField()

class StudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sample', 'user_response', 'viewed', 'created', 'updated', 'start_time')
    list_filter = ['user']
    save_on_top = True
    list_editable = ['viewed', 'user_response']
    
class SamplesAdmin(admin.ModelAdmin):
    list_display = ('sample_name', 'question', 'database_name', "hardness", "correct_prediction")
    list_filter = ['database_name', "hardness", "correct_prediction"]
    save_on_top = True

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-json/', self.upload_json)]
        return new_urls + urls
    
    def upload_json(self, request):
        if request.method == 'POST':
            json_file = request.FILES['json_file']
            if not json_file.name.endswith('.json'):
                messages.error(request, 'File is not JSON type')
                return HttpResponseRedirect(request.path_info)
            file_data = json_file.read().decode("utf-8")
            parsed_data = ast.literal_eval(file_data)
            for each in parsed_data:
                created = Samples.objects.update_or_create(
                    question=each['question'],
                    ground_sql=each['ground_sql'],
                    pred_sql=each['pred_sql'],
                    hardness=each['hardness'],
                    db_records=each['db_records'],
                    components=each['components'],
                    feature_attribution=each['feature_attribution'],
                    confidence=each['confidence'],
                    correct_prediction=each['correct_prediction'],
                    database_name=each['database_name'],
                )
            messages.success(request, 'JSON file uploaded successfully')
            return HttpResponseRedirect('admin/main/samples/')
        form = JsonUploadForm()
        data = {"form": form}
        return render(request, 'admin/json_upload.html', data)

admin.site.register(Samples, SamplesAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Spider_db)
admin.site.register(db_test)
admin.site.register(Hyperparameters)
admin.site.register(SqlExplanation)
admin.site.register(UserTransaprency)
admin.site.register(TrainingSamples)
admin.site.register(TrainingStudy)
admin.site.register(UserTrust)
admin.site.register(UserAgreement)
admin.site.register(JianTrustScale)
admin.site.site_header = "Trust Calibration Admin"

