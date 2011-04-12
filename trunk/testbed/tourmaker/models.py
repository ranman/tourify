from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Overlay(models.Model): 
  lat = models.FloatField()
  lng = models.FloatField()
  uri = models.URLField()
  name = models.TextField()
  content = models.TextField()

class Placemark(models.Model):
  lat = models.FloatField()
  lng = models.FloatField()
  content = models.TextField()

class Audio(models.Model):
  uri = models.URLField();

class Camera(models.Model):
  lat = models.FloatField()
  lng = models.FloatField()
  alt = models.FloatField()

class TimelineItem(models.Model):
  begin = models.TimeField()
  end = models.TimeField()
  item_type = models.ForeignKey(ContentType) 
  item_id = models.PositiveIntegerField() 
  item = generic.GenericForeignKey('item_type', 'item_id') 
