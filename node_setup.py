#!/bin/python3

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
            f.write('deb http://ftp.us.debian.org/debian bookworm main contrib')
            f.write('')
            f.write('deb http://ftp.us.debian.org/debian bookworm-updates main contrib')
            f.write('')
            f.write('# security updates')
            f.write('deb http://security.debian.org bookworm-security main contrib')
            f.write('')
            f.write('# pve no subscription repository')
            f.write('deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')
    
    print_task('disabling pve-enterprise repo')
    try:
        with open('/etc/apt/sources.list.d/pve-enterprise.list', 'w') as f:
            f.write('# comment out')
            f.write('# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')

    print_task('disabling ceph enterprise repo')
    try:
        with open('/etc/apt/sources.list.d/ceph.list', 'w') as f:
            f.write('# comment out')
            f.write('# deb https://enterprise.proxmox.com/debian/ceph-quincy bookworm enterprise')
    except Exception as e:
        print(f'ERROR: {e} while changing main sources list')


if __name__ == '__main__':
    print('Starting PVE Node Setup Script')
    set_repos()
