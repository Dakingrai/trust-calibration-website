from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TRUST_LEVEL = (
    (0, 'Low'),
    (1, 'Mid'),
    (2, 'High'),
  )


class Hyperparameters(models.Model):
    no_samples_per_user = models.IntegerField()


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

