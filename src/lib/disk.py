#
# Disk Class
#
# Author: Carles Mateo
# Creation Date: 2017-04-23
# Description: Class for a Disk
#

from .file import File


class Disk:

    # Strings identifying the STATUS of the drives. Do not modify the Strings as they are used for comparisons.
    STATUS_ONLINE = "ONLINE"
    STATUS_OFFLINE = "OFFLINE"
    STATUS_FAULTED = "FAULTED"
    STATUS_UNAVAIL = "UNAVAIL"
    STATUS_DEGRADED = "DEGRADED"
    STATUS_REMOVED = "REMOVED"
    STATUS_BUILDING = "BUILDING"
    STATUS_CHECKSUM = "CHECKSUM"
    STATUS_FAILURE = "FAILURE"

    LIGHT_FAULT = "fault"
    LIGHT_LOCATE = "locate"

    o_file = File()
    s_dev_name = ""
    s_id = ""
    s_serial = ""
    s_slot = ""
    s_drive_status = ""
    s_power_status = ""
    s_fault = ""
    s_locate = ""
    s_size = ""
    s_logical_block_size = ""
    s_physical_block_size = ""

    def __init__(self, s_dev_name, o_file=File()):
        self.s_dev_name = s_dev_name
        self.o_file = o_file

    def get_device_info(self):
        path = "/sys/block/" + self.s_dev_name + "/device/"

        # get files in device directory
        b_success, device_files = self.o_file.list_dir(path)
        for filename in device_files:
            if "enclosure_device" in filename:
                path += filename + "/"
                break

        if "enclosure" not in path:
            return

        b_success, s_slot = self.o_file.read(path + "slot")
        if b_success is True:
            self.s_slot = s_slot.strip()
        b_success, s_drive_status = self.o_file.read(path + "status")
        if b_success is True:
            self.s_drive_status = s_drive_status.strip()
        b_success, s_power_status = self.o_file.read(path + "power_status")
        if b_success is True:
            self.s_power_status = s_power_status.strip()
        b_success, s_fault = self.o_file.read(path + "fault")
        if b_success is True:
            self.s_fault = s_fault.strip()
        b_success, s_locate = self.o_file.read(path + "locate")
        if b_success is True:
            self.s_locate = s_locate.strip()

    def get_drive_info(self):
        """
        Returns the information of the drive
        :rtype: string
        :return: s_name
        :rtype: string
        :return: s_id
        :rtype: string
        :return: s_serial
        :rtype: string
        :return: s_slot
        :rtype: string
        :return: s_size
        """
        s_dev_name = self.s_dev_name
        s_id = self.s_id
        s_serial = self.s_serial
        s_slot = self.s_slot
        s_size = self.s_size
        s_logical_block_size = self.s_logical_block_size
        s_physical_block_size = self.s_physical_block_size

        return s_dev_name, s_id, s_serial, s_slot, s_size, s_logical_block_size, s_physical_block_size
