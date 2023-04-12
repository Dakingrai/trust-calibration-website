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
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
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

@login_required
def start_study(request):
    study_samples = Study.objects.filter(user=request.user, viewed=False).order_by('id').first()
    if study_samples:
        return redirect(reverse('study', kwargs={'pk': study_samples.id}))
    else:
        messages.success(request, f'You have completed the study!')
        return redirect(reverse('home'))

@login_required
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
    
    db_name = study_sample.sample.database_name
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
    sorted_ab = sorted(zip(comp_conf, comp_exp), reverse=True)
    sorted_comp_conf, sorted_comp_exp = [list(t) for t in zip(*sorted_ab)]
    sorted_ac = sorted(zip(comp_conf, feature_attr), reverse=True)
    sorted_comp_conf, sorted_feature_attr = [list(t) for t in zip(*sorted_ac)]
    if len(comp_conf) > 1:
        mid_comp_conf = [max(comp_conf), min(comp_conf)]
        mid_comp_exp = [comp_exp[comp_conf.index(max(comp_conf))], comp_exp[comp_conf.index(min(comp_conf))]]
        mid_feature_attr = [feature_attr[comp_conf.index(max(comp_conf))], feature_attr[comp_conf.index(min(comp_conf))]]
        mid = True
        mid_desc = ["most", "least"]
    else:
        mid_comp_conf = comp_conf
        mid_comp_exp = comp_exp
        mid_feature_attr = feature_attr
        mid = False
        mid_desc = []
    question = study_sample.sample.question.split()
    ques_and_feat_attr = [zip(question, each) for each in sorted_feature_attr]
    ques_and_feat_attr_mid = [zip(question, each) for each in mid_feature_attr]
    
    context = {
        'db': final_context,
        'question': study_sample.sample.question,
        'db_records': ast.literal_eval(study_sample.sample.db_records),
        'comp_exp': comp_exp,
        'feature_attr_mid': zip(ques_and_feat_attr_mid, mid_comp_exp, mid_comp_conf, mid_desc),
        'feature_attr_high': zip(ques_and_feat_attr, sorted_comp_exp, sorted_comp_conf),
        'overall_conf': study_sample.sample.confidence,
        'hardness': study_sample.sample.hardness,
        'pred_sql': study_sample.sample.pred_sql,
        'ground_sql': study_sample.sample.ground_sql,
        "no_tables": len(final_context),
        "db_name": db_name,
    }
    return render(request, 'main/study.html', {'study_sample': context})

