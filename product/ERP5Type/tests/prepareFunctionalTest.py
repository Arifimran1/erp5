##############################################################################
#
# Copyright (c) 2007 Nexedi SARL and Contributors. All Rights Reserved.
#                     Kazuhiko <kazuhiko@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import os
import unittest

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase

from Products.ERP5Type.tests.runFunctionalTest import (
    FunctionalTestRunner as FunctionalTestRunnerBase
)

class FunctionalTestRunner(FunctionalTestRunnerBase):

  def __init__(self, host, port):
    FunctionalTestRunnerBase.__init__(self, os.environ['INSTANCE_HOME'])
    # local overrides
    self.host = host
    self.port = int(port)
  
os.environ['erp5_tests_portal_id'] = 'erp5_portal'

class TestZelenium(ERP5TypeTestCase):
    def getBusinessTemplateList(self):
        """
          Return the list of business templates.
        """
        return ('erp5_base', 'erp5_ui_test_core', 'erp5_ui_test', 'erp5_forge',
                'erp5_knowledge_pad',
                'erp5_knowledge_pad_ui_test',
                'erp5_trade', 'erp5_pdm', 'erp5_ooo_import',
                'erp5_accounting', 'erp5_invoicing',
                'erp5_simplified_invoicing', 'erp5_project',
                'erp5_accounting_ui_test',
                'erp5_pdm_ui_test',
                'erp5_trade_ui_test',
                'erp5_project_ui_test',
                'erp5_ingestion', 'erp5_ingestion_mysql_innodb_catalog',
                'erp5_web', 'erp5_dms', 'erp5_dms_ui_test',
                'erp5_km', 'erp5_km_ui_test',
                # erp5_web_ui_test must run at the last, because it logs out
                # manager user and continue other tests as a user created in
                # that test.
                'erp5_web_ui_test',
                )

    def testFunctional(self):
      # first of all, abort to get rid of the mysql participation inn this
      # transaction
      self.portal._p_jar.sync()
      self.runner = FunctionalTestRunner(self.serverhost, self.serverport)
      # XXX weak parsing of arguments, avoid spaces in argument values:
      runner_arguments = os.environ.get('erp5_functional_test_arguments',
                                        '').split()
      self.runner.parseArgs(runner_arguments)
      self.logMessage('starting functional test runner with arguments: %s' %
                      runner_arguments)
      self.runner.main()
      self.runner.sendResult()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestZelenium))
    return suite
