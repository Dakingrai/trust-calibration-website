from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Samples, Study, TrainingStudy, db_test, Hyperparameters, SqlExplanation, Spider_db, UserTransaprency
from .forms import StudyForm
import random
from django.http import HttpResponse
import pdb
import ast
from django.contrib.auth.decorators import login_required
import copy, json
from django.utils import timezone
import random


@login_required
def home(request):
    not_responded_count = Study.objects.filter(user=request.user, viewed=False).count()
    all_count = Study.objects.filter(user=request.user).count()
    n_correct_response = Study.objects.filter(user=request.user, user_response=True, sample__correct_prediction=True, viewed=True).count() + Study.objects.filter(user=request.user, user_response=False, sample__correct_prediction=False, viewed=True).count()
    context = {
        'not_responded_count': not_responded_count, 
        'all_count': all_count, 
        "responded_count": all_count-not_responded_count,
        "n_correct_response": n_correct_response,
        }
    return render(request, 'main/home.html', context)


@login_required
def create_study(request):
    no_samples = Hyperparameters.objects.all().first().no_samples_per_user
    check_samples = Study.objects.filter(user=request.user)
    if len(check_samples) == 0:
        all_samples = Samples.objects.all()
        # random_sample = [all_samples[i] for i in sorted(random.sample(range(len(all_samples)), no_samples))] 
        random_sample = [all_samples[i] for i in sorted(random.sample(range(len(all_samples)), no_samples))] 
        random.shuffle(random_sample)
        for each in random_sample:
            StudyInstance = Study(user=request.user, sample=each)
            StudyInstance.save()
        messages.success(request, f'Your samples have been created!')
    else:
        messages.error(request, f'You already have samples!')
    return redirect(reverse('home'))


def delete_study(request):
    Study.objects.filter(user=request.user).delete()
    return redirect(reverse('home'))


def generate_report(request):
    context = {
        "test": "This is test"
    }
    return render(request, 'main/report.html', {'data': context})


def reset_study(request):
    Study.objects.filter(user=request.user).update(viewed=False)
    messages.success(request, f'Your study has been reset!')
    return redirect(reverse('home'))
                    
@login_required
def start_study(request):
    study_samples = Study.objects.filter(user=request.user, viewed=False).order_by('id').first()
    if study_samples:
        return redirect(reverse('study', kwargs={'pk': study_samples.id}))
    else:
        messages.success(request, f'You have completed the study!')
        return redirect(reverse('home'))


def convert_string_to_list_of_list(input_string):
    inner_list_strings = input_string.strip("[]").split("], [")
    list_of_lists = [list(map(str, inner_list.split(", "))) for inner_list in inner_list_strings]
    return list_of_lists


def convert_str_to_list_depth3(input_string):
    # Step 1: Parse the string to extract inner list of list strings
    inner_list_of_list_strings = input_string.strip("[]").split("], [")

    # Step 2: Convert inner list of list strings to actual lists of lists
    list_of_list_of_lists = []
    for inner_list_of_list_string in inner_list_of_list_strings:
        inner_lists = inner_list_of_list_string.split("], [")
        inner_list_of_list = []
        for inner_list in inner_lists:
            inner_list_of_list.append(list(map(str, inner_list.split(", "))))
        list_of_list_of_lists.append(inner_list_of_list)
    
    return list_of_list_of_lists


