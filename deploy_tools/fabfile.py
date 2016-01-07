from fabric.contrib.files import append, exists, sed
from fabric.api import *
from fabric.operations import local, put
import random
import time
import subprocess
import os
import boto.ec2

REPO_URL = 'https://github.com/jchen7960/tdd_python'

env.hosts = ['localhost',]
env.aws_region = 'us-west-2'

@task
def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

@task
def deploy_small_ec2_instance():
    local('/usr/bin/ec2-run-instances ami-5189a661 --instance-type t2.micro --region us-west-2 --key ${EC2_KEYPAIR} --user-data user-data.sh --group ${SGROUP}')

@task
def deploy_medium_ec2_instance():
    local('/usr/bin/ec2-run-instances ami-6dacf728 --instance-type c1.medium --region us-west-2 --key ${EC2_KEYPAIR} --user-data-file user-data.sh --group ${SGROUP}')

@task
def deploy_large_ec2_instance():
    local('/usr/bin/ec2-run-instances ami-6dacf728 --instance-type m1.large --region us-west-2 --key ${EC2_KEYPAIR} --user-data-file user-data.sh --group ${SGROUP}')

@task
def deploy_large_ec2_instance():
    local('/usr/bin/ec2-run-instances ami-6dacf728 --instance-type m1.large --region us-west-2 --key ${EC2_KEYPAIR} --user-data-file user-data.sh --group ${SGROUP}')
                                

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))
