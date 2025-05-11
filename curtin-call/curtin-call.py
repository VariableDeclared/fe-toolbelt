import yaml

def get_user_input(prompt, default=None):
    value = input(f"{prompt} [{default}]: ") if default else input(f"{prompt}: ")
    return value.strip() or default

def build_storage_config():
    device = get_user_input("Enter disk device (e.g., /dev/sda)", "/dev/sda")
    use_crypt = get_user_input("Encrypt with LUKS? (yes/no)", "no").lower() == "yes"
    use_lvm = get_user_input("Use LVM? (yes/no)", "yes").lower() == "yes"

    storage = {'version': 1, 'config': []}
    
    # Base disk
    storage['config'].append({
        'id': 'disk0',
        'type': 'disk',
        'path': device,
    })

    # Partition table
    # Boot
    storage['config'].append({
        'id': 'grub-part0',
        'flag': 'boot',
        'name': 'grub-part0',
        'number': 1,
        'size': '512M',
        'wipe': 'superblock',
        'type': 'partition',
        'device': 'disk0'
    })
    storage['config'].append({
        'id': 'grub-part1',
        'name': 'grub-part1',
        'number': 2,
        'size': '5G',
        'wipe': 'superblock',
        'type': 'partition',
        'device': 'disk0'
    })
    # OS and other layers
    storage['config'].append({
        'id': 'ptable0',
        'type': 'partition_table',
        'table_type': 'gpt',
        'device': 'disk0',
    })

    # Single full partition
    storage['config'].append({
        'id': 'main-part',
        'type': 'partition',
        'device': 'ptable0',
        'size': '80%',
    })

    volume_id = 'main-part'

    # Optional encryption
    if use_crypt:
        storage['config'].append({
            'id': 'crypt-vol',
            'type': 'dm_crypt',
            'volume': volume_id,
            'key': 'random',
            'cipher': 'aes-xts-plain64',
            'name': 'cryptroot'
        })
        volume_id = 'crypt-vol'

    # Optional LVM
    if use_lvm:
        storage['config'].append({
            'id': 'pv0',
            'type': 'lvm_pv',
            'volume': volume_id,
        })
        storage['config'].append({
            'id': 'vg0',
            'type': 'lvm_vg',
            'name': 'vgroot',
            'devices': ['pv0'],
        })

        # Root LV
        storage['config'].append({
            'id': 'lv-root',
            'type': 'lvm_lv',
            'name': 'root',
            'vg': 'vg0',
            'size': '100%',
        })

        # Format root
        storage['config'].append({
            'id': 'fs-root',
            'type': 'format',
            'fstype': 'ext4',
            'volume': 'lv-root',
        })

        # Mount root
        storage['config'].append({
            'type': 'mount',
            'id': 'mount-root',
            'device': 'fs-root',
            'path': '/',
        })

    else:
        # No LVM
        storage['config'].append({
            'id': 'fs-root',
            'type': 'format',
            'fstype': 'ext4',
            'volume': volume_id,
        })
        storage['config'].append({
            'type': 'mount',
            'id': 'mount-root',
            'device': 'fs-root',
            'path': '/',
        })

    return storage

def write_yaml_file(data, filename='storage-config.yaml'):
    with open(filename, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"\nCurtin storage configuration written to '{filename}'.")

if __name__ == "__main__":
    config = build_storage_config()
    write_yaml_file(config)

