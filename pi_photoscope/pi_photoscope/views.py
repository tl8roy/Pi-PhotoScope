from django.http import HttpResponse
import tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Photos

def index(request):
    return HttpResponse(render(request, 'pi_photoscope/index.html'))

def take(request):
    return HttpResponse(render(request, 'pi_photoscope/take_photos.html'))

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

