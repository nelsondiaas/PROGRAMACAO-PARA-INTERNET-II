from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Address(models.Model):
    street = models.CharField(max_length=200)
    suite = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return "street: {}, suite: {}, city: {}, zipcode: {}".format(
        self.street,self.suite, self.city, self.city, self.zipcode)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return "{}".format(self.name)
    

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    cpf = models.CharField(max_length=11)
    salary = models.FloatField()


class Employee(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    cpf = models.CharField(max_length=11)
    salary = models.FloatField()
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='employees')


class Status(models.Model):
    message = models.CharField(max_length=255)


class Sale(models.Model):
    total = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sales")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()


class Genre(models.Model):
    description = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=60)
    prince = models.FloatField()


class Write(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="writes")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Itemsale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="itemsales")
    amount = models.IntegerField()
    subtotal = models.FloatField()
