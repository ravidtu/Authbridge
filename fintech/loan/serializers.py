from .models import clientInformation,Loan,BankAccount,LOAN_STATUS,LOAN_TYPE,ACCOUNT_TYPE,ACCOUNT_STATUS
from django.contrib.auth.models import User
from rest_framework import serializers

class LoanApprovalSerializer(serializers.Serializer):
    loan_account=serializers.IntegerField()
    approved_loan_amount =serializers.IntegerField()
    loan_verify_check = serializers.BooleanField()
    loan_approve_by = serializers.EmailField()
    loan_approve_comment = serializers.CharField()

    def create(self, validated_data):
        import pdb;pdb.set_trace()
        loanObj = Loan.objects.filter(id=validated_data.get('loan_account'))
        if loanObj:
            #check account
            if loanObj[0].bankAccount.status is 1 or loanObj[0].bankAccount.status is 2:
                loanObj[0].bankAccount.status=3
                loanObj[0].bankAccount.save()

            approvUserObj=User.objects.filter(email=validated_data.get('loan_approve_by'),is_superuser=1)
            if approvUserObj:
                loanObj[0].approvedAmount=validated_data.get('approved_loan_amount')
                if validated_data.get('loan_verify_check'):
                    loanObj[0].status=1
                else:
                    loanObj[0].status = 2
                loanObj[0].comment=validated_data.get('loan_approve_comment')
                loanObj[0].approveBy=approvUserObj[0]
                loanObj[0].save()
                return "Loan has been approved"
            else:
                return "loan_approve_by  is not authorize for loan approval "
        else:
            return "Loan Account not found in our database"


class LoanSerializer(serializers.ModelSerializer):
    loan_account = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    loanType = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    def get_loan_account(self,object):
        return object.id

    def get_account(self,object):
        account=dict()
        account["account_number"]=object.bankAccount.id

        for at in ACCOUNT_TYPE:
            if at[0] == object.bankAccount.type:
                account["account_type"]=at[1]

        for at in ACCOUNT_STATUS:
            if at[0] == object.bankAccount.status:
                account["account_status"]=at[1]
        return account

    def get_client(self,object):
        client=dict()
        client['name']=object.client.user.first_name
        client['email']=object.client.user.email
        client['date_of_birth'] =object.client.dateOfBirth
        return client

    def get_loanType(self,object):
        for lt in LOAN_TYPE:
            if lt[0] == object.loanType:
                return lt[1]

    def get_status(self,object):
        for st in LOAN_STATUS:
            if st[0]==object.status:
                return st[1]

    class Meta:
        model = Loan
        fields = ("loan_account","applyAmount","status","loanType","approvedAmount","client","account","validTill")


class LoanProcessSerializer(serializers.ModelSerializer):

    dateOfBirth = serializers.DateField()
    mobileNumber = serializers.CharField()
    homeAddress = serializers.CharField()
    workAddress = serializers.CharField()
    relationshipWithBank = serializers.IntegerField()
    applyAmount = serializers.IntegerField()
    loanType = serializers.IntegerField()
    validiity = serializers.DateField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'dateOfBirth', 'mobileNumber','homeAddress','workAddress','relationshipWithBank','applyAmount','loanType','validiity')


    def create(self, validated_data):
        #check user is alredy exist and account exist or not
        userEmail=validated_data.get('email')
        userObj=User.objects.filter(email=userEmail)
        if userObj:  #user already exist ,update user info
            userObj=userObj[0]
            userObj.first_name=validated_data.get('first_name')
            userObj.last_name=validated_data.get('last_name')
            userObj.save()
            clientInfoObj = clientInformation.objects.filter(user=userObj)
            if clientInfoObj:
                clientInfoObj=clientInfoObj[0]
                clientInfoObj.dateOfBirth=validated_data.get('dateOfBirth')
                clientInfoObj.mobileNumber=validated_data.get('mobileNumber')
                clientInfoObj.homeAddress=validated_data.get('homeAddress')
                clientInfoObj.workAddress=validated_data.get('workAddress')
                clientInfoObj.relationshipWithBank=validated_data.get('relationshipWithBank')
                clientInfoObj.save()
        else:
            userObj=User.objects.create(first_name=validated_data.get('first_name'),last_name=validated_data.get('last_name'),email=userEmail,username=userEmail)
            clientInfoObj=clientInformation.objects.create(dateOfBirth=validated_data.get('dateOfBirth'),
                               mobileNumber=validated_data.get('mobileNumber'),
                               homeAddress=validated_data.get('homeAddress'),
                               workAddress=validated_data.get('workAddress'),
                               relationshipWithBank=validated_data.get('relationshipWithBank'),user=userObj)
        #check account exist or not
        accntObj = BankAccount.objects.filter(client=clientInfoObj)
        if accntObj:
            accntObj=accntObj[0]
        else:
            accntObj = BankAccount.objects.create(client=clientInfoObj,status=2,type=1) #if account not exist ,create account

        return Loan.objects.create(client=clientInfoObj,bankAccount=accntObj,applyAmount=validated_data.get('applyAmount'),loanType=validated_data.get('loanType'),validTill=validated_data.get('validiity'))