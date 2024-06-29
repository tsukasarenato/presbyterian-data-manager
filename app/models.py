import os
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify


def church_image_path(instance, filename):
    
    # Slugify the name to make it URL safe
    name_slug = slugify(instance.name)

    # Extract the file extension
    extension = filename.split('.')[-1]

    # Construct the new filename with church id and name
    new_filename = f'{name_slug}.{extension}'

    # Return the complete path for the new filename
    return os.path.join('churches', new_filename)

def person_image_path(instance, filename):
    
    # Slugify the name to make it URL safe
    name_slug = slugify(instance.name)

    # Extract the file extension
    extension = filename.split('.')[-1]

    # Construct the new filename with church id and name
    new_filename = f'{instance.church.id}_{name_slug}.{extension}'

    # Return the complete path for the new filename
    return os.path.join('people', new_filename)

def ministry_image_path(instance, filename):
    
    # Slugify the name to make it URL safe
    name_slug = slugify(instance.name)

    # Extract the file extension
    extension = filename.split('.')[-1]

    # Construct the new filename with church id and name
    new_filename = f'{instance.church.id}_{name_slug}.{extension}'

    # Return the complete path for the new filename
    return os.path.join('ministries', new_filename)



class Churches(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    acronym = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to=church_image_path, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class People(models.Model):
    EXCOMMUNICATED = 0
    MEMBER = 1
    PASTOR = 2
    ELDER = 3
    DEACON = 4
    VISITOR = 5
    DISCIPLESHIP = 6
    STATUS_CHOICES = [
        (EXCOMMUNICATED, 'Excommunicated'),
        (MEMBER, 'Member'),
        (PASTOR, 'Pastor'),
        (ELDER, 'Elder'),
        (DEACON, 'Deacon'),
        (VISITOR, 'Visitor'),
        (DISCIPLESHIP, 'Discipleship'),
    ]
    
    church = models.ForeignKey(Churches, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    abbreviated_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_member = models.BooleanField(default=False)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=VISITOR
    )
    image = models.ImageField(upload_to=person_image_path, blank=True, null=True)


    def __str__(self):
        return self.name

class Ministries(models.Model):
    church = models.ForeignKey(Churches, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    acronym = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to=ministry_image_path, blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['church', 'name'], name='unique_ministry_church')
        ]

    def __str__(self):
        return self.name

class Positions(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    ministry = models.ForeignKey(Ministries, on_delete=models.CASCADE)
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['ministry', 'person'], name='unique_ministry_person')
        ]

    def __str__(self):
        return f'{self.person} - {self.ministry} - {self.position}'
