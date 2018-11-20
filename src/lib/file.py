#
# File utilities
#
# Author: Carles Mateo
# Creation Date: 2017-04-23
# Description: Class to deal with File Read, Write...
#              Please try to keep it lightweight and without other library dependencies as it is injected as Dependency.
#
import os
import glob


class File:

    def __init__(self):
        pass

    def write(self, s_file, s_text):
        """
        This method creates or overwrites a text file
        :param s_file: The file path for the file to delete
        :type s_file: str
        :param s_text: Text to add
        :type s_text: str
        :return: Indicate success of deletion
        :rtype boolean
        """
        try:
            fh = open(s_file, "w")
            fh.write(s_text)
            fh.close()

        except:
            return False

        return True

    def append(self, s_file, s_text):
        """
        This method creates or appends to a file
        :param s_file: The file path for the file to delete
        :type s_file: str
        :param s_text: Text to add
        :type s_text: str
        :return: Indicate success of deletion
        :rtype boolean
        """
        try:
            fh = open(s_file, "a")
            fh.write(s_text)
            fh.close()

        except:
            return False

        return True

    def read(self, s_file):
        """
        This method reads the file in text format.
        Note: Python3 will try to UTF-8 Decode and return "UnicodeDecodeError: 'utf-8' codec can't decode byte"
        :param s_file: The file path for the file to read
        :type s_file: str
        :return: b_result: Indicate success reading
        :rtype boolean
        :return: s_result: The text
        :rtype str
        """
        s_result = ""
        b_success = True

        try:
            fh = open(s_file, "r")
            s_result = fh.read()
            fh.close()

        except:
            b_success = False

        return b_success, s_result

    def read_binary(self, s_file):
        """
        This method reads the file in binary format
        :param s_file: The file path for the file to read
        :type s_file: str
        :return: Indicate success reading
        :rtype boolean
        :return: a_result: byte array
        :rtype byte_array
        """
        a_result = []
        b_success = True

        try:
            fh = open(s_file, "rb")
            a_result = fh.read()
            fh.close()

        except:
            b_success = False

        # For python2
        a_result = bytearray(a_result)

        return b_success, a_result

    def readlines(self, s_file):
        """
        Read a file and return its contents as an array of lines
        :param s_file: The file to read
        :type s_file: str
        :return: A list with each line of the file as strings
        """
        a_result = []
        b_success = True

        try:
            fh = open(s_file, "r")
            a_result = fh.readlines()
            fh.close()

        except:
            b_success = False

        return b_success, a_result

    def delete(self, s_file):
        """
        This method deletes a given file
        :param s_file: The file path for the file to delete
        :type s_file: str
        :return: Indicate success of deletion
        :rtype boolean
        """

        b_success = True
        try:
            if os.path.exists(s_file):
                os.remove(s_file)
            else:
                b_success = False
        except IOError:
            b_success = False

        return b_success

    def delete_all_with_mask(self, s_mask):
        """
        This method deletes all files matching a given mask. Example mask: '/root/file*.txt'. This mask will delete any
        file in the root directory, starting with 'file' and ending with '.txt'.
        :param s_mask: The mask to use for deletion. Should contain entire file path.
        :type s_mask: str
        :return: Indicate success of deletion
        :rtype boolean
        :return: Number of files successfully deleted
        :rtype integer

        """
        b_success = True
        i_files_deleted = 0
        try:
            for o_file in glob.glob(s_mask):
                os.remove(o_file)
                i_files_deleted = i_files_deleted + 1
        except IOError:
            b_success = False

        return b_success, i_files_deleted

    def get_all_with_mask(self, s_mask):
        """
        Get all files matching a given mask. Example mask: '/root/file*.txt'. This mask will return any file in the
        root directory, starting with 'file' and ending with '.txt'.
        :param s_mask: The mask to use for gathering the files. Should contain entire file path.
        :type s_mask: str
        :return: A boolean indicating success, A list of files matching the mask
        :rtype boolean, list
        """
        l_files = []
        b_success = True
        try:
            for o_file in glob.glob(s_mask):
                l_files.append(o_file)
        except IOError:
            b_success = False

        return b_success, l_files

    def folder_exists(self, s_folder):
        """
        Checks if a folder exists
        :param s_folder:
        :return: boolean
        """

        try:
            b_exists = os.path.isdir(s_folder)
        except IOError:
            b_exists = False
        except OSError:
            b_exists = False

        return b_exists

    def file_exists(self, s_file):
        """
        Check if a file exists
        :param s_file: The file to check
        :return: boolean indicating success
        """
        try:
            b_exists = os.path.isfile(s_file)
        except IOError:
            b_exists = False
        except OSError:
            b_exists = False

        return b_exists

    def path_exists(self, s_file_path):
        """
        Check if a file path exists
        :param s_file: The file path to check
        :return: boolean indicating success
        """
        try:
            b_exists = os.path.exists(s_file_path)
        except IOError:
            b_exists = False
        except OSError:
            b_exists = False

        return b_exists

    def create_folder(self, s_folder):
        """
        Creates a folder
        :param s_folder:
        :return: boolean
        """

        b_success = True
        try:
            os.makedirs(s_folder)
        except IOError:
            b_success = False
        except OSError:
            b_success = False

        return b_success

    def remove_folder(self, s_folder):
        """
        Remove a folder
        :param s_folder: The folder to remove
        :return: A boolean indicating success
        """
        b_success = True
        try:
            os.removedirs(s_folder)
        except IOError:
            b_success = False
        except OSError:
            b_success = False

        return b_success

    def list_dir(self, s_dir):
        """
        Get the contents of a directory and return them as a list
        :param s_dir: The directory to list
        :return: A boolean indicating success, A list of the contents
        """
        b_success = True
        a_files = []
        try:
            a_files = os.listdir(s_dir)
        except IOError:
            b_success = False
        except OSError:
            b_success = False

        return b_success, a_files

    def rename_file(self, s_old_file, s_new_file):
        """
        Rename a file to a new name
        :param s_old_file: The old file name
        :param s_new_file: The new file name
        :return: A boolean indicating success
        """
        try:
            os.rename(s_old_file, s_new_file)
            b_success = self.file_exists(s_new_file)
        except IOError:
            b_success = False
        except OSError:
            b_success = False

        return b_success

    def get_real_path(self, s_file):
        """
        Get the canonical path(removes symbolic links) for a specified file
        :param s_file: The file to get the path for
        :return: A boolean indicating success, A string of the real path
        """
        s_path = ""
        try:
            s_path = os.path.realpath(s_file)
            if self.file_exists(s_file):
                b_success = True
            else:
                b_success = False
        except IOError:
            b_success = False
        except OSError:
            b_success = False

        return b_success, s_path
