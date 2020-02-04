"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

# -*- coding: utf-8 -*-


import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from katana.native.settings.settings import Settings
from katana.utils.navigator_util import Navigator
from katana.utils.json_utils import read_json_data
import ast
import json

nav_obj = Navigator()
REF_FILE = os.path.join(nav_obj.get_katana_dir(), "katana.native", "assembler", "static", "assembler",
                        "base_templates", "empty.xml")
config_json_path = os.path.join(nav_obj.get_katana_dir(),"config.json")

controls = Settings()

def index(request):
    return render(request, 'settings/index.html', {"data": controls.get_location()})

def email_setting_handler( request ):
    return render(request, 'settings/email_setting_handler.html', {"setting": controls.email_setting_handler(request)})

def secret_handler( request ):
    return render(request, 'settings/secret.html', {"secret": controls.secret_handler(request)})

def jira_setting_handler( request ):
    return render(request, 'settings/jira_setting_handler.html', {"jira": controls.jira_setting_handler(request)})

def general_setting_handler( request ):
    return render(request, 'settings/general_setting_handler.html', {"data": controls.general_setting_handler(request)})

def profile_setting_handler( request ):
    return render(request, 'settings/profile_setting_handler.html', {"data": controls.profile_setting_handler(request)})

def smart_analysis_handler( request ):
    return render(request, 'settings/smart_analysis_handler.html', {"data": controls.smart_analysis_handler(request)})

def prerequisites_handler(request):
    return render(request, 'settings/prerequisites_handler.html', {"data": controls.prerequisites_handler(request)})

def install_prerequisite(request):
    return JsonResponse(controls.prereq_installation_handler(request))

def validate_input_repo(request):
    paths_string=request.POST.get('paths')
    paths_list = ast.literal_eval(paths_string)
    for i in paths_list:
        if os.path.exists(i):
           in_valid=False
        else:
            in_valid=True
            break
    if(in_valid):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def myajaxtestview(request):
    return HttpResponse(request.POST['text'])

def populate_paths(request):
    returned_json = read_json_data(config_json_path)
    if os.path.isdir(returned_json["pythonsrcdir"]):
        if returned_json["pythonsrcdir"].split("/")[-1] == "Warriorspace" or returned_json["pythonsrcdir"].split("/")[-2] == "Warriorspace":
            child_dirs = os.listdir(returned_json["pythonsrcdir"])
            if "Testcases" in child_dirs:
                returned_json["xmldir"] = returned_json["pythonsrcdir"] + "/Testcases"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/Testcases")
                returned_json["xmldir"] = (returned_json["pythonsrcdir"] + "/Testcases")
            
            if "Suites" in child_dirs:
                returned_json["testsuitedir"] = returned_json["pythonsrcdir"] + "/Suites"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/Suites")
                returned_json["testsuitedir"] = (returned_json["pythonsrcdir"] + "/Suites")
            
            if "Projects" in child_dirs:
                returned_json["projdir"] = returned_json["pythonsrcdir"] + "/Projects"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/Projects")
                returned_json["projdir"] = (returned_json["pythonsrcdir"] + "/Projects")
            
            if "Data" in child_dirs:
                returned_json["idfdir"] = returned_json["pythonsrcdir"] + "/Data"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/Data")
                returned_json["idfdir"] = (returned_json["pythonsrcdir"] + "/Data")

            if "Config_files" in child_dirs:
                returned_json["testdata"] = returned_json["pythonsrcdir"] + "/Config_files"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/Config_files")
                returned_json["testdata"] = (returned_json["pythonsrcdir"] + "/Config_files")

            if "wrapper_files" in child_dirs:
                returned_json["testwrapper"] = returned_json["pythonsrcdir"] + "/wrapper_files"
            else:
                os.mkdir(returned_json["pythonsrcdir"] + "/wrapper_files")
                returned_json["testwrapper"] = (returned_json["pythonsrcdir"] + "/wrapper_files")
        else:
            base_tree = os.listdir(returned_json["pythonsrcdir"])
            if "Warriorspace" in base_tree:
                child_dirs = os.listdir(returned_json["pythonsrcdir"])
                if "Testcases" in child_dirs:
                    returned_json["xmldir"] = returned_json["pythonsrcdir"] + "/Testcases"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Testcases")
                    returned_json["xmldir"] = (returned_json["pythonsrcdir"] + "/Testcases")
            
                if "Suites" in child_dirs:
                    returned_json["testsuitedir"] = returned_json["pythonsrcdir"] + "/Suites"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Suites")
                    returned_json["testsuitedir"] = (returned_json["pythonsrcdir"] + "/Suites")
                
                if "Projects" in child_dirs:
                    returned_json["projdir"] = returned_json["pythonsrcdir"] + "/Projects"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Projects")
                    returned_json["projdir"] = (returned_json["pythonsrcdir"] + "/Projects")
            
                if "Data" in child_dirs:
                    returned_json["idfdir"] = returned_json["pythonsrcdir"] + "/Data"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Data")
                    returned_json["idfdir"] = (returned_json["pythonsrcdir"] + "/Data")

                if "Config_files" in child_dirs:
                    returned_json["testdata"] = returned_json["pythonsrcdir"] + "/Config_files"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Config_files")
                    returned_json["testdata"] = (returned_json["pythonsrcdir"] + "/Config_files")
                if "wrapper_files" in child_dirs:
                    returned_json["testwrapper"] = returned_json["pythonsrcdir"] + "/wrapper_files"
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/wrapper_files")
                    returned_json["testwrapper"] = (returned_json["pythonsrcdir"] + "/wrapper_files")
            else:
                if "Testcases" in base_tree or "Suites" in base_tree or "Data" in base_tree or "wrapper_files" in base_tree or "Config_files" in base_tree or "Projects" in base_tree or "Execution" in base_tree:
                    sub_folders = {"Testcases":"xmldir","Suites":"testsuitedir","Projects":"projdir","Data": "idfdir","Config_files":"testdata","wrapper_files":"testwrapper"}
                    for folder in ["Testcases", "Suites", "Data", "wrapper_files", "Config_files", "Projects"]:
                        try:
                            os.mkdir(returned_json["pythonsrcdir"] + "/"+ folder)
                            returned_json[sub_folders[folder]] = returned_json["pythonsrcdir"] + "/"+ folder
                        except FileExistsError:
                            returned_json[sub_folders[folder]] = returned_json["pythonsrcdir"] + "/"+ folder
                else:
                    os.mkdir(returned_json["pythonsrcdir"] + "/Warriorspace")
                    sub_folders = {"Testcases":"xmldir","Suites":"testsuitedir","Projects":"projdir","Data": "idfdir","Config_files":"testdata","wrapper_files":"testwrapper"}
                    for folder in ["Testcases", "Suites", "Data", "wrapper_files", "Config_files", "Projects"]:
                        os.mkdir(returned_json["pythonsrcdir"] + "/Warriorspace/"+ folder)
                        returned_json[sub_folders[folder]] = returned_json["pythonsrcdir"] + "/Warriorspace/"+ folder
    with open(config_json_path, "w") as f:
        f.write(json.dumps(returned_json, indent=4))
    return HttpResponse(request)