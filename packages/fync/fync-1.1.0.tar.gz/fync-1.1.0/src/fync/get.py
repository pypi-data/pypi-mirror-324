import argparse
import configparser
import os
from pathlib import Path
import tempfile
import urllib
import urllib.parse
import urllib.request
import shutil

config = configparser.ConfigParser()
file_path = Path.home().joinpath('.fync-get')


def url_request(url, opener):
    urllib.request.install_opener(opener)
    with tempfile.NamedTemporaryFile(
        prefix='fync_', suffix='.download', delete=False
    ) as temp_file:
        try:
            temporary_filename, headers = urllib.request.urlretrieve(
                url, temp_file.name
            )
            filename = headers.get_filename()
            if filename:
                shutil.move(temporary_filename, filename)
                return filename
        except urllib.error.URLError as e:
            print(f'Error downloading {url}: {e}')
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    return None


def download_bearer(url, token):
    print('Download (Authorization Bearer) ..')
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', f'Bearer {token}')]
    result = url_request(url, opener)
    print(
        'Download (Authorization Bearer) ' + ('done' if result else 'failed')
    )
    return result


def download_basic(url, username, password):
    print('Download (Authorization Basic) ..')
    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
    opener = urllib.request.build_opener(auth_handler)
    result = url_request(url, opener)
    print('Download (Authorization Basic) ' + ('done' if result else 'failed'))
    return result


def save_credentials(section, credentials):
    config.read(file_path)
    if section not in config:
        config.add_section(section)
    for credential, value in credentials.items():
        config[section][credential] = value
    with open(file_path, 'w') as configfile:
        config.write(configfile)


def cli():
    parser = argparse.ArgumentParser(
        description='Authenticated file download.'
    )
    parser.add_argument(
        'urls', nargs=argparse.REMAINDER, help='URLs to download from.'
    )
    parser.add_argument(
        '--update', action='store_true', help='Update credentials'
    )
    args = parser.parse_args()

    if not args.urls:
        parser.print_help()
        return

    config.read(file_path)

    for url in args.urls:
        parsed_url = urllib.parse.urlparse(url)
        section = f'credentials-{parsed_url.netloc}'

        update_credentials = args.update
        authorization = None
        try:
            username = config[section]['username']
            password = config[section]['password']
            authorization = config[section].get('authorization')
        except KeyError:
            update_credentials = True

        if update_credentials:
            username = input(f'({parsed_url.netloc}) Username: ')
            password = input(f'({parsed_url.netloc}) Password: ')
            save = input(f'({parsed_url.netloc}) Save credentials? [y/n]: ')
            if save.lower().startswith('y'):
                save_credentials(
                    section, {'username': username, 'password': password}
                )

        if authorization == 'bearer':
            result = download_bearer(url, password)
        elif authorization == 'basic':
            result = download_basic(url, username, password)
        else:
            result = download_bearer(url, password)
            if not result:
                result = download_basic(url, username, password)

            if result:
                save_credentials(
                    section, {'authorization': 'bearer' if result else 'basic'}
                )

        if not result:
            exit(1)
