"""
This module is part of the Clemson ACM Auto Grader

This module is responsible for testing the cleanup functionality
"""

import os
import shutil
import subprocess
import unittest
from unittest import mock

from autograder.source import clean

VALID = {
    "./": True,
    "test.in": 'testing 123\n',
    "test2.in": 'testing 456\n',
    "test/test3.in": "testing 789\n",
    "test": True
}

class CleanTests(unittest.TestCase):
    """
    Tests that verify that cleans occur as expected
    """
    def setUp(self):
        self.student = {
            'username': 'test',
            'directory': 'test/scratch'
            }

        self.settings = {
            'clean': {
                'timeout': 5,
                'git': {'force': False}
            },
            'project': {'name': 'testproject'}
        }

    def tearDown(self):
        if os.path.exists('test'):
            shutil.rmtree('test')


    def test_git(self):
        """
        Test cleaning up git repos
        """
        directory = self.student['directory']
        clean_git(directory)
        self._valid_state(directory, VALID)
        make_changes(directory)
        clean.clean_git(self.settings, self.student)
        self._valid_state(directory, VALID)

    def test_git_force(self):
        """
        Test cleaning up git repos using force option
        """
        self.settings['clean']['git']['force'] = True
        directory = self.student['directory']
        clean_git(directory)
        self._valid_state(directory, VALID)
        make_changes(directory)
        clean.clean_git(self.settings, self.student)
        self._valid_state(directory, VALID)


    def test_hg(self):
        """
        Test cleaning up hg repos
        """
        directory = self.student['directory']
        clean_hg(directory)
        self._valid_state(directory, VALID)
        make_changes(directory)
        clean.clean_hg(self.settings, self.student)
        self._valid_state(directory, VALID)

    def test_noop(self):
        """
        Test cleaning up with a noop
        """
        self.assertTrue(clean.clean_noop(self.settings, self.student))


    def test_svn(self):
        """
        Test cleaning up svn repos
        """
        directory = self.student['directory']
        clean_svn(directory)
        self._valid_state(directory, VALID)
        make_changes(directory)
        clean.clean_svn(self.settings, self.student)
        self._valid_state(directory, VALID)

    @mock.patch('autograder.source.clean.subprocess.check_call')
    def test_script(self, mock_check_call):
        """
        Test cleaning up with a script
        """
        self.settings['clean']['command'] = 'date'
        clean.clean_script(self.settings, self.student)
        mock_check_call.assert_called_with('date', stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL, shell=True, timeout=5,
                                           cwd=self.student['directory'])

    def _valid_state(self, directory, valid):
        """
        checks that only the files and directories in the valid state exist

        str directory - path to check for the files that should exist
        dict(names,content) valid  - path to check for the files that should exist
            str names - the names of the expected files
            content - a bool True if it should be a dir
                    - a string containing its contents if it should be a file
        """
        valid = {os.path.abspath(os.path.join(directory, i)):valid[i] for i in valid}
        for path in valid:
            with self.subTest(i=path):
                self.assertTrue(os.path.exists(os.path.abspath(path)))
        for path, dirs, files in os.walk(directory):
            _remove_vcs_dirs(dirs)
            self.assertIn(os.path.abspath(path), valid)
            self.assertEqual(True, valid[os.path.abspath(path)])
            self._assert_files_valid(os.path.abspath(path), files, valid)

    def _assert_files_valid(self, path, files, valid):
        """
        ensure that all files are expected
        """
        for filename in files:
            filepath = os.path.join(path, filename)
            self.assertIn(filepath, valid)
            with open(filepath) as file_contents:
                self.assertEqual(valid[filepath], file_contents.read())
        return False


def _remove_vcs_dirs(dirs):
    """
    removes vcs directories from the walk
    """
    if '.git' in dirs:
        dirs.remove('.git')
    if '.hg' in dirs:
        dirs.remove('.hg')
    if '.svn' in dirs:
        dirs.remove('.svn')

def clean_hg(directory):
    """
    Setup the directory for hg tests
    """
    subprocess.check_call(["./scripts/repo_util.sh", "setup_hg", directory],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_git(directory):
    """
    Setup the directory for hg tests
    """
    subprocess.check_call(["./scripts/repo_util.sh", "setup_git", directory],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def clean_svn(directory):
    """
    Setup the directory for hg tests
    """
    subprocess.check_call(["./scripts/repo_util.sh", "setup_svn", directory],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def make_changes(directory):
    """
    Make changes that should be cleaned during clean
    """
    subprocess.check_call(["./scripts/repo_util.sh", "change_files", directory],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


