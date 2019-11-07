"""This script collects all the registered apps from the aiidalab-registry and adds git-related information to them"""
from __future__ import print_function
import codecs
import json
import os
import sys
import requests
from collections import OrderedDict

outdir_abs = '/var/appsdata/out'
apps_meta_file = 'apps_meta.json'
registry_url = 'https://raw.githubusercontent.com/aiidalab/aiidalab-registry/master/apps.json'
categories_url = 'https://raw.githubusercontent.com/aiidalab/aiidalab-registry/master/categories.json'

def validate_meta_info(app_name, meta_info):
    if not 'state' in meta_info.keys():
        meta_info['state'] = 'registered'

    if not 'title' in meta_info.keys():
        meta_info['title'] = app_name

    return meta_info

def get_hosted_on(url):
    if sys.version_info[0] < 3:
        from urlparse import urlparse
    else:
        from urllib.parse import urlparse
    try:
        netloc = urlparse(app_data['git_url']).netloc
    except Exception as e:
        print (e)
        return None

    # Remove port (if any)
    netloc = netloc.partition(':')[0]

    # Remove subdomains (this only works for domain suffixes of length 1!)
    # TODO: fix it for domains like yyy.co.uk
    netloc = ".".join(netloc.split('.')[-2:])

    return netloc

def get_meta_info(json_url):
    if sys.version_info[0] < 3:
        from urllib2 import urlopen
    else:
        from urllib.request import urlopen
    try:
        response = urlopen(json_url)
        json_txt = response.read()
    except Exception as e:
        import traceback
        print ("  >> UNABLE TO RETRIEVE THE JSON URL: {}".format(json_url))
        print (traceback.print_exc(file=sys.stdout))
        return None
    try:
        json_data = json.loads(json_txt)
    except ValueError:
        print ("  >> WARNING! Unable to parse JSON")
        return None

    return json_data

def get_git_branches(git_url):
    from dulwich.client import get_transport_and_path_from_url
    t, p = get_transport_and_path_from_url(git_url)
    branches = {key.decode("utf-8"):value.decode("utf-8") for key, value in t.get_refs(p).items() if not key.startswith(b'refs/pull/')} 
    return branches

if __name__ == "__main__":
    apps_raw_data = requests.get(registry_url).json()
    categories_raw_data = requests.get(categories_url).json()

    all_data = {}
    all_data['apps'] = OrderedDict()
    all_data['categories'] = categories_raw_data

    #print ("[apps]")
    for app_name in sorted(apps_raw_data.keys()):
        #print ("  - {}".format(app_name))
        app_data = apps_raw_data[app_name]

        hosted_on = get_hosted_on(app_data['git_url'])

        # Get meta.json from the project;
        # set to None if not retrievable
        try:
            meta_url = app_data['meta_url']
        except KeyError:
            print ("  >> WARNING: Missing meta_url!!!")
            meta_info = None
        else:
            meta_info = get_meta_info(meta_url)

        if meta_info is None:
            sys.exit(1)

        app_data['metainfo'] = validate_meta_info(app_name, meta_info)
        app_data['gitinfo'] = get_git_branches(app_data['git_url'])
        app_data['hosted_on'] = hosted_on

        #Fix for the backwards compatibility
        if 'categories' in app_data:
            app_data['groups'] = app_data['categories']

        all_data['apps'][app_name] = app_data


    if not os.path.exists(outdir_abs):
        os.makedirs(outdir_abs, exist_ok=True)

    outfile = os.path.join(outdir_abs, apps_meta_file)
    with codecs.open(outfile, 'w', 'utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