@login_required
def study(request, pk):
    study_sample = Study.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        btn_value = bool(int(request.POST.get('btn_value')))
        if btn_value:
            study_sample.user_response = True
        else:
            study_sample.user_response = False
        study_sample.viewed = True
        study_sample.save()
        return redirect(reverse('start-study'))
    # pdb.set_trace()
    # try:
    #     prev_sample = Study.objects.filter(id__lt=pk, user=request.user, viewed=True).order_by('-id').first()
    #     if prev_sample.user_response == prev_sample.sample.correct_prediction:
    #         prev_sample_correct = "Yes"
    #     else:
    #         prev_sample_correct = "No"
    #     prev_sample = "Yes"
    # except:
    #     prev_sample = "None"
    #     prev_sample_correct = "None"
    is_correct_prediction = study_sample.sample.correct_prediction
    if is_correct_prediction:
        gold_pred = 1
    else:
        gold_pred = 0
    # pdb.set_trace()
    question = study_sample.sample.question.split()
    feature_attr = ast.literal_eval(study_sample.sample.feature_attribution)
    ques_and_feat_attr = [(q, f) for q, f in zip(question, feature_attr)]
    # comp = [(db, feat, conf) for db, feat, conf in zip(comp_exp, comp_feature_attr, comp_conf)]
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
    
    sample_name = study_sample.sample.sample_name
    components = SqlExplanation.objects.filter(sample=sample_name).order_by('step')
    comp_exp = [each.explanation for each in components]
    comp_feature_attr = [ast.literal_eval(each.feature_attribution) for each in components]
    comp_conf = [each.confidence for each in components]
    comp_db_name = [each.database_name for each in components]
    comp_dbs = []
    tables = []
    component_context = []
    for idx, each in enumerate(comp_db_name):
        step_context = []
        each_db = Spider_db.objects.filter(db_name=each).first()
        # all = ast.literal_eval(each_db.all_dbs)
        # pdb.set_trace()
        table_names = each_db.table_names.split(",")
        column_names = each_db.column_names
        column_names = convert_string_to_list_of_list(column_names)
        values = each_db.db_values
        values = values.split("|")
        final_values = []
        for each in values:
            final_values.append(convert_string_to_list_of_list(each))
        # values = convert_str_to_list_depth3(values)
        # try:
        #     assert len(column_names) == len(final_values)
        # except:
        #     pdb.set_trace()
        for i, each in enumerate(table_names):
            step_context.append({'table_name': each,
                                 'columns': column_names[i],
                                 'values': final_values[i],
                                 })
        component_context.append(step_context)

    assert len(comp_exp) == len(comp_feature_attr) == len(comp_conf) == len(component_context)
    full_component_data = []
    for i, each in enumerate(comp_exp):
        ques_and_feat_attr1 = [(q, f) for q, f in zip(question, comp_feature_attr[i])]
        full_component_data.append((comp_exp[i], ques_and_feat_attr1, comp_conf[i], component_context[i]))
    # pdb.set_trace()
    # full_component_data = zip(comp_exp, comp_feature_attr, comp_conf, comp_db_name, component_context)
        # column_names = [ast.literal_eval(c) for c in column_names.split("|")]
        # each_values = ast.literal_eval(each_db.db_values)

        
    # comp_exp = ast.literal_eval(study_sample.sample.comp_explanations)
    # feature_attr = ast.literal_eval(study_sample.sample.feature_attribution)
    # comp_conf = ast.literal_eval(study_sample.sample.comp_confidence)
    # if len(comp_conf) > 1:
    #     mid_comp_conf = [max(comp_conf), min(comp_conf)]
    #     if comp_conf.index(min(comp_conf)) != comp_conf.index(max(comp_conf)):
    #         mid_comp_exp = [comp_exp[comp_conf.index(max(comp_conf))], comp_exp[comp_conf.index(min(comp_conf))]]
    #         mid_feature_attr = [feature_attr[comp_conf.index(max(comp_conf))], feature_attr[comp_conf.index(min(comp_conf))]]
    #         mid = True
    #         mid_desc = ["most", "least"]
    #     else:
    #         mid_comp_exp = [comp_exp[comp_conf.index(max(comp_conf))], comp_exp[comp_conf.index(min(comp_conf))+1]]
    #         mid_feature_attr = [feature_attr[comp_conf.index(max(comp_conf))], feature_attr[comp_conf.index(min(comp_conf))+1]]
    #         mid = True
    #         mid_desc = ["most", "least"]
    # else:
    #     mid_comp_conf = comp_conf
    #     mid_comp_exp = comp_exp
    #     mid_feature_attr = feature_attr
    #     mid = False
    #     mid_desc = []
    
    # ques_and_feat_attr_mid = [zip(question, each) for each in mid_feature_attr]
    # print(ques_and_feat_attr, comp_exp, comp_conf)
    username = request.user.username
    user_transparency = UserTransaprency.objects.filter(username = username).first()
    context = {
        'db': final_context,
        'question': study_sample.sample.question,
        'db_records': ast.literal_eval(study_sample.sample.db_records),
        'overall_conf': study_sample.sample.confidence,
        'hardness': study_sample.sample.hardness,
        'pred_sql': study_sample.sample.pred_sql,
        'ground_sql': study_sample.sample.ground_sql,
        "no_tables": len(final_context),
        "db_name": db_name,
        'ques_and_feat_attr': ques_and_feat_attr,
        'comp_feature_attr': comp_feature_attr,
        'comp_conf': comp_conf,
        'comp_exp': comp_exp,
        'full_comp_data': full_component_data,
        'transparency': user_transparency.user_transparency,
        'is_correct_prediction': gold_pred,

    }
    Study.objects.filter(id=pk, user=request.user).update(start_time= timezone.now()) # update start time

    return render(request, 'main/study.html', {'study_sample': context})


