from django.db import models

import datetime

"""
This model is used to uniquely identify a equipment
with its name, id etc. It saves the info about the 
equipment 
"""
class FoodItem(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    recipe_id = models.IntegerField(default=1)
    expiryDate = models.DateField(default=datetime.datetime.today)
    #,input_formats=['%m-%m-%Y']
    recipe_name = models.CharField(max_length=255, default=None, blank=True, null=True)

    @staticmethod
    def fetch_items(id_list):
        return FoodItem.objects.filter(id__in=id_list)

    @staticmethod
    def fetch_expired_items():
        return FoodItem.objects.filter(expiryDate__lte = datetime.datetime.today)

    @staticmethod
    def fetch_unexpired_items():
        return FoodItem.objects.filter(expiryDate__gte=datetime.datetime.today)

    @staticmethod
    def fetch_items_by_type(type):
        if type is not None:
            return FoodItem.objects.filter(type=type)
        else:
            return FoodItem.objects.all()

class Recipe(models.Model):
    recipe_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    image = models.CharField(max_length=255)


"""
This model is used to save the User details  
done by the customer
"""
class Users(models.Model):
    user_id = models.IntegerField(default=1)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

