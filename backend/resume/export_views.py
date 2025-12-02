from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Resume
from .export_utils import generate_pdf, generate_docx
import os


class ResumeExportPDFView(APIView):
    """Экспорт резюме в PDF"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        try:
            pdf_file = generate_pdf(resume)
            
            # Формируем имя файла
            filename = f"{resume.title.replace(' ', '_')}.pdf"
            
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        except Exception as e:
            return Response({
                'error': f'Ошибка при генерации PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResumeExportDOCXView(APIView):
    """Экспорт резюме в DOCX"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        try:
            docx_file = generate_docx(resume)
            
            # Формируем имя файла
            filename = f"{resume.title.replace(' ', '_')}.docx"
            
            response = HttpResponse(
                docx_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        except Exception as e:
            return Response({
                'error': f'Ошибка при генерации DOCX: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)