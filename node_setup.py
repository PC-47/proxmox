#!/bin/python3

import subprocess

task_count = 0

# simple function to print tasks with task number
def print_task(task: str) -> None:
    global task_count
    task_count += 1
    print(f'  {task_count}) {task}')


# function to set and comment appropriate repos for non enterprise pve node
def set_repos() -> None:
    print_task('setting subscription repo to pve-no-subscription')
    try:
        with open('/etc/apt/sources.list', 'w') as f:
            f.write('deb http://ftp.us.debian.org/debian bookworm main contrib\n\n')
            f.write('deb http://ftp.us.debian.org/debian bookworm-updates main contrib\n\n')
            f.write('# security updates\n')
            f.write('deb http://security.debian.org bookworm-security main contrib\n\n')
            f.write('# pve no subscription repository\n')
            f.write('deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription\n')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')

    print_task('disabling pve-enterprise repo')
    try:
        with open('/etc/apt/sources.list.d/pve-enterprise.list', 'w') as f:
            f.write('# comment out\n')
            f.write('# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise\n')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')

    print_task('disabling ceph enterprise repo')
    try:
        with open('/etc/apt/sources.list.d/ceph.list', 'w') as f:
            f.write('# comment out\n')
            f.write('# deb https://enterprise.proxmox.com/debian/ceph-quincy bookworm enterprise\n')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')


# function to update the host
def update_host() -> None:
    print_task('updating host with "apt update"')
    command = 'apt update'
    try:
        process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
        stdout, stderr = process.communicate()
        exit_code = process.returncode
    except Exception as e:
        print(f'ERROR running {command}, {e}')


# function to upgrade the host
def upgrade_host() -> None:
    print_task('upgrading host with "apt dist-upgrade -y"')
    command = 'apt dist-upgrade -y'
    try:
        process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
        stdout, stderr = process.communicate()
        exit_code = process.returncode
    except Exception as e:
        print(f'ERROR running {command}, {e}')


if __name__ == '__main__':
    print('\nStarting PVE Node Setup Script')
    set_repos()
    update_host()
    upgrade_host()
    print('Finished PVE Node Setup Script\n')
