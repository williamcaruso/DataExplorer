from __future__ import unicode_literals

from django.db import models

# Create your models here.


HAND_CHOICES = (
    ('L', 'Left'),
    ('R', 'Right'),
    ('A', 'Ambidextrous')
)


class Graphs(models.Model):
    eda = models.TextField(null=True)
    acc_raw = models.TextField(null=True)
    acc = models.TextField(null=True)
    bvp = models.TextField(null=True)
    hr = models.TextField(null=True)
    temp = models.TextField(null=True)
    breathing = models.TextField(null=True)


# class Regression(models.Model):
#     eda_pre_shot =


class Participants(models.Model):

    name = models.CharField(max_length=120, null=True)
    dominant_hand = models.CharField(choices=HAND_CHOICES, max_length=10, null=True)
    shooter_id = models.CharField(max_length=120, null=True)
    has_left_data = models.BooleanField(default=True)
    has_right_data = models.BooleanField(default=True)
    has_bioharness_data = models.BooleanField(default=True)

    graphs = models.OneToOneField(Graphs, on_delete=models.CASCADE)
