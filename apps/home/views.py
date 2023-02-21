# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from collections import Counter

from django.shortcuts import render, redirect
from py_templates.my_model import ModelPredict
import os
import pandas as pd

@login_required(login_url="/login/")
def index(request):
    
    
    context = {

        'segment': 'index',
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        #print(load_template)

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def readfile(filename):

    #we have to create those in order to be able to access it around
    # use panda to read the file because i can use DATAFRAME to read the file
    #column;culumn2;column
    global data,missingvalue,myfile
     #read the missing data - checking if there is a null
    missingvalue = ['?', '--']

    my_file = pd.read_csv(filename, sep='[:;,|_]',na_values=missingvalue, engine='python')

    data = pd.DataFrame(data=my_file, index=None)
    #print(data)



def pageblank(request):
    context = {}
    print('\n hello')
    if request.method == 'POST':
        
        uploaded_file = request.FILES['document']
        

        #check if this file ends with csv
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            d = os.getcwd()
            name = savefile.save(d+'\\media\\'+uploaded_file.name, uploaded_file) #gets the name of the file
            
            print(name)
            # how we get the current dorectory
            print('\n'+d+'\n\n')
            file_directory = d+'\\'+name #saving the file in the media directory
            print('\n'+ file_directory+'\n\n')
            readfile(file_directory)
            print('\n\n\n is here\n\n')
            preds = ModelPredict(data)
            context = {

                'segment': 'index',
                'predictions': preds,
            }

            #we need to save the file somewhere in the project, MEDIA
            #now lets do the savings

             #saving the file in the media directory
            #print(file_directory)
            #readfile(file_directory)
            # Remove the file
            # 'file.txt'
            os.remove(file_directory)
            
            html_template = loader.get_template('home/index.html')
            return HttpResponse(html_template.render(context, request))

        else:
            messages.warning(request, 'File was not uploaded. Please use .csv file extension!')


    html_template = loader.get_template('home/page-blank.html')
    return HttpResponse(html_template.render(context, request))
    
