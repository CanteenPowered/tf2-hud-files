import os
import re
import shutil
import subprocess

def require_command(name):
    path = shutil.which(name)
    if path is None:
        print(f'Please install {name}')
        quit(1)
    return path

if __name__ == '__main__':
    basedir = os.path.dirname(os.path.realpath(__file__))

    cmd_depotdownloader = require_command('depotdownloader')
    cmd_vpk = require_command('vpk')

    if not 'STEAM_USERNAME' in os.environ or not 'STEAM_PASSWORD' in os.environ:
        print('Either STEAM_USERNAME or STEAM_PASSWORD is unset')
        quit(1);

    login_username = os.environ['STEAM_USERNAME']
    login_password = os.environ['STEAM_PASSWORD']

    # Download OSX client files
    subprocess.run([cmd_depotdownloader,
        '-username',    login_username,
        '-password',    login_password,
        '-app',         '440',
        '-dir',         os.path.join(basedir, 'files'),
        '-filelist',    os.path.join(basedir, 'update_filefilter.txt'),
    ])

    # Extract game version
    with open(os.path.join(basedir, 'files', 'tf', 'steam.inf'), 'r') as f1:
        version = re.search(r'PatchVersion=(.*)', f1.read())[1]
        with open(os.path.join(basedir, 'version.txt'), 'w') as f2:
            f2.write(version)

    # Extract popfiles
    subprocess.run([cmd_vpk,
        '-x',       basedir,
        '-re',      '^resource/.*\\.res$',
        os.path.join(basedir, 'files', 'tf', 'tf2_misc_dir.vpk')
    ])
