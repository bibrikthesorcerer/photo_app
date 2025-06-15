import tempfile
import shutil
from django.test import override_settings
from rest_framework.test import APITestCase


class TempDirectoryAPITestCase(APITestCase):    
    @classmethod
    def setUpClass(cls):
        ''' 
        Hook method for setting up class fixture before running tests in the class.  
        Changes `MEDIA_ROOT` to a temporary directory which will be erased in `tearDownClass`.  
        '''
        cls.test_media = tempfile.mkdtemp() # create tempdir
        cls._media_override = override_settings(MEDIA_ROOT=cls.test_media) # init context manager with overriden dir
        cls._media_override.enable() # enable context manager
        super().setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        '''
        Hook method for deconstructing the class fixture after running all tests in the class.  
        Erases temporary directory which is `MEDIA_ROOT` for this test. 
        '''
        super().tearDownClass() # delete fixtures
        shutil.rmtree(cls.test_media, ignore_errors=True) # clear tempdir
        cls._media_override.disable() # disable context