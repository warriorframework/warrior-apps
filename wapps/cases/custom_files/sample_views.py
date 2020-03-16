# -*- coding: utf-8 -*-
import collections
import json
import os
import re
import xmltodict
from collections import OrderedDict
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from katana.utils.directory_traversal_utils import join_path, get_dir_from_path, get_parent_dir_path
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
from katana.wapps.cases.cases_utils.defaults import impacts, on_errors, runmodes, iteration_types, contexts
from katana.wapps.cases.cases_utils.get_drivers import GetDriversActions
from katana.wapps.cases.cases_utils.verify_case_file import VerifyCaseFile

navigator = Navigator()
CONFIG_FILE = join_path(navigator.get_katana_dir(), "config.json")
APP_DIR = join_path(navigator.get_katana_dir(), "wapps", "cases")
STATIC_DIR = join_path(APP_DIR, "static", "cases")
TEMPLATE = join_path(STATIC_DIR, "base_templates", "Untitled.xml")
DROPDOWN_DEFAULTS = read_json_data(join_path(STATIC_DIR, "base_templates", "dropdowns_data.json"))


class CasesView(View):

    def get(self, request):
        """
        Get Request Method
        """
        return render(request, 'cases/cases.html')


def get_list_of_cases(request):
    """
    Returns a list of cases
    """
    print("get list of files ")
    config = read_json_data(CONFIG_FILE)
    return JsonResponse({"data": navigator.get_dir_tree_json(config["xmldir"])})


def get_file(request):
    """
    Reads a case file and returns it's contents in JSOn format
    """
    print("get file")
    try:
        file_path = request.GET.get('path')
        if file_path == "false":
            file_path = TEMPLATE
        vcf_obj = VerifyCaseFile(TEMPLATE, file_path)
        output, data = vcf_obj.verify_file()
        if output["status"]:
            mid_req = (len(data["Testcase"]["Requirements"]["Requirement"]) + 1)/2
            repo_dirs = navigator.get_user_repos_dir()
            repo_dict = {}

            for repo in repo_dirs:
                repo_dict[repo] = {}

                repo_path = repo_dirs[str(repo)]
                da_obj = GetDriversActions(repo_path)
                if file_path == TEMPLATE:
                    output["filepath"] = read_json_data(CONFIG_FILE)["xmldir"]
                else:
                    output["filepath"] = get_parent_dir_path(file_path)
                output["filename"] = os.path.splitext(get_dir_from_path(file_path))[0]
                output["user_repos"] = repo_dirs

                repo_dict[repo]= da_obj.get_all_actions()
            output["drivers"] = repo_dict
            output["html_data"] = render_to_string('cases/display_case.html', {"data": data, "mid_req": mid_req,
                                                                               "defaults": DROPDOWN_DEFAULTS,
                                                                               "user_repos":repo_dirs})

            return JsonResponse(output)
        else:
            JsonResponse({"status": output["status"], "message": output["message"]})
    except Exception as e:
        return JsonResponse({"status": 0,"message":"Exception opening the file"})


