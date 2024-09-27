from django.http import HttpResponse
import requests
from django.shortcuts import render
import json

def generate_image_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', 'a beautiful sunset')
        
        # Replace with your ngrok URL
        ngrok_url = 'https://e77e-34-169-125-51.ngrok-free.app/generate'

        # Send prompt to Google Colab (Flask API)
        try:
            response = requests.post(ngrok_url, json={"prompt": prompt})
            response.raise_for_status()  # Ensure it raises an error if status_code is not 200
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error communicating with the image generation service: {str(e)}", status=500)

        # Try to parse the response as JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            return HttpResponse("Error: The response from the image generation service is not valid JSON.", status=500)

        # Check if the image is in the response
        if 'image' in response_data:
            image_data = response_data['image']
            content_type = "image/png"
            return render(request, 'image_generation/image_display.html', {
                'image_data': image_data,
                'content_type': content_type,
                'prompt': prompt
            })
        else:
            return HttpResponse(f"Error: Image data not found in the response from the image generation service.", status=500)

    return render(request, 'image_generation/index.html')
