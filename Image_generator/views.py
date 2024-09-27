from django.http import HttpResponse
from django.shortcuts import render
import requests
import base64

def generate_image_view(request):
    prompt = request.GET.get('prompt', 'a beautiful sunset')
    
    # Replace with your ngrok URL
    ngrok_url = 'https://9436-34-169-125-51.ngrok-free.app/generate'

    # Send prompt to Flask API
    response = requests.post(ngrok_url, json={"prompt": prompt})

    if response.status_code == 200:
        # Convert the binary content to base64 for rendering in the template
        image_data = base64.b64encode(response.content).decode('utf-8')
        return render(request, 'image_generation/image_display.html', {
            'image_data': image_data,
            'prompt': prompt
        })
    else:
        return HttpResponse(f"Error: {response.status_code} - {response.text}", status=response.status_code)
