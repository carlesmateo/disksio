#
# DriveUtils Class
#
# Author: Carles Mateo
# Creation Date: 2017-04-23
# Description: Class to deal with Disks (Disk objects)
#

from .file import File
from .disk import Disk


class DriveUtils:

    o_file = File()

    def __init__(self, o_file=File()):
        self.o_file = o_file

    def get_all_disks(self):
        """ Get all the available disks """
        all_disks = []
        i_error_code = 0

        # get all attached disks by id
        s_path = "/dev/disk/by-id"
        b_success, a_disk_ids = self.o_file.list_dir(s_path)
        if b_success is False:
            return 1, all_disks

        for s_disk_id in a_disk_ids:
            if "part" in s_disk_id:
                continue

            if "wwn" in s_disk_id or "VBOX" in s_disk_id or "nvme" in s_disk_id \
                    or ("ata-" in s_disk_id):
                # get the device name
                b_success, s_dev_name = self.o_file.get_real_path(s_path + "/" + s_disk_id)
                s_dev_name = s_dev_name.replace("/dev/", "")
                # check its an sd device or an NVMe
                if ("sd" not in s_dev_name) and ("nvme" not in s_dev_name):
                    continue
                # make sure a disk with both wwn and ata is not added twice
                # Or if wrong zoning show them as duplicates
                if s_dev_name in [disk.s_dev_name for disk in all_disks]:
                    continue
                new_disk = Disk(s_dev_name, self.o_file)
                new_disk.id = s_disk_id

                i_info_error_code = self.get_disk_info(new_disk)
                if i_info_error_code != 0:
                    new_disk.suspect = True
                all_disks.append(new_disk)

        # get all attached disks if not found by id (for virtualbox)
        b_success, s_output = self.o_file.read("/proc/partitions")
        if b_success is True:
            output_lines = s_output.split("\n")
            for line in output_lines:

                if "major minor" in line:
                    continue
                elif len(line) == 0 or len(line) < 4:
                    continue
                s_drive_dev_name = line.split()[3]
                if any(char.isdigit() for char in s_drive_dev_name):
                    continue
                if s_drive_dev_name not in [drive.s_dev_name for drive in all_disks]:
                    new_disk = Disk(s_drive_dev_name, self.o_file)
                    new_disk.id = "n/a"
        else:
            i_error_code = 1

        return i_error_code, all_disks

    def get_disk_info(self, disk, b_cmdline=False):
        """
        Gets information for the disk including ioc, logical/physical sector and drive information from smartctl.
        :param disk: The disk to get the information for
        :type disk: Disk
        :param b_cmdline:
        :return: Returns an error code indicating the success of the command. O indicates everything is ok.
        :rtype int
        """
        i_error_code = 0
        i_ioc_error_code, s_output = self.get_ioc_info_for_drive_from_system(disk.s_dev_name)
        if i_ioc_error_code == 0:
            if 'platform' in s_output:  # The drive is a Zvol so skip it
                return None

            disk.ioc = self.parse_ioc_info(s_output)
        else:
            i_error_code = i_ioc_error_code


        self.get_disk_info_from_sys_fs(disk)

        # get physical and logical block size
        disk.s_logical_block_size = self.get_logical_block_size(disk.s_dev_name)
        disk.s_physical_block_size = self.get_physical_block_size(disk.s_dev_name)

        # check for partition 3
        if self.o_file.file_exists("/sys/block/" + disk.s_dev_name + "/" + disk.s_dev_name + "3"):
            disk.has_partition3 = True
        else:
            disk.has_partition3 = False

        return i_error_code

    def get_disk_info_from_sys_fs(self, disk):
        """
        Load the information for a disk from sysfs
        :param disk: The disk to load the information for
        :type disk: Disk
        :return: None
        """
        s_drive_path = "/sys/class/block/" + disk.s_dev_name
        # get disk size
        b_success, s_size = self.o_file.read(s_drive_path + "/size")
        s_size = s_size.strip()
        if b_success is True:
            i_size_in_tb = float(s_size)*512/1000/1000/1000/1000  # Dividing by 1000 for human readable
            if i_size_in_tb > 1:
                if i_size_in_tb > 10:
                    disk.size = "%.1f" % i_size_in_tb + "TB"
                else:
                    disk.size = "%.2f" % i_size_in_tb + "TB"
            else:
                i_size_in_gb = float(s_size)*512/1000/1000/1000  # Dividing by 1000 for human readable
                if i_size_in_gb > 100:
                    disk.size = "%.0f" % i_size_in_gb + "GB"
                elif i_size_in_gb > 10:
                    disk.size = "%.0f" % i_size_in_gb + "GB"
                else:
                    disk.size = "%.2f" % i_size_in_gb + "GB"
            disk.byte_size = int(s_size)/2*1024

        # get the vendor
        b_success, s_vendor = self.o_file.read(s_drive_path + "/device/vendor")
        if b_success is True:
            disk.manufacturer = s_vendor

        # get the type - spinning or solid state
        b_success, s_type_value = self.o_file.read(s_drive_path + "/queue/rotational")
        if b_success is True:
            if s_type_value.strip() == "0" or s_type_value == 0:
                disk.type = "Solid State"
            else:
                disk.type = "Spinning"

        # get serial number
        s_serial = ""
        s_file_serial = s_drive_path + "/device/vpd_pg80"
        if self.o_file.file_exists(s_file_serial) is True:
            b_success, a_serial = self.o_file.read_binary(s_file_serial)
            if b_success is True:
                for i_char in a_serial:
                    if i_char > 40 and i_char < 123:
                        s_serial += chr(i_char)
                disk.s_serial = s_serial
            else:
                disk.s_serial = ""
                print("Error reading: " + s_file_serial)
        else:
            disk.s_serial = ""

        # check drive is readable
        b_success, s_serial = self.o_file.read(s_drive_path + "/stat")
        b_readable = False
        if b_success is True:
            for s_part in s_serial.split():
                if s_part != "0":
                    b_readable = True
                    break

        if b_readable is False:
            disk.status = Disk.STATUS_FAILURE
            disk.b_unreadable = True

    def get_ioc_info_for_drive_from_system(self, s_disk_name):
        # get the host (ioc)
        i_error_code = 0

        if self.o_file.path_exists("/sys/block/" + s_disk_name):
            b_success, s_ioc_info_path = self.o_file.get_real_path("/sys/block/" + s_disk_name)

            if s_disk_name not in s_ioc_info_path:
                i_error_code = 1
        else:
            s_ioc_info_path = ""
            i_error_code = 2

        return i_error_code, s_ioc_info_path

    def parse_ioc_info(self, s_output):
        ioc = "-"
        if 'host' in s_output and 'expander' in s_output:
            ioc = s_output.split('/')[6][4:]
        return ioc

    def get_logical_block_size(self, s_disk_name):
        b_success, s_logical_block = self.o_file.read("/sys/class/block/" + s_disk_name + "/queue/logical_block_size")
        if b_success is True:
            return s_logical_block.strip()
        return "n/a"

    def get_physical_block_size(self, s_disk_name):
        b_success, s_physical_block = self.o_file.read("/sys/class/block/" + s_disk_name + "/queue/physical_block_size")
        if b_success is True:
            return s_physical_block.strip()
        return "n/a"
