from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class SysterUser(models.Model):
	"""Profile model to store additional information about a user
	"""
	user = models.OneToOneField(User)
	country = CountryField(blank=True, null=True)
	BlogURL = models.URLField(max_length=255, blank=True, null=True)
	HomepageURL = models.URLField(max_length=255, blank=True, null=True)
	Profilepicture = models.ImageField(upload_to='photos/', default='photos/dummy.png',blank=True, null=True)
	def __unicode__(self):
		firstname = self.user.first_name
		lastname = self.user.last_name
		if firstname and lastname:
			return "{0} {1}".format(self.user.first_name, self.user.last_name)
		else:
			return self.user.username

class Community(models.Model):
	"""Model to represent a Syster Community
	"""
	name = models.CharField(max_length=255, blank=False, null=False)
	email = models.EmailField(max_length=255, blank=False, null=False)
	mailing_list = models.EmailField(max_length=255, blank=True, null=True)
	resource_area = models.URLField(max_length=255, blank=True, null=True)
	members = models.ManyToManyField(SysterUser,blank=True,null=True)
	admin = models.ForeignKey(User) 
	website = models.URLField(max_length=255, blank=True, null=True)
	facebook = models.URLField(max_length=255, blank=True, null=True)
	googleplus = models.URLField(max_length=255, blank=True, null=True)
	twitter = models.URLField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.name

class News(models.Model):
	title=models.CharField(max_length=255,blank=False,null=True)
	community = models.ForeignKey(Community)
	author=models.ForeignKey(SysterUser)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	date_modified = models.DateField(auto_now=True, auto_now_add=False)
	is_public = models.BooleanField(default=True)
	contents = models.TextField()
	def __unicode__(self):
		return "{0} of {0} Community".format(self.title, self.community.name)
class FAQ(models.Model):
	title=models.CharField(max_length=255,blank=False,null=True)
	community = models.ForeignKey(Community)
	author=models.ForeignKey(SysterUser)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	date_modified = models.DateField(auto_now=True, auto_now_add=False)
	contents = models.TextField()
	def __unicode__(self):
		return "{0} of {0} Community".format(self.title, self.community.name)
class Resource(models.Model):
	RESOURCE_TYPES = ( 
	       ('scholarship', 'Scholarship'),
	       ('grant', 'Grant'),
	       ('internship', 'Internship'),
	       ('workshop', 'Workshop'),
	       ('development', 'Professional Development'),
	      )   
	title = models.CharField(max_length=255, blank=False, null=False)
	community = models.ForeignKey(Community)
	author = models.ForeignKey(User)
	date_created = models.DateField(auto_now=False, auto_now_add=True)
	date_modified = models.DateField(auto_now=True, auto_now_add=False)
	is_public = models.BooleanField(default=True)
	contents = models.TextField()
	resource_type =  models.CharField(max_length=30, choices=RESOURCE_TYPES)
