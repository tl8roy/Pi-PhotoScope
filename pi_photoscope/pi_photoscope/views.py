from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

from os import listdir,mkdir
from os.path import isfile, isdir, join
import tempfile, zipfile

import datetime
from time import sleep

from fractions import Fraction

#from .models import Photos
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
            #camera.capture(settings.ASTRO_IMAGES + 'preview.jpg')
        import base64
        image = settings.ASTRO_IMAGES+'preview.jpg'
        image_64 = base64.encodestring(open(image, "rb").read())

        #Process our actual sequence
        if request.POST['submit_btn'] == 'go':
            #Get all our astro folders
            folders = [ f for f in listdir(settings.ASTRO_IMAGES) if isdir(join(settings.ASTRO_IMAGES,f)) ]
            newFolderId = 1
            makeADir = True
            today = datetime.date.today().strftime('%Y-%m-%d')

            #Go through each folder to see if we have today's
            for folder in folders:
                folderID = folder.split('_')
                #If it is todays, skip the rest
                if folderID[1] == today:
                    newFolderId = folderID[0]
                    makeADir = False
                    break
                elif newFolderId <= int(folderID[0]):
                    #If the folder id is less than the current ID
                    newFolderId = int(folderID[0]) + 1

            #Set the current folder and make it if required
            currentFolder = settings.ASTRO_IMAGES + str(newFolderId)+ '_' + today
            if makeADir:
                mkdir(currentFolder)

            #Go through the folder to get the latest file id
            newFileId = 1
            files = [ f for f in listdir(currentFolder) if isfile(join(currentFolder,f)) ]
            for file in files:
                fileID = file.split('_')
                if newFileId <= int(fileID[0].replace('.txt','')):
                    newFileId = int(fileID[0].replace('.txt','')) + 1

            #Write out a text file with the settings we used
            f = open(currentFolder + '/' + str(newFileId) + '.txt','w+')
            f.write('ID: ' + str(newFileId) + "\n")
            f.write('Date: ' + str(datetime.datetime.now()) + "\n")
            f.write('Name: ' + photo_parameters['name'] + "\n")
            f.write('ISO: ' + str(photo_parameters['iso']) + "\n")
            f.write('Shutter Speed:' + str(photo_parameters['shutter_speed']) + " s\n")
            f.write('Shutter Speed Inverse: 1/' + str(photo_parameters['shutter_speed_inverse']) + "\n")
            f.write('Number of Pictures: ' + str(photo_parameters['num_to_take']) + "\n")
            f.write('Time Between: ' + str(photo_parameters['time_between']) + "\n")
            f.close()

            #Shoot the images
            for i in range(1,photo_parameters['num_to_take'] + 1):
                sleep(photo_parameters['time_between'])
                f = open(currentFolder + '/' + str(newFileId) + '_' + str(i) +'.jpg','w+')
                f.close()
                #camera.capture(currentFolder + '/' + str(newFileId) + '_' + str(i) +'.jpg')

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

