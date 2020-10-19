from django.db import models

# Create your models here.

class blogpost(models.Model):
    blogpost_id = models.AutoField(primary_key = True)
    head0 =models.CharField(max_length= 50,default = "")
    head1 =models.CharField(max_length= 50,default = "")
    head2 =models.CharField(max_length= 50,default="")
    chead0 = models.CharField(max_length=5000,default="")
    chead1 = models.CharField(max_length=5000,default="")
    chead2 = models.CharField(max_length=5000,default="")
    title = models.CharField(max_length=50,default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to = 'blog/images',default = "")

    def __str__(self):
        return self.title
