from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Samples, Study, db_test
from .forms import StudyForm
import random
from django.http import HttpResponse
import pdb
import ast

def home(request):
    return render(request, 'main/home.html')


def create_samples(request):
    check_samples = Study.objects.filter(user=request.user)
    if len(check_samples) == 0:
        all_samples = Samples.objects.all()
        random_sample = [all_samples[i] for i in sorted(random.sample(range(len(all_samples)), 2))]
        for each in random_sample:
            StudyInstance = Study(user=request.user, sample=each)
            StudyInstance.save()
        messages.success(request, f'Your samples have been created!')
    else:
        messages.error(request, f'You already have samples!')
    return redirect(reverse('home'))


def start_study(request):
    study_samples = Study.objects.filter(user=request.user, viewed=False).order_by('id').first()
    if study_samples:
        return redirect(reverse('study', kwargs={'pk': study_samples.id}))
    else:
        messages.success(request, f'You have completed the study!')
        return redirect(reverse('home'))


def study(request, pk):
    study_sample = Study.objects.get(id=pk)
    if request.method == 'POST':
        btn_value = bool(int(request.POST.get('btn_value')))
        if btn_value:
            study_sample.user_response = True
        else:
            study_sample.user_response = False
        study_sample.viewed = True
        study_sample.save()
        return redirect(reverse('start-study'))
    
    db_name = study_sample.sample.database.db_name
    all_db_schema = db_test.objects.all().first().all_db
    all_db_schema = ast.literal_eval(all_db_schema)
    schema_and_values = all_db_schema[db_name]
    final_context = []
    for each in schema_and_values:
        final_context.append({'table_name': each['table_name'],
                              'columns': [c.strip() for c in each['columns'].strip().split(",")],
                              'values': ast.literal_eval(each['records'])
                              })
    # pdb.set_trace()
    comp_exp = ast.literal_eval(study_sample.sample.comp_explanations)
    feature_attr = ast.literal_eval(study_sample.sample.feature_attribution)
    comp_conf = ast.literal_eval(study_sample.sample.comp_confidence)
    question = study_sample.sample.question.split()
    ques_and_feat_attr = [zip(question, each) for each in feature_attr]
    context = {
        'db': final_context,
        'question': study_sample.sample.question,
        'db_records': ast.literal_eval(study_sample.sample.db_records),
        'comp_exp': comp_exp,
        'feature_attr': zip(ques_and_feat_attr, comp_exp, comp_conf),
        'hardness': study_sample.sample.hardness,
        'pred_editsql': study_sample.sample.pred_editsql,
        'ground_editsql': study_sample.sample.ground_editsql,
    }
    return render(request, 'main/study.html', {'study_sample': context})
