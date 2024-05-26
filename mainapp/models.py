from django.db import models
# Create your models here.

class User(models.Model):
    user_id=models.CharField(max_length=10 , unique=True , primary_key=True)
    uName=models.CharField(max_length=40)
    pword=models.CharField(max_length=20)
    uType=models.IntegerField(default=4)
    """
        1 - Head Librarian
        2 - Librarian
        4 - VIP User
        3 - Normal User
    """
    status=models.IntegerField(default=2)
    """
    1 - Active
    2 - Inactive
    """

class Book(models.Model):
    book_id=models.IntegerField(default=0 , primary_key=True)
    bName=models.CharField(max_length=50)
    publisher=models.CharField(max_length=30)
    author=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    edition=models.IntegerField()
    count=models.IntegerField()
    class Meta:
        constraints=[
            models.CheckConstraint(
                name="qty_check",
                check=models.Q(count__gte=0),
            )
        ]


class Transaction(models.Model):
    trans_id=models.IntegerField(auto_created=True , primary_key=True)
    user_id=models.ForeignKey(User , on_delete=models.DO_NOTHING)
    book_id=models.ForeignKey(Book , on_delete=models.DO_NOTHING)
    issueDtTm=models.DateTimeField()
    returnDtTm=models.DateTimeField(null=True , blank=True)

class IssuedBook(models.Model):
    trans_id=models.ForeignKey(Transaction , on_delete=models.DO_NOTHING)
    user_id=models.ForeignKey(User , on_delete=models.DO_NOTHING , blank=True , null=True)



