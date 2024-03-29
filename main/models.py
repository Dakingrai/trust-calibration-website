from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

import random

TRUST_LEVEL = (
    (0, 'Low'),
    (1, 'Mid'),
    (2, 'High'),
  )

@receiver(post_save, sender=User)
def after_user_created(sender, instance, created, **kwargs):
    if created:
        # Your additional actions here
        # For example, you can create a related profile, send a welcome email, etc.
        print("Let's goooo!!!")
        
        # Create training samples for created users
        all_samples = TrainingSamples.objects.all()
        random_sample = [all_samples[i] for i in sorted(range(len(all_samples)))]
        random.shuffle(random_sample)
        for each in random_sample:
            StudyInstance = TrainingStudy(user=instance, sample=each)
            StudyInstance.save()
        
        # Create study samples for created users
        all_samples = Samples.objects.all()
        no_samples = Hyperparameters.objects.all().first().no_samples_per_user
        random_sample = [all_samples[i] for i in sorted(random.sample(range(len(all_samples)), no_samples))] 
        random.shuffle(random_sample)
        for each in random_sample:
            StudyInstance = Study(user=instance, sample=each)
            StudyInstance.save()

        # Assign transparency level for created users
        UserTransaprencyInstance = UserTransaprency()
        UserTransaprencyInstance.username = instance.username
        UserTransaprencyInstance.user_transparency = "High"
        UserTransaprencyInstance.save()
        

class Hyperparameters(models.Model):
    no_samples_per_user = models.IntegerField()
    agreement_text = models.TextField(blank=True, null=True)


class Spider_db(models.Model):
    db_name = models.CharField(max_length=100)
    table_names = models.TextField()
    column_names = models.TextField()
    db_values = models.TextField()
    all_dbs = models.TextField()

    def __str__(self):
        return self.db_name


class db_test(models.Model):
    all_db = models.TextField()


class Samples(models.Model):
    sample_name = models.CharField(max_length=100)
    question = models.CharField(max_length=256)
    ground_sql = models.CharField(max_length=256, null=True, blank=True)
    pred_sql = models.CharField(max_length=256, null=True, blank=True)
    hardness = models.CharField(max_length=9)
    db_records = models.TextField(null=True, blank=True)
    feature_attribution = models.TextField()
    confidence = models.FloatField()
    correct_prediction = models.BooleanField()
    database_name = models.CharField(max_length=100)

    def __str__(self):
        return self.question
    
class TrainingSamples(models.Model):
    sample_name = models.CharField(max_length=100)
    question = models.CharField(max_length=256)
    ground_sql = models.CharField(max_length=256, null=True, blank=True)
    pred_sql = models.CharField(max_length=256, null=True, blank=True)
    hardness = models.CharField(max_length=9)
    db_records = models.TextField(null=True, blank=True)
    feature_attribution = models.TextField()
    confidence = models.FloatField()
    correct_prediction = models.BooleanField()
    database_name = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class Study(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Samples, on_delete=models.CASCADE)
    user_response = models.BooleanField(blank=True, null=True)
    viewed = models.BooleanField(default=False) # flag to check if user has viewed the sample
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.sample.question
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(Study, self).save(*args, **kwargs)

class FormAfterStudy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_response = models.TextField(blank=False, null=False)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(FormAfterStudy, self).save(*args, **kwargs)

class TrainingStudy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(TrainingSamples, on_delete=models.CASCADE)
    user_response = models.BooleanField(blank=True, null=True)
    viewed = models.BooleanField(default=False) # flag to check if user has viewed the sample
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.sample.question
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(TrainingStudy, self).save(*args, **kwargs)

class SqlExplanation(models.Model):
    sample = models.CharField(max_length=100)
    step = models.IntegerField()
    explanation = models.TextField()
    feature_attribution = models.TextField()
    confidence = models.FloatField()
    database_name = models.CharField(max_length=100)

    def __str__(self):
        return self.database_name
    

class UserTransaprency(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    user_transparency = models.CharField(max_length=100, default="Low")


class UserAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_agreement_status = models.BooleanField(default=False)
    user_agreement_time = models.DateTimeField(blank=True, null=True)
    user_agreement = models.TextField(blank=True, null=True)


class UserTrust(models.Model):
    TRUST_LEVEL = (
        (1, 'Strongly disagree'),
        (2, 'Somewhat disagree'),
        (3, 'Neither agree or disagree'),
        (4, 'Somewhat agree'),
        (5, 'Strongly agree'),
      )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trust_until_no_reason = models.IntegerField(choices=TRUST_LEVEL, default=3)
    most_part_i_distrust = models.IntegerField(choices=TRUST_LEVEL, default=3)
    rely_on_machine_assist = models.IntegerField(choices=TRUST_LEVEL, default=3)
    tendency_to_trust = models.IntegerField(choices=TRUST_LEVEL, default=3)
    easy_for_me_to_trust = models.IntegerField(choices=TRUST_LEVEL, default=3)
    likely_to_trust = models.IntegerField(choices=TRUST_LEVEL, default=3)
    user_trust_status = models.BooleanField(default=False)
    before_study = models.BooleanField(default=True)


class UserDemographic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    race = models.CharField(max_length=100, blank=True, null=True)

class UserTrainingMeta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_one = models.BooleanField(default=False)
    task_two = models.BooleanField(default=False)
    question = models.BooleanField(default=False)
    feedback = models.BooleanField(default=False)
    database = models.BooleanField(default=False)
    model_explanation = models.BooleanField(default=False)
    explanation_density = models.BooleanField(default=False)
    general_task = models.BooleanField(default=False)
    begin_train = models.BooleanField(default=False)
    begin_study = models.BooleanField(default=False)

class JianTrustScale(models.Model):
    JIAN_LEVEL = (
        (1, 'one'),
        (2, 'two'),
        (3, 'three'),
        (4, 'four'),
        (5, 'five'),
        (6, 'six'),
        (7, 'seven'),
      )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sytem_deceptive = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_underhanded = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_sus_intent = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_wary_system = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_action_harmful = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_confident = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_security = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_integrity = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_dependable = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_reliable = models.IntegerField(choices=JIAN_LEVEL, default=1)
    systen_trust = models.IntegerField(choices=JIAN_LEVEL, default=1)
    system_familiar = models.IntegerField(choices=JIAN_LEVEL, default=1)
    initial_survey = models.BooleanField(default=True)
    before_study = models.BooleanField(default=True)




