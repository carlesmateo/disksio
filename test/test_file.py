#
# Tests for File class
#
# Author: Carles Mateo
# Creation Date: 2017-04-23
#

import pytest
import os
from ..src.lib.file import File


class TestFile(object):

    s_path_test_file = "/tmp/test_file.txt"

    def create_sample_file(self):
        """
        It creates a sample file
        :return:
        """
        o_file = File()

        b_success = o_file.write(self.s_path_test_file, "For testing purposes")


    # Start Tests
    def test_write_ok(self):
        o_file = File()
        b_result = o_file.write("/tmp/test_file.txt", "Test from test_file.txt")

        assert b_result is True

    def test_write_ko(self):
        o_file = File()
        b_result = o_file.write("/not_existing/test_file.txt", "Test from test_file.txt")

        assert b_result is False

    def test_append_ok(self):
        o_file = File()
        b_result = o_file.append("/tmp/test_file.txt", "Test from test_file.txt")

        assert b_result is True

    def test_append_ko(self):
        o_file = File()
        b_result = o_file.append("/not_existing/test_file.txt", "Test from test_file.txt")

        assert b_result is False

    def test_read_ok(self):
        o_file = File()
        b_result, s_text = o_file.read("/tmp/test_file.txt")

        assert b_result is True

    def test_read_ko(self):
        o_file = File()
        b_result, s_text = o_file.read("/not_existing/test_file.txt")

        assert b_result is False

    def test_delete_ko(self):
        o_file = File()
        b_result = o_file.delete("/not_existing/test_file.txt")

        assert b_result is False

    def test_delete_ok(self):
        self.create_sample_file()

        o_file = File()

        b_result = o_file.delete(self.s_path_test_file)

        assert b_result is True

    def test_delete_with_mask(self):
        self.create_sample_file()

        o_file = File()
        b_success, i_files_deleted = o_file.delete_all_with_mask(self.s_path_test_file)

        assert b_success is True
        assert i_files_deleted == 1

    def test_folder_exists(self):
        s_path_folder = "/tmp/"

        o_file = File()

        b_result = o_file.folder_exists(s_path_folder)
        assert b_result is True

        s_path_folder = "/tmp"
        b_result = o_file.folder_exists(s_path_folder)
        assert b_result is True

        s_path_folder = "/this-has-to-fail"
        b_result = o_file.folder_exists(s_path_folder)
        assert b_result is False

    def test_file_exists(self):
        s_path_file = "/tmp/not_real_file.txt"

        o_file = File()

        b_result = o_file.file_exists(s_path_file)
        assert b_result is False

        # create file to test for existing file
        o_file.write("/tmp/test_file.txt", "File for testing")

        s_path_file = "/tmp/test_file.txt"
        b_result = o_file.file_exists(s_path_file)
        assert b_result is True

        # Clean up the file
        o_file.delete("/tmp/test_file.txt")

    def test_create_folder(self):
        s_path_folder = "/tmp/test"

        o_file = File()

        b_result = o_file.create_folder(s_path_folder)
        assert b_result is True

        b_result = o_file.remove_folder(s_path_folder)
        assert b_result is True

        s_path_folder = "///this-should-give-exception-catched"
        b_result = o_file.create_folder(s_path_folder)
        assert b_result is False

    def test_path_exists(self):
        s_path = "/tmp"

        o_file = File()

        b_result = o_file.path_exists(s_path)
        assert b_result is True

        # test with file
        s_path = s_path + "/file.txt"
        o_file.write(s_path, "File for testing")

        b_result = o_file.path_exists(s_path)
        assert b_result is True

        # test with bad path
        s_path = "/idontexist"
        b_result = o_file.path_exists(s_path)
        assert b_result is False

    def test_list_dir(self):
        s_path = "/tmp"

        o_file = File()

        # create a file for the test
        filename = "testfile"
        o_file.write(s_path + "/" + filename, "File for testing")

        b_success, a_files = o_file.list_dir(s_path)

        assert b_success is True
        assert filename in a_files

        # test with bad path
        s_path = "/idontexist"

        b_success, a_files = o_file.list_dir(s_path)
        assert b_success is False
        assert len(a_files) == 0

    def test_get_real_path(self):
        s_path = "/tmp"

        o_file = File()

        # create a file for the test
        filename = s_path + "/testfile"
        o_file.write(s_path + "/" + filename, "File for testing")

        # create a symbolic link
        s_sym_link = s_path + "/testsymlink"
        if not o_file.path_exists(s_sym_link):
            os.symlink(filename, s_sym_link)

        b_success, s_real_path = o_file.get_real_path(s_sym_link)
        assert b_success is True
        assert s_real_path == filename

        # try with non symlink path
        b_success, s_real_path = o_file.get_real_path(filename)
        assert b_success is True
        assert s_real_path == filename

        # try with bad path
        b_success, s_real_path = o_file.get_real_path("/tmp/idontexist")
        assert b_success is False

    def test_get_all_with_mask(self):
        o_file = File()

        s_mask = "/etc/*nam*"

        b_success, l_files = o_file.get_all_with_mask(s_mask)

        assert b_success is True
        assert len(l_files) > 0
