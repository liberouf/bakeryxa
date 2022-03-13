from itertools import product
from typing import cast
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from accounts.models import Account
from django.utils.text import slugify   
from django.db.models import Avg, Count
from django.urls import reverse




class ghanadimanager(BaseUserManager):
    def create_user(self, owner, name, username , password , images):
        
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            owner = owner ,
            username = username,
            name = name,
            email = owner.email,
            password = password, 
            images=images,
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, owner, name, email, username, password):
        user = self.create_user(
            owner = owner ,
            username = username,
            name = name,
            email = email,
            password = password, 
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user




class ghanadi(AbstractBaseUser):
   # ownerlist = Account.objects.filter(is_owner=True)
    owner            = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    email            = models.EmailField(max_length=100, unique=True)
    name             = models.CharField(max_length=50)
    phone            = models.CharField(max_length=50)
    address          = models.TextField(max_length=500)
    username         = models.CharField(max_length=50, unique=True)
    slug             = models.SlugField(max_length=200 ,default=username)
    date_joined      = models.DateTimeField(auto_now_add=True)
    password         = models.CharField(max_length=150,default=None) 
    position         = models.PointField(null=True, blank=True)
    
    images           = models.ImageField(upload_to='images/', null=True, blank=True)
    is_active        = models.BooleanField(default=True)     
    date_joined      = models.DateTimeField(auto_now_add=True)
    last_login       = models.DateTimeField(auto_now_add=True)
    is_admin         = models.BooleanField(default=False)
    is_staff         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin    = models.BooleanField(default=False)
    is_superadmin    = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
  
    objects = ghanadimanager()

    #def get_url(self):
        #return reverse('ghanadi_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def imagesurl(self):
        try:
            url=self.images.url
        except:
            url=''
        return url

    def slugify(self):
            self.slug = slugify(self.user.username)

        ###############################                ################################

class mahsool(models.Model):  
    ghanadish       = models.ForeignKey(ghanadi,on_delete=CASCADE,null=True,blank=True) 
    name            = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    #category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('mahsool-detail', args=[self.id])

    def __str__(self):
        return self.name

    def slugify(self):
        self.slug = slugify("{obj.product_name}-{obj.id}".format(obj=self))

    def imagesurl(self):
        try:
            url=self.images.url
        except:
            url=''
        return url
        
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count



class ReviewRating(models.Model):
        product = models.ForeignKey(mahsool, on_delete=models.CASCADE)
        user = models.ForeignKey(Account, on_delete=models.CASCADE)
        subject = models.CharField(max_length=100, blank=True)
        review = models.TextField(max_length=500, blank=True)
        rating = models.FloatField()
        ip = models.CharField(max_length=20, blank=True)
        status = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.subject