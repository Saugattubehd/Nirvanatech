from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import shortuuid



STATUS = ( 
    ('Published', 'Published'),
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled'),
)
class Category(models.Model):
    title   = models.CharField(max_length=255)
    image  = models.FileField(upload_to='image', blank=True, null=True)
    slug   = models.SlugField(max_length=255, unique=True, blank=True)



    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']



class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='image', blank=True, null=True,default='product.jpg')
    description = CKEditor5Field('Text', config_name='extends')
    model_num=models.CharField(max_length=100,null=True,blank=True)           
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, )
    status = models.CharField(max_length=50, choices=STATUS, default='Published')
    featured = models.BooleanField(default=False,verbose_name=' MarketPlace Featured ')
    stock = models.PositiveIntegerField(default=0, null=True, blank=True, )
    sku = ShortUUIDField(
        length=5,
        max_length=50,
        alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        prefix='SKU',
    )
    slug = models.SlugField(null=True,  blank=True)


    date  = models.DateTimeField(default=timezone.now, ) #verbose_name='Date Created'



    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Products'


    def __str__(self):
        return self.name  
    
    
    def save( self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)+"-"+str(shortuuid.uuid().lower()[:2])
        super(Product, self).save(*args, **kwargs)

class Department(models.Model):
    name = models.CharField(max_length=100)  # Technical, Leadership, Sales
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.FileField(upload_to='team/', blank=True, null=True,default='team/default-avatar.png')
    email = models.EmailField(blank=True)
    number = models.IntegerField(blank=True,null=True)
    order = models.IntegerField(default=0)  # For controlling display order
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural="teammembers"
        
    def __str__(self):
        return f"{self.name} - {self.position}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} from {self.company}"
    

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)  # For controlling slider order
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        
    def __str__(self):
        return self.title
    

# Add after Product model
class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    name = models.CharField(max_length=100)    # e.g., "Storage", "Power Supply"
    value = models.CharField(max_length=255)   # e.g., "128GB", "AC 110V~240V"

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Specifications'

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='features'
    )
    title = models.CharField(max_length=100)   # e.g., "AI Detection"
    description = models.TextField()           # Feature description
    is_highlighted = models.BooleanField(default=False)  # For key features

    class Meta:
        ordering = ['-is_highlighted', 'title']
        verbose_name_plural = 'Features'

    def __str__(self):
        return f"{self.product.name} - {self.title}"

class ProductSupport(models.Model):
    DOCUMENT_TYPES = (
        ('manual', 'User Manual'),
        ('datasheet', 'Technical Datasheet'),
        ('guide', 'Installation Guide'),
        ('warranty', 'Warranty Information'),
    )

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='support_docs'
    )
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='product_support/', blank=True)
    url = models.URLField(blank=True)  # For external documents

    class Meta:
        ordering = ['doc_type', 'title']
        verbose_name_plural = 'Support Documents'

    def __str__(self):
        return f"{self.product.name} - {self.get_doc_type_display()}"