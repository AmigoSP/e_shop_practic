from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя категории')
    slug_url = models.SlugField(max_length=20, unique=True, null=True)

    def __str__(self):
        return str(self.name)


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя подкатегории')
    slug_url = models.SlugField(max_length=20, unique=True, null=True)

    def __str__(self):
        return str(self.name)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Производитель')
    slug_url = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='Название продукта')
    descriptions = models.TextField(verbose_name='Описание')
    product_image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    slug_url = models.SlugField(max_length=20, unique=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, verbose_name='Категория продукта',
                                 on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, verbose_name='Подкатегория продукта',
                                    on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель продукта',
                                     on_delete=models.CASCADE)

    def __iter__(self):
        foreign_fields = {
            'category': self.category.name,
            'subcategory': self.subcategory.name,
            'manufacturer': self.manufacturer.name
        }
        for field in self._meta.fields:
            foreign_field_name = foreign_fields.get(field.name)
            if foreign_field_name:
                yield field.name, foreign_field_name
            elif field.name not in ('id', 'slug_url', 'date_create', 'date_update'):
                yield field.name, field.value_to_string(self)

    class Meta:
        abstract = True


class Smartphone(Product):
    processor = models.CharField(max_length=150, verbose_name='Марка процессора')
    ram_value = models.IntegerField(verbose_name='Объем оперативной памяти')
    memory_value = models.IntegerField(verbose_name='Объем встроенной памяти')
    resolution_screen = models.CharField(max_length=150, verbose_name='Разрешение экрана')
    battery_capacity = models.IntegerField(verbose_name='Емкость аккумулятора')
    nfc = models.BooleanField(verbose_name='NFC')
    os_system = models.CharField(max_length=150, verbose_name='Операционная система')

    def __str__(self):
        return str(self.product_name)


class NoteBook(Product):
    processor = models.CharField(max_length=150, verbose_name='Марка процессора')
    ram_value = models.IntegerField(verbose_name='Объем оперативной памяти')
    memory_value = models.IntegerField(verbose_name='Объем встроенной памяти')
    resolution_screen = models.CharField(max_length=150, verbose_name='Разрешение экрана')
    battery_capacity = models.IntegerField(verbose_name='Емкость аккумулятора')
    video_card = models.CharField(max_length=150, verbose_name='Видеокарта', blank=True)
    os_system = models.CharField(max_length=150, verbose_name='Операционная система', blank=True)

    def __str__(self):
        return str(self.product_name)


class VideoCard(Product):
    processor = models.CharField(max_length=150, verbose_name='Марка процессора')
    memory_value = models.IntegerField(verbose_name='Объем встроенной памяти')
    connectors = models.CharField(max_length=255, verbose_name='Разъемы подключения')
    connectors_number = models.IntegerField(verbose_name='Кол-во подключаемых мониторов')

    def __str__(self):
        return str(self.product_name)


class HddDisk(Product):
    interface = models.CharField(max_length=150, verbose_name='Интерфейс')
    memory_value = models.IntegerField(verbose_name='Объем памяти')
    units_of_measurement = models.CharField(max_length=255, verbose_name='Единицы измерения')
    product_type = models.CharField(max_length=150, verbose_name='HDD/SSD/M2')

    def __str__(self):
        return str(self.product_name)
