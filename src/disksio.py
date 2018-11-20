#
# disksio
# Author: Carles Mateo
# Description: IO operations for Disks

from lib.driveutils import DriveUtils
from lib.file import File


def main():
    o_file = File()
    o_driveutils = DriveUtils(o_file)

    i_error_code, l_disks = o_driveutils.get_all_disks()

    # Please Note: Serial works in Python2 but not un Python3
    if i_error_code == 0:
        for o_disk in l_disks:
            s_dev_name, s_id, s_serial, s_slot, s_size, s_logical_block_size, s_physical_block_size = o_disk.get_drive_info()
            s_line = "Device: " + s_dev_name + " Id: " + s_id + " Serial: " + s_serial + " Slot: " + s_slot + \
                     "Size: " + s_size + "Physical/Logical: " + s_physical_block_size + "/" + s_logical_block_size
            print(s_line)
    else:
        print("Error reading the drives")


if __name__ == "__main__":
    # execute only if run as a script
    main()
