from django.db import models

# Create your models here.
# bricksmasher_app/models.py
#from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    
#added later
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            }
#added later
    
class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    in_stock = models.PositiveIntegerField()
    checked_out = models.PositiveIntegerField()
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "in_stock": self.in_stock,
            "checked_out": self.checked_out,
        }

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'movie': self.movie.to_dict(),
        }
