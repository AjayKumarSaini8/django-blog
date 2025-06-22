# blog_project/utils/file_upload.py
import json
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CustomFileUploadView(View):
    def post(self, request):
        uploaded_file = request.FILES.get('upload')
        
        # Validate file exists
        if not uploaded_file:
            return JsonResponse({
                'error': {'message': 'No file provided'}
            }, status=400)
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({
                'error': {'message': 'Invalid file type. Only images are allowed.'}
            }, status=400)
        
        # Validate file size (5MB limit)
        max_size = 5 * 1024 * 1024
        if uploaded_file.size > max_size:
            return JsonResponse({
                'error': {'message': f'File too large. Max size is {max_size//1024//1024}MB.'}
            }, status=400)
        
        # Save the file
        file_path = default_storage.save(f'uploads/{uploaded_file.name}', uploaded_file)
        file_url = default_storage.url(file_path)
        
        return JsonResponse({
            'url': file_url,
            'fileName': uploaded_file.name,
            'uploaded': 1
        })