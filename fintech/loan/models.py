from django.db import models
from django.contrib.auth.models import User
# Create your models here.
LOAN_STATUS=((1, "approved"),(2,"discard"),(3, "pending"),)
LOAN_TYPE=((1, "Personal Loan"),(2, "Home Loan"),(3, "Car Laon"),(4, "Top Up Loan"),(5, "Construction Loan"))
ACCOUNT_TYPE=((1, "Personal Account"),(2, "Current Account"),(3, "Saving Account"))
ACCOUNT_STATUS=((1, "pending"),(2, "inactive"),(3, "active"))
class clientInformation(models.Model):
    user = models.OneToOneField(User)
    dateOfBirth = models.DateField()
    mobileNumber = models.CharField(max_length=10)
    relationshipWithBank = models.IntegerField(choices=((1, "Personal Account"),
                                        (2,"Current Account"),
                                        (3,"Saving Account"),
                                        (4, "Fresh Account")),
                                default=4)
    homeAddress= models.CharField(max_length=255)
    workAddress= models.CharField(max_length=255)

class BankAccount(models.Model):
    client = models.ForeignKey(clientInformation)
    status = models.IntegerField(choices=ACCOUNT_STATUS, default=2)
    type = models.IntegerField(choices=ACCOUNT_TYPE,default=1)

class Loan(models.Model):
    client = models.ForeignKey(clientInformation)
    bankAccount = models.ForeignKey(BankAccount, blank=True, null=True)
    applyAmount = models.IntegerField(default=0)
    approvedAmount = models.IntegerField(default=0)
    status = models.IntegerField(choices=LOAN_STATUS,default=3)
    comment = models.CharField(max_length=255)
    loanType = models.IntegerField(choices=LOAN_TYPE,blank=True, null=True)
    approveBy = models.ForeignKey(User,blank=True, null=True)
    validTill = models.DateField()

