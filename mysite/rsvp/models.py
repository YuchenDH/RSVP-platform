from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    """
    Model representing a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    nickname = models.CharField(max_length=20, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Event(models.Model):
    """
    Model representing an event
    """
    title = models.CharField(max_length=200, help_text="Enter the title of the event")
    owner = models.ManyToManyField(User)
    date_and_time = models.DateTimeField(help_text="Enter the date and time of the event")
    summary = models.TextField(help_text="(Optional) Enter the details of the event.", null=True, blank=True)
    plus = models.IntegerField(default=0, help_text="Can guests bring additonal guests?")
    
    class Meta:
        ordering = ["date_and_time", "title"]
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('event-details', args=[str(self.id)])


class Vendor(models.Model):
    """
    Intermediate model for the vendor group
    """
    people = models.ManyToManyField(User, blank=True, null=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

class Guest(models.Model):
    """
    Intermediate model for the guest group
    """
    people = models.ManyToManyField(User, blank=True, null=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

class Question(models.Model):
    """
    Model representing a survey question within an event
    """
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(help_text="Enter the question")
    final = models.IntegerField(default=0, help_text="Is the result finalized?")
    def is_final(self):
        """
        return True if the question is finalized
        """
        if (self.final-1 == 0) :
            return True
        else:
            return False

    def __str__(self):
        """
        String for representing the Model object
        """
        return self.description

class Option(models.Model):
    """
    Model representing a option for a survey question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(help_text="Enter the option")
    count = models.IntegerField(default=0)

    def __str__(self):
        """
        String for representing the Model object
        """
        return self.description
