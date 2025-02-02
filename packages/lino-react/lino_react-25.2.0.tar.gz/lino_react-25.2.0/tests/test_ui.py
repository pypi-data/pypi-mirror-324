import os
import signal
import sys
from pathlib import Path
from subprocess import Popen, PIPE, DEVNULL
from lino.utils.pythontest import TestCase

SERVER_URL = "localhost:8787"


class UITests(TestCase):

    def setUp(self):
        super().setUp()
        self.server_process = Popen([
            sys.executable,
            str(Path(__file__).parent.parent / 'puppeteers' / 'noi' / 'manage.py'),
            'runserver',
            SERVER_URL
        ], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, start_new_session=True)

    def test_ui(self):
        print("="*80)
        print(self.server_process.pid)
        print("="*80)

    def tearDown(self):
        os.kill(self.server_process.pid, signal.SIGKILL)
        super().tearDown()