@login_required
def start_training_study(request):
    study_samples = TrainingStudy.objects.filter(user=request.user, viewed=False).order_by('id').first()
    if study_samples:
        return redirect(reverse('training-study', kwargs={'pk': study_samples.id}))
    else:
        messages.success(request, f'You have completed the Training!')
        return redirect(reverse('home'))


@login_required
def trainining_study(request, pk):
    study_sample = TrainingStudy.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        btn_value = bool(int(request.POST.get('btn_value')))
        if btn_value:
            study_sample.user_response = True
        else:
            study_sample.user_response = False
        study_sample.viewed = True
        study_sample.save()
        return redirect(reverse('start-training-study'))
    # pdb.set_trace()
    # try:
    #     prev_sample = Study.objects.filter(id__lt=pk, user=request.user, viewed=True).order_by('-id').first()
    #     if prev_sample.user_response == prev_sample.sample.correct_prediction:
    #         prev_sample_correct = "Yes"
    #     else:
    #         prev_sample_correct = "No"
    #     prev_sample = "Yes"
    # except:
    #     prev_sample = "None"
    #     prev_sample_correct = "None"
    is_correct_prediction = study_sample.sample.correct_prediction
    if is_correct_prediction:
        gold_pred = 1
    else:
        gold_pred = 0
    # pdb.set_trace()
    question = study_sample.sample.question.split()
    feature_attr = ast.literal_eval(study_sample.sample.feature_attribution)
    ques_and_feat_attr = [(q, f) for q, f in zip(question, feature_attr)]
    # comp = [(db, feat, conf) for db, feat, conf in zip(comp_exp, comp_feature_attr, comp_conf)]
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
    
    sample_name = study_sample.sample.sample_name
    components = SqlExplanation.objects.filter(sample=sample_name).order_by('step')
    comp_exp = [each.explanation for each in components]
    comp_feature_attr = [ast.literal_eval(each.feature_attribution) for each in components]
    comp_conf = [each.confidence for each in components]
    comp_db_name = [each.database_name for each in components]
    comp_dbs = []
    tables = []
    component_context = []
    for idx, each in enumerate(comp_db_name):
        step_context = []
        each_db = Spider_db.objects.filter(db_name=each).first()
        # all = ast.literal_eval(each_db.all_dbs)
        # pdb.set_trace()
        table_names = each_db.table_names.split(",")
        column_names = each_db.column_names
        column_names = convert_string_to_list_of_list(column_names)
        values = each_db.db_values
        values = values.split("|")
        final_values = []
        for each in values:
            final_values.append(convert_string_to_list_of_list(each))
        # values = convert_str_to_list_depth3(values)
        # try:
        #     assert len(column_names) == len(final_values)
        # except:
        #     pdb.set_trace()
        # pdb.set_trace()
        for i, each in enumerate(table_names):
            step_context.append({'table_name': each,
                                 'columns': column_names[i],
                                 'values': final_values[i],
                                 })
        component_context.append(step_context)

    assert len(comp_exp) == len(comp_feature_attr) == len(comp_conf) == len(component_context)
    full_component_data = []
    for i, each in enumerate(comp_exp):
        ques_and_feat_attr1 = [(q, f) for q, f in zip(question, comp_feature_attr[i])]
        full_component_data.append((comp_exp[i], ques_and_feat_attr1, comp_conf[i], component_context[i]))
    # pdb.set_trace()
    # full_component_data = zip(comp_exp, comp_feature_attr, comp_conf, comp_db_name, component_context)
        # column_names = [ast.literal_eval(c) for c in column_names.split("|")]
        # each_values = ast.literal_eval(each_db.db_values)

        
    # comp_exp = ast.literal_eval(study_sample.sample.comp_explanations)
    # feature_attr = ast.literal_eval(study_sample.sample.feature_attribution)
    # comp_conf = ast.literal_eval(study_sample.sample.comp_confidence)
    # if len(comp_conf) > 1:
    #     mid_comp_conf = [max(comp_conf), min(comp_conf)]
    #     if comp_conf.index(min(comp_conf)) != comp_conf.index(max(comp_conf)):
    #         mid_comp_exp = [comp_exp[comp_conf.index(max(comp_conf))], comp_exp[comp_conf.index(min(comp_conf))]]
    #         mid_feature_attr = [feature_attr[comp_conf.index(max(comp_conf))], feature_attr[comp_conf.index(min(comp_conf))]]
    #         mid = True
    #         mid_desc = ["most", "least"]
    #     else:
    #         mid_comp_exp = [comp_exp[comp_conf.index(max(comp_conf))], comp_exp[comp_conf.index(min(comp_conf))+1]]
    #         mid_feature_attr = [feature_attr[comp_conf.index(max(comp_conf))], feature_attr[comp_conf.index(min(comp_conf))+1]]
    #         mid = True
    #         mid_desc = ["most", "least"]
    # else:
    #     mid_comp_conf = comp_conf
    #     mid_comp_exp = comp_exp
    #     mid_feature_attr = feature_attr
    #     mid = False
    #     mid_desc = []
    
    # ques_and_feat_attr_mid = [zip(question, each) for each in mid_feature_attr]
    # print(ques_and_feat_attr, comp_exp, comp_conf)
    username = request.user.username
    user_transparency = UserTransaprency.objects.filter(username = username).first()
    context = {
        'db': final_context,
        'question': study_sample.sample.question,
        'db_records': ast.literal_eval(study_sample.sample.db_records),
        'overall_conf': study_sample.sample.confidence,
        'hardness': study_sample.sample.hardness,
        'pred_sql': study_sample.sample.pred_sql,
        'ground_sql': study_sample.sample.ground_sql,
        "no_tables": len(final_context),
        "db_name": db_name,
        'ques_and_feat_attr': ques_and_feat_attr,
        'comp_feature_attr': comp_feature_attr,
        'comp_conf': comp_conf,
        'comp_exp': comp_exp,
        'full_comp_data': full_component_data,
        'transparency': user_transparency.user_transparency,
        'is_correct_prediction': gold_pred,

    }
    # pdb.set_trace()
    TrainingStudy.objects.filter(id=pk, user=request.user).update(start_time= timezone.now()) # update start time

    return render(request, 'main/train_study.html', {'study_sample': context})


@login_required
def delete_training_samples(request):
    TrainingStudy.objects.filter(user=request.user).delete()
    return redirect(reverse('home'))


@login_required
def reset_training_study(request):
    TrainingStudy.objects.filter(user=request.user).update(viewed=False)
    messages.success(request, f'Your study has been reset!')
    return redirect(reverse('home'))


@login_required
def create_training_samples(request):
    pass

