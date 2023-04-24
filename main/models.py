from django.db import models
from django.contrib.auth.models import User

TRUST_LEVEL = (
    (0, 'Low'),
    (1, 'Mid'),
    (2, 'High'),
  )

class Hyperparameters(models.Model):
    no_samples_per_user = models.IntegerField()

class Spider_db(models.Model):
    db_name = models.CharField(max_length=100)
    db_schema = models.TextField()
    db_values = models.TextField()

    def __str__(self):
        return self.db_name

class db_test(models.Model):
    all_db = models.TextField()

class Samples(models.Model):
    question = models.CharField(max_length=256)
    ground_editsql = models.CharField(max_length=256)
    pred_editsql = models.CharField(max_length=256)
    ground_sql = models.CharField(max_length=256, null=True, blank=True)
    pred_sql = models.CharField(max_length=256, null=True, blank=True)
    hardness = models.CharField(max_length=9)
    db_records = models.TextField(null=True, blank=True)
    components = models.TextField()
    comp_explanations = models.TextField()
    feature_attribution = models.TextField()
    confidence = models.FloatField()
    comp_confidence = models.CharField(max_length=100)
    correct_prediction = models.BooleanField()
    database_name = models.CharField(max_length=100)

    def __str__(self):
        return self.question

class Study(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Samples, on_delete=models.CASCADE)
    user_response = models.BooleanField(blank=True, null=True)
    viewed = models.BooleanField(default=False) # flag to check if user has viewed the sample
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
