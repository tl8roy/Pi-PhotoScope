from django.http import HttpResponse
import tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
#from .models import Photos

#import time
#from time import sleep
from fractions import Fraction
#import picamera

def index(request):
    return HttpResponse(render(request, 'pi_photoscope/index.html'))

def take(request):
    photo_parameters = {}
    image_64 = ''

    if request.method == 'POST':

        #Get the shutter speed in seconds
        if request.POST['ss'] == 'long':
            shutter_speed = float(request.POST['ss_long'])
            shutter_speed_inverse = 1 / float(request.POST['ss_long'])
        else:
            shutter_speed = 1 / int(request.POST['ss_short'])
            shutter_speed_inverse = int(request.POST['ss_short']);

        photo_parameters = {
            'name': request.POST['name'],
            'iso': int(request.POST['iso']),
            'time_between': float(request.POST['time_between']),
            'num_to_take': int(request.POST['num_to_take']),
            'shutter_speed': shutter_speed,
            'shutter_speed_inverse': shutter_speed_inverse,
        }

        """with picamera.PiCamera() as camera:
            camera.resolution = (2592,1944)
            # Set a framerate of 1/6fps, then set shutter
            # speed to 6s and ISO to 800
            camera.framerate = Fraction(photo_parameters['shutter_speed_inverse'])
            camera.shutter_speed = photo_parameters['shutter_speed'] * 1000000
            camera.exposure_mode = 'off'
            camera.iso = photo_parameters['iso']
            # Give the camera a good long time to measure AWB
            # (you may wish to use fixed AWB instead)


            # Wait for analog gain to settle on a higher value than 1
            while camera.analog_gain <= 1:
                pass
                #time.sleep(0.1)
            g = camera.awb_gains
            camera.awb_mode = 'off'
            camera.awb_gains = g
            #sleep(10)"""

            # Take a preview Image
            #camera.capture('preview.jpg')
        import base64
        image = settings.ASTRO_IMAGES+'preview.jpg'
        image_64 = base64.encodestring(open(image, "rb").read())

        #Only take 1 photo and send it to a known location
        if request.POST['submit_btn'] == 'go':
            pass
            """camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])"""

    return HttpResponse(render(request, 'pi_photoscope/take_photos.html', {
        'photo_parameters': photo_parameters,
        'preview_img': image_64
    }))

def view(request):
    return HttpResponse(render(request, 'pi_photoscope/view_photos.html'))

def download(request,photo_id):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = __file__ # Select your files here.
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp, "rb")
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response

def delete(request,photo_id):
    return redirect('view')

