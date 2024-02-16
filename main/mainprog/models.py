from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    # Категория товаров

    name = models.CharField("Имя", max_length=150)
    descriptions = models.TextField('Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"


class Brand(models.Model):
    name = models.CharField("Имя", max_length=150)
    descriptions = models.TextField("Описание")
    image = models.ImageField("Изоброжение", upload_to='brands/')
    url = models.SlugField(max_length=150, unique=True)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name='brands')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"

    def get_absolute_url(self):
        return reverse("view_prod", kwargs={"slug": self.url})


class TypeOfProduct(models.Model):
    # тип продукта

    name = models.CharField("Имя", max_length=150)
    descriptions = models.TextField("Описание")
    image = models.ImageField("Изображения", upload_to='type/')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип продукта"
        verbose_name_plural = "Тип продукта"


class Product(models.Model):
    title = models.CharField("Заголовок", max_length=150)
    descriptions = models.TextField("Описание")
    poster = models.ImageField("Изоброжение", upload_to='products/')
    poster1 = models.ImageField("Изоброжение", upload_to='products/')
    poster2 = models.ImageField("Изоброжение", upload_to='products/')

    brand = models.ManyToManyField(Brand, verbose_name='Бренды', related_name='product_brand')
    typeofproduct = models.ManyToManyField(TypeOfProduct, verbose_name="тип продукта")
    price = models.PositiveIntegerField("Цена", default=500, help_text="Укажите сумму в тенге")

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    storage = models.IntegerField("Память", default=64)

    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse("buy", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title)

            counter = 1
            while Product.objects.filter(url=self.url).exists():
                self.url = f"{slugify(self.title)}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


class ProductShots(models.Model):
    title = models.CharField("Заголовок", max_length=150)
    descriptions = models.TextField("Описание")
    image = models.ImageField("Изоброжнения", upload_to='product_shots')
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товара"


class Reviews(models.Model):
    name = models.CharField("Имя", max_length=150)
    email = models.EmailField()
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )

    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.product}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
