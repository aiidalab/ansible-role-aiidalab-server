import os
import warnings
from os import path
from jupyter_client.localinterfaces import public_ips
from oauthenticator.github import GitHubOAuthenticator
from tornado import gen

c = get_config()
#c.JupyterHub.log_level = 'DEBUG'
c.JupyterHub.logo_file          = "/etc/jupyterhub/aiidalab_wide.png"
c.JupyterHub.cookie_secret_file = "/var/jupyterhub/jupyterhub_cookie_secret"
c.JupyterHub.db_url             = "/var/jupyterhub/jupyterhub.sqlite"
c.JupyterHub.extra_log_file     = "/var/jupyterhub/jupyterhub.log"
c.JupyterHub.template_paths     = ["/etc/jupyterhub/templates", ]
# apparently this does not yet work properly with DockerSpawner
c.JupyterHub.cleanup_proxy      = False
c.JupyterHub.cleanup_servers    = False

auth_server = "{{ aiidalab_server_oauth_server }}"

#===============================================================================
# user Docker Spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# JupyterHub always runs image tagged as "aiidalab-image:latest" on local docker instance
c.DockerSpawner.image = "aiidalab-image:latest"
c.DockerSpawner.extra_host_config.update({
    # take care of lost child processes
    # see also: https://github.com/krallin/tini/issues/8
    'init': True,
   # constrain CPU usage, see
   # https://docs.docker.com/config/containers/resource_constraints/#cpu
   # https://github.com/docker/docker-py/blob/7911c5463557acce7f0def1d9572742ef04a98f5/docker/api/container.py#L432
    'cpu_period': 100000,
    'cpu_quota':  {{ (aiidalab_server_cpu_limit * 100000) | int }},
})
c.DockerSpawner.volumes = {'/var/jupyterhub/volumes/{username}' : '/home/aiida'}
c.DockerSpawner.remove_containers = True
c.JupyterHub.hub_ip = public_ips()[0] # default loopback port doesn't work
c.Spawner.start_timeout = 180
c.Spawner.http_timeout = 120
c.Spawner.mem_limit = '{{ aiidalab_server_mem_limit }}'

#===============================================================================
# Simple FirstUseAuthenticator to get started
from firstuseauthenticator import FirstUseAuthenticator
c.JupyterHub.authenticator_class = FirstUseAuthenticator
c.FirstUseAuthenticator.create_users = {{ aiidalab_server_create_users }}

#===============================================================================
# OAuth2 authenticator example below
#from oauthenticator.generic import GenericOAuthenticator, GenericEnvMixin

# key for encrypting access_token generated using `openssl rand -hex 32`
#jupyterhub_crypt_key = '{{ aiidalab_server_crypt_key }}'
# Alternatively pass it via JUPYTERHUB_CRYPT_KEY environment variable
#c.CryptKeeper.keys = [ jupyterhub_crypt_key ]

#c.JupyterHub.authenticator_class = GenericOAuthenticator
#GenericEnvMixin._OAUTH_AUTHORIZE_URL = auth_server + "/oauth2/auth"
#
#c.EnvOAuthenticator.custom_html = login_html
#c.EnvOAuthenticator.login_service = "Materials Cloud"
#c.EnvOAuthenticator.enable_auth_state = True
#
##c.EnvOAuthenticator.auto_login = True
#c.EnvOAuthenticator.client_id = "{{ aiidalab_server_name }}"
#c.EnvOAuthenticator.oauth_callback_url = "https://{{ aiidalab_server_name }}/hub/oauth_callback"
#c.EnvOAuthenticator.token_url = auth_server + "/oauth2/token"
#c.EnvOAuthenticator.client_secret = "{{ aiidalab_server_oauth_client_secret }}"
#c.EnvOAuthenticator.userdata_url = auth_server + "/oauth2/userinfo"

## overwrite logout handler to also logout of main Materials Cloud site
## https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/handlers/login.py#L14
#import urllib.parse
#def logout_handler(self):
#    user = self.get_current_user()
#    if user:
#        self.log.info("User logged out: %s", user.name)
#        self.clear_login_cookie()
#        self.statsd.incr('logout')
#    next = urllib.parse.quote("https://{{ aiidalab_server_name }}")
#    url = auth_server + "/logout?next="+next
#    self.redirect(url, permanent=False)
#
#from jupyterhub.handlers.login import LogoutHandler
#LogoutHandler.get = logout_handler

#===============================================================================
# create home directory if it doesn't exist already
def pre_spawn_hook(spawner):
    project_dir = "/var/jupyterhub/volumes/" + spawner.user.name
    if not path.exists(project_dir):
        spawner.log.info("Creating directory: "+project_dir)
        os.mkdir(project_dir)
c.Spawner.pre_spawn_hook = pre_spawn_hook
