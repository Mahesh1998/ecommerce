from django.db import models

class ProductManager(models.Manager):
    def create_product(self, name, description, manufacturer_name, inventory_count):
        product = self.create(name=name, description=description, manufacturer_name=manufacturer_name, inventory_count=inventory_count)
        return product

    def get_product(self, product_id):
        return self.get(pk=product_id)

    def update_product(self, product_id, **kwargs):
        product = self.get(pk=product_id)
        for field, value in kwargs.items():
            setattr(product, field, value)
        product.save()
        return product

    def delete_product(self, product_id):
        product = self.get(pk=product_id)
        product.delete()

class UserManager(models.Manager):
    def create_user(self, user_name, user_password, user_preferences):
        user = self.create(user_name=user_name, user_password=user_password, user_preferences=user_preferences)
        return user

    def get_user(self, user_id):
        return self.get(pk=user_id)

    def update_user(self, user_id, **kwargs):
        user = self.get(pk=user_id)
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
        return user

    def delete_user(self, user_id):
        user = self.get(pk=user_id)
        user.delete()



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer_name = models.CharField(max_length=100)
    inventory_count = models.IntegerField(default=0)

    objects = ProductManager()

class ProductsBoughtManager(models.Manager):
    def create_products_bought(self, user, product, user_name, product_name, quantity, date_of_purchase):
        products_bought = self.create(user=user, product=product, user_name=user_name,
                                      product_name=product_name, quantity=quantity, date_of_purchase=date_of_purchase)
        return products_bought

    def get_products_bought(self, id):
        return self.get(pk=id)

    def update_products_bought(self, id, **kwargs):
        products_bought = self.get(pk=id)
        for field, value in kwargs.items():
            setattr(products_bought, field, value)
        products_bought.save()
        return products_bought

    def delete_products_bought(self, id):
        products_bought = self.get(pk=id)
        products_bought.delete()


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)  # Password should be encrypted in real-world applications
    user_preferences = models.CharField(max_length=20)

    objects = UserManager()


class ProductsBought(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date_of_purchase = models.DateField()

    objects = ProductsBoughtManager()
