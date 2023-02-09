from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from .models import File
from .serializers import FileUploadSerializer,SaveFileSerializer
import openpyxl
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView


# remember to import the File model
# remember to import the FileUploadSerializer and SaveFileSerializer

class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print('-----------',serializer)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']

        wb = openpyxl.load_workbook(file)
        reader = wb.active
        # print('------',reader)
        header = [cell.value for cell in reader[1]]
        # print('header-------',header)
        excel_data = []
        for row in reader.iter_rows(min_row=2):
            excel_data.append({header[i]:row[i].value for i in range(len(header))})
        print(excel_data)
        print(len(excel_data))

        for row in (excel_data):
            print(row['name'])
            new_file = File(
                       id = row['id'],
                       name= row["name"],
                       position= row['position'],
                       age= row["age"],
                       year_joined= row["year"]
                       )
            new_file.save()
        return Response({"status": "success"})


# class UserViewSet(APIView):
#     def get(self, request, format=None):
#         snippets = File.objects.all()
#         print(snippets)
#         serializer = SaveFileSerializer(snippets, many=True)
#         return Response(serializer.data)
    
#     def get_queryset(self):
#         column_name = self.request.query_params.get('column_name')
#         sort_order = self.request.query_params.get('sort_order')
#         # Return the sorted rows as JSON
#         if column_name and sort_order:
#             return self.queryset.order_by(f'{sort_order}{column_name}')[:]
#         return self.queryset[:2]



class UserViewSet(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = SaveFileSerializer

    def get_queryset(self):
        column_name = self.request.query_params.get('column_name')
        sort_order = self.request.query_params.get('sort_order')
        # Return the sorted rows as JSON
        if column_name and sort_order:
            return self.queryset.order_by(f'{sort_order}{column_name}')[:]
        return self.queryset[:3]   # it give data you want in api ,we have 6 data but we see only 3 data
          