from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json

key = "gomugomunojetpistol"

def home(request):
    if request.method == 'POST':
        input_key = request.POST.get('key')
        files = request.FILES.getlist('files')
        if not files:
            error_message = {"error": "No files uploaded"}
            return JsonResponse(error_message, status=401) 
        elif key == input_key:
            dropdown_option = request.POST.get('dropdown')
            s3_folder_path = dropdown_option
            url = 'https://us-central1-appydesigne-24e6c.cloudfunctions.net/python_widget/ AppyUpload'
            response_data = {
                "success" : {},
                "error" : {}
            }

            for file in files:
                payload = {'filename': file.name, 'folderpath': s3_folder_path}
                files_data = {'file': (file.name, file.read(), file.content_type)}
                response = (requests.post(url, data=payload, files=files_data)).json()
                if response["statusCode"] == 200:
                    response_data["success"][file.name] = response["FileUrl"]
                else:
                    response_data["error"][file.name] = response["error"]
            response_json = json.dumps(response_data, indent=4)

            # Create an HTTP response with the JSON content
            response = HttpResponse(response_json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="response_data.json"'
            return response
        else:
            error_message = {"error": "Incorrect key provided"}
            return JsonResponse(error_message, status=401) 
        
    return render(request, 'myapp/home.html')
