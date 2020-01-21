from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class LoanProcess(APIView):

    def post(self, request, format=None):
        try:
            str=''
            serializer = LoanProcessSerializer(data=request.data)
            if serializer.is_valid():
                loanObj=serializer.save()
                if loanObj:
                    str="Congratulations ,You have applied loan for amount {} .Your Loan Account is {} . This is under processing".format(loanObj.applyAmount,loanObj.id)
                    message=dict()
                    message["message"]=str
                    message["status"]="success"
                    return Response(message,status.HTTP_201_CREATED)
        except Exception as e:
            message["message"] = str(e)
            message["status"] = "failed"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        LoanObjQuerySet = Loan.objects.all()
        serializer = LoanSerializer(LoanObjQuerySet, many=True)
        if serializer.data:
            return Response(serializer.data[0])
        else:
            return Response("Laon Data not found in database")



class ApproveLoans(APIView):

    def post(self ,request, format=None):
        try:
            serializer = LoanApprovalSerializer(data=request.data)
            if serializer.is_valid():
                res=serializer.save()
                message=dict()
                message["message"] = res
                message["status"] = "success"
                return Response(message, status.HTTP_200_OK)
        except Exception as e:
            message=dict()
            message["message"] = str(e)
            message["status"] = "failed"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)