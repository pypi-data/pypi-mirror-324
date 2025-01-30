# coding: utf-8

"""
    PhrameAPI

    Phrame API  # noqa: E501

    The version of the OpenAPI document: 1.0.2
    Contact: david@3adesign.co.uk
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import PhrameAPI
from PhrameAPI.models.db_phrame_ui_configuration import DbPhrameUIConfiguration  # noqa: E501
from PhrameAPI.rest import ApiException

class TestDbPhrameUIConfiguration(unittest.TestCase):
    """DbPhrameUIConfiguration unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DbPhrameUIConfiguration
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = PhrameAPI.models.db_phrame_ui_configuration.DbPhrameUIConfiguration()  # noqa: E501
        if include_optional :
            return DbPhrameUIConfiguration(
                id = 'bf325375-e030-4fcc-aa00-917317c5747701234567891011121314151617181920212223242526272829303132333435', 
                left = 56, 
                top = 56, 
                width = 56, 
                height = 56, 
                type = '', 
                z_order = 56, 
                stream_id = '', 
                stream_suffix = '', 
                button_label = '', 
                group_id = ''
            )
        else :
            return DbPhrameUIConfiguration(
        )

    def testDbPhrameUIConfiguration(self):
        """Test DbPhrameUIConfiguration"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
