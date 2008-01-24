##############################################################################
#
# Copyright (c) 2007 Nexedi SARL and Contributors. All Rights Reserved.
#          Fabien Morin <fabien.morin@gmail.com>
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################
"""
  Tests paysheet creation using paysheet model.

TODO:
  - review naming of new methods
  - in the test test_04_paySheetCalculation, add sub_object (annotation_line, 
  ratio_line and payment conditioni), and verify that before the script 
  'PaySheetTransaction_applyModel' is called, subobjects are not in the 
  paysheet, and after that there are copied in.
  - use ratio settings and test it (there is a method getRatioQuantityList, see
  the file Document/PaySheetTransaction.py)
  - test with bonus which participate on the base_salary and see if the 
  contribution are applied on the real base_salary or on the base_salary + bonus
  (it should).

WARNING: 
  - current API naming may change although model should be stable.

"""

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from Testing import ZopeTestCase
from DateTime import DateTime
from Acquisition import aq_parent

class TestPayrollMixin(ERP5TypeTestCase):

  paysheet_model_portal_type        = 'Pay Sheet Model'
  paysheet_model_line_portal_type   = 'Pay Sheet Model Line'
  paysheet_transaction_portal_type  = 'Pay Sheet Transaction'
  paysheet_line_portal_type         = 'Pay Sheet Line'
  payroll_service_portal_type       = 'Payroll Service'
  currency_portal_type              = 'Currency'
  person_portal_type                = 'Person'
  organisation_portal_type          = 'Organisation'


  default_region                    = 'europe/west/france'
  france_settings_forfait           = 'france/forfait'
  france_settings_slice_a           = 'france/tranche_a'
  france_settings_slice_b           = 'france/tranche_b'
  france_settings_slice_c           = 'france/tranche_c'
  tax_category_employer_share       = 'employer_share'
  tax_category_employee_share       = 'employee_share'
  base_amount_deductible_tax        = 'deductible_tax'
  base_amount_non_deductible_tax    = 'deductible_tax'
  base_amount_bonus                 = 'bonus'
  base_amount_base_salary           = 'base_salary'
  grade_worker                      = 'worker'
  grade_engineer                    = 'engineer'

  plafond = 2682.0

  model = None
  model_id                          = 'model_one'
  model_title                       = 'Model One'
  person_id                         = 'one'
  person_title                      = 'One'
  person_career_grade               = 'worker'
  organisation_id                   = 'company_one'
  organisation_title                = 'Company One'
  variation_settings_category_list  = ['salary_range/france',]
  price_currency                    = 'currency_module/EUR'

  def getTitle(self):
    return "Payroll"

  def afterSetUp(self):
    """Prepare the test."""
    self.portal = self.getPortal()
    self.organisation_module = self.portal.organisation_module
    self.person_module = self.portal.person_module
    self.payroll_service_module = self.portal.payroll_service_module
    self.paysheet_model_module = self.portal.paysheet_model_module 
    self.createCategories()
    self.createCurrencies()

    self.model = self.createModel(self.model_id, self.model_title, 
        self.person_id, self.person_title, self.person_career_grade, 
        self.organisation_id, self.organisation_title, 
        self.variation_settings_category_list, self.price_currency)

    self.login()

    # creation of payroll services
    self.urssaf_id = 'sickness_insurance'
    self.labour_id = 'labour'

    self.urssaf_slice_list = ['salary_range/'+self.france_settings_slice_a, 
                              'salary_range/'+self.france_settings_slice_b, 
                              'salary_range/'+self.france_settings_slice_c]

    self.urssaf_share_list = ['tax_category/'+self.tax_category_employee_share,
                              'tax_category/'+self.tax_category_employer_share]

    self.salary_slice_list = ['salary_range/'+self.france_settings_forfait,]
    self.salary_share_list = ['tax_category/'+self.tax_category_employee_share,]


    payroll_service_organisation = self.createOrganisation(id='urssaf', 
        title='URSSAF')
    self.urssaf=self.createPayrollService(id=self.urssaf_id, 
        organisation=payroll_service_organisation, 
        base_amount_list=['deductible_tax',],
        variation_base_category_list=['tax_category', 'salary_range'],
        variation_category_list=self.urssaf_slice_list + \
                                self.urssaf_share_list)

    self.labour=self.createPayrollService(id=self.labour_id, 
        organisation=None, 
        base_amount_list=['base_salary', 'gross_salary'],
        variation_base_category_list=['tax_category', 'salary_range'],
        variation_category_list=self.salary_slice_list +\
                                self.salary_share_list)

  def _safeTic(self):
    """Like tic, but swallowing errors, usefull for teardown"""
    try:
      get_transaction().commit()
      self.tic()
    except RuntimeError:
      pass

  def beforeTearDown(self):
    """Clear everything for next test."""
    self._safeTic()
    for module in [ 'organisation_module',
                    'person_module',
                    'currency_module',
                    'payroll_service_module',
                    'paysheet_model_module',
                    'accounting_module']:
      folder = getattr(self.getPortal(), module, None)
      if folder:
        [x.unindexObject() for x in folder.objectValues()]
        self._safeTic()
        folder.manage_delObjects([x.getId() for x in folder.objectValues()])
    self._safeTic()
    # cancel remaining messages
    activity_tool = self.getPortal().portal_activities
    for message in activity_tool.getMessageList():
      activity_tool.manageCancel(message.object_path, message.method_id)
      ZopeTestCase._print('\nCancelling active message %s.%s()\n'
                          % (message.object_path, message.method_id) )
    get_transaction().commit()

  def login(self, quiet=0, run=1):
    uf = self.getPortal().acl_users
    uf._doAddUser('admin', 'admin', ['Manager', 'Assignee', 'Assignor',
                               'Associate', 'Auditor', 'Author'], [])
    user = uf.getUserById('admin').__of__(uf)
    newSecurityManager(None, user)

  def createCategories(self):
    """Create the categories for our test. """
    # create categories
    for cat_string in self.getNeededCategoryList() :
      base_cat = cat_string.split("/")[0]
      # if base_cat not exist, create it
      if getattr(self.getPortal().portal_categories, base_cat, None) == None:
        self.getPortal().portal_categories.newContent(\
                                          portal_type='Base Category',
                                          id=base_cat)
        get_transaction().commit()
        self.tic()
      path = self.getPortal().portal_categories[base_cat]
      for cat in cat_string.split("/")[1:] :
        if not cat in path.objectIds() :
          path = path.newContent(
                    portal_type='Category',
                    id=cat,
                    title=cat.replace('_', ' ').title(),)
        else:
          path = path[cat]
    get_transaction().commit()
    self.tic()
    # check categories have been created
    for cat_string in self.getNeededCategoryList() :
      self.assertNotEquals(None,
                self.getCategoryTool().restrictedTraverse(cat_string),
                cat_string)

  def getNeededCategoryList(self):
    """return a list of categories that should be created."""
    return ('region/%s' % self.default_region,
            'salary_range/%s' % self.france_settings_forfait,
            'salary_range/%s' % self.france_settings_slice_a,
            'salary_range/%s' % self.france_settings_slice_b,
            'salary_range/%s' % self.france_settings_slice_c,
            'tax_category/%s' % self.tax_category_employer_share,
            'tax_category/%s' % self.tax_category_employee_share,
            'base_amount/%s' % self.base_amount_deductible_tax,
            'base_amount/%s' % self.base_amount_non_deductible_tax,
            'base_amount/%s' % self.base_amount_bonus,
            'base_amount/%s' % self.base_amount_base_salary,
            'grade/%s' % self.grade_worker,
            'grade/%s' % self.grade_engineer,
           )

  def createCurrencies(self):
    """Create some currencies.
    This script will reuse existing currencies, because we want currency ids 
    to be stable, as we use them as categories.
    """
    currency_module = self.getCurrencyModule()
    if not hasattr(currency_module, 'EUR'):
      self.EUR = currency_module.newContent(
          portal_type = self.currency_portal_type,
          reference = "EUR", id = "EUR", base_unit_quantity=0.001 )
      self.USD = currency_module.newContent(
          portal_type = self.currency_portal_type,
          reference = "USD", id = "USD" )
      self.YEN = currency_module.newContent(
          portal_type = self.currency_portal_type,
          reference = "YEN", id = "YEN" )
      get_transaction().commit()
      self.tic()
    else:
      self.EUR = currency_module.EUR
      self.USD = currency_module.USD
      self.YEN = currency_module.YEN

  def getBusinessTemplateList(self):
    """ """
    return ('erp5_base', 'erp5_pdm', 'erp5_trade', 'erp5_accounting', 
        'erp5_payroll',)

  def createPerson(self, id='one', title='One', 
      career_subordination_value=None, career_grade=None, **kw):
    """
      Create some Pesons so that we have something to feed.
    """
    person_module = self.portal.getDefaultModule(portal_type=\
                                                 self.person_portal_type)
    if hasattr(person_module, id):
      person_module.manage_delObjects([id])
    person = person_module.newContent(portal_type=self.person_portal_type, 
                                      id=id)
    person.edit(
        title=title,
        career_subordination_value=career_subordination_value,
        career_grade=career_grade,
               )
    get_transaction().commit()
    person.reindexObject()
    self.tic()
    return person

  def createOrganisation(self, id='company_one', title='Company One', **kw):
    if hasattr(self.organisation_module, id):
      self.organisation_module.manage_delObjects([id])
    organisation = self.organisation_module.newContent( \
                                   portal_type=self.organisation_portal_type,
                                   id=id,
                                   title=title)
    get_transaction().commit()
    organisation.reindexObject()
    self.tic()
    return organisation

  def createPayrollService(self, id='', organisation='', 
      base_amount_list=None, variation_base_category_list=None, 
      variation_category_list=None, **kw):
    payroll_service_portal_type = 'Payroll Service'
    payroll_service_module = self.portal.getDefaultModule(\
                                    portal_type=payroll_service_portal_type)

    if base_amount_list == None: 
      base_amount_list=[]
    if variation_category_list == None: 
      variation_category_list=[]
    if variation_base_category_list == None: 
      variation_category_list=[]
    if hasattr(payroll_service_module, id):
      payroll_service_module.manage_delObjects([id])

    payroll_service = payroll_service_module.newContent(\
        portal_type                  = self.payroll_service_portal_type,
        id                           = id,
        source_value                 = organisation,
        quantity_unit                = 'time/month',
        product_line                 = 'social_service/state_insurance',
        base_amount_list             = base_amount_list)
    payroll_service.setVariationBaseCategoryList(variation_base_category_list)
    payroll_service.setVariationCategoryList(variation_category_list)
    get_transaction().commit()
    payroll_service.reindexObject()
    self.tic()
    return payroll_service

  def createModel(self, id, title='', person_id='', 
      person_title='', person_career_grade='', 
      organisation_id='', organisation_title='',
      variation_settings_category_list=None,
      price_currency=''):
    """
      Create a model
    """
    if variation_settings_category_list == None:
      variation_settings_category_list = []

    organisation = self.createOrganisation(organisation_id, organisation_title)
    person = self.createPerson(id=person_id, title=person_title, 
                               career_subordination_value=organisation,
                               career_grade=person_career_grade)

    if hasattr(self.paysheet_model_module, id):
      self.paysheet_model_module.manage_delObjects([id])
    paysheet_model = self.paysheet_model_module.newContent( \
                                portal_type=self.paysheet_model_portal_type,
                                id=id)
    paysheet_model.edit(\
        title=title,
        variation_settings_category_list=variation_settings_category_list,
        destination_section_value=organisation,
        source_section_value=person,)
    paysheet_model.setPriceCurrency(price_currency)
    get_transaction().commit()
    paysheet_model.reindexObject()
    self.tic()

    return paysheet_model

  def addSlice(self, model, slice, min_value, max_value, base_id='cell'):
    '''
      add a new slice in the model
    '''
    slice = model.newCell(slice, portal_type='Pay Sheet Model Slice', 
        base_id=base_id)
    if slice is not None:
      slice.setQuantityRangeMax(max_value)
      slice.setQuantityRangeMin(min_value)

      get_transaction().commit()
      slice.reindexObject()
      self.tic()
      return slice
    return None

  def addAllSlices(self, model):
    '''
      create all usefull slices with min and max values
    '''
    model.updateCellRange(base_id='cell')
    slice_list = []
    slice_list.append(self.addSlice(model, 'salary_range/%s' % \
        self.france_settings_forfait, 0, 9999999999999))
    slice_list.append(self.addSlice(model, 'salary_range/%s' % \
        self.france_settings_slice_a, 0, self.plafond))
    slice_list.append(self.addSlice(model, 'salary_range/%s' % \
        self.france_settings_slice_b, self.plafond, self.plafond*4))
    slice_list.append(self.addSlice(model, 'salary_range/%s' % \
        self.france_settings_slice_c, self.plafond*4, self.plafond*8))
    return slice_list

  def createModelLine(self, model, id, variation_category_list, 
      resource, slice_list, share_list, values, editable=False,
      base_amount_list=['base_salary']):
    '''
      test the function addModelLine and test if the model line has been 
      well created.
      explaination for values :
      if slice_list is ('slice_a', 'slice_b') and share list is ('employer', 
      'employee') and if you want to put 100 % of 1000 for slice_a for the 
      employee and employer, and 50% of the base_application for slice_b 
      employer and and 2000 for slice_b employee, the value list will look 
      like this :
      values = [[[1000, 1], [1000, 1]], [[2000, None], [None, 0.5]]]

      next, two representations to well understand :
      
       'employee_share', 'employer_share'
      [[  1470, None  ], [  2100, None  ]] 
       'salary_range/france/forfait'

    'employee_share',  'employer_share'   'employee_share',  'employer_share'
[ [   None, 0.01   ], [   None, 0.02   ],[   None, 0.01  ], [   None, 0.02  ] ]
'salary_range/france/tranche_a''salary_range/france/tranche_b'
    '''
    
    # verify if category used in this model line are selected in the resource 
    resource_list = resource.getVariationCategoryList(base=1)
    msg='%r != %r' % (resource_list, variation_category_list)
    for i in variation_category_list:
      self.failUnless(i in resource_list, msg)

    if hasattr(model, id):
      model.manage_delObjects([id])
    model_line = model.newContent(\
        portal_type                  = self.paysheet_model_line_portal_type,
        id                           = id,
        resource_value               = resource,
        source_section_value         = model.getSourceSectionValue(),
        editable                     = editable,
        base_amount_list             = base_amount_list,
        variation_category_list      = variation_category_list,)
    get_transaction().commit()
    model_line.reindexObject()
    self.tic()

    # put values in Model Line cells
    model_line.updateCellRange(base_id='movement')
    for slice in slice_list:
      for share in share_list:
        cell = model_line.newCell(\
            share, slice, portal_type='Pay Sheet Cell', base_id='movement')
        cell.setMappedValuePropertyList(['quantity', 'price'])
        amount = values[share_list.index(share)][slice_list.index(slice)][0]
        percent = values[share_list.index(share)][slice_list.index(slice)][1]
        if amount != None:
          cell.setQuantity(amount)
        if percent != None:
          cell.setPrice(percent)
        get_transaction().commit()
        cell.reindexObject()
        self.tic()

    return model_line

  def createPaySheet(self, model, id='my_paysheet'):
    '''
      create a Pay Sheet with the model specialisation
    '''
    paysheet_module = self.portal.getDefaultModule(\
                            portal_type=self.paysheet_transaction_portal_type)
    if hasattr(paysheet_module, id):
      paysheet_module.manage_delObjects([id])
    paysheet = paysheet_module.newContent(\
        portal_type               = self.paysheet_transaction_portal_type,
        id                        = id,
        title                     = id,
        specialise_value          = model,
        source_section_value      = model.getSourceSectionValue(),
        destination_section_value = model.getDestinationSectionValue(),
        start_date                = DateTime(2008, 1, 1),
        stop_date                 = DateTime(2008, 1, 31),)
    paysheet.setPriceCurrency('currency_module/EUR')
    get_transaction().commit()
    paysheet.reindexObject()
    self.tic()
    return paysheet

  def calculatePaySheet(self, paysheet):
    '''
      Calcul the given paysheet like if you hace click on the 'Calculation of 
      the Pay Sheet Transaction' action button.
      XXX Editable line are not yet take into account
    '''
    paysheet_line_list = \
        paysheet.createPaySheetLineList()
    portal_type_list = ['Annotation Line', 'Payment Condition',
                        'Pay Sheet Model Ratio Line']
    paysheet.PaySheetTransaction_copySubObject(portal_type_list)
    get_transaction().commit()
    paysheet.recursiveReindexObject()
    self.tic()
    return paysheet_line_list

  def assertEqualAmounts(self, pay_sheet_line, correct_value_slice_list,
      base_salary, i):
    slice_list = pay_sheet_line.getVariationCategoryList(\
        base_category_list='base_salary')
    share_list = pay_sheet_line.getVariationCategoryList(\
        base_category_list='tax_category')
    for slice in slice_list:
      for share in share_list: 
        cell = pay_sheet_line.getCell(share, slice)
        value = cell.getQuantity()
        min_slice = correct_value_slice_list[i-1]
        max_slice = correct_value_slice_list[i]

        if base_salary <= max_slice:
          correct_value = base_salary - min_slice
        else:
          correct_value = max_slice - min_slice
        self.assertEqual(correct_value, value)
      i += 1

  def planPaySheet(self, paysheet, **kw) :
    """ put the paysheet in the `confirmed` state, which will 
      start the validateTransactionLines and confirm scripts """
    self.getPortal().portal_workflow.doActionFor(
      paysheet, 'plan_action',
      wf_id = 'accounting_workflow',
      skip_period_validation = 1
    )
    self.assertEquals(paysheet.getSimulationState(), 'planned')

  def confirmPaySheet(self, paysheet, **kw) :
    """ put the paysheet in the `confirmed` state, which will 
      start the validateTransactionLines and confirm scripts """
    self.getPortal().portal_workflow.doActionFor(
      paysheet, 'confirm_action',
      wf_id = 'accounting_workflow',
      skip_period_validation = 1
    )
    self.assertEquals(paysheet.getSimulationState(), 'confirmed')


class TestPayroll(TestPayrollMixin):
  RUN_ALL_TESTS = 1
  QUIET = 0

  def test_01_modelCreation(self, quiet=QUIET, run=RUN_ALL_TESTS):
    '''
      test the function createModel and test if the model has been well created
    '''
    if not run: return
    if not quiet:
      self.logMessage('Model Creation')

    if hasattr(self.paysheet_model_module, self.model_id):
      self.paysheet_model_module.manage_delObjects([self.model_id])
    
    model_count_before_add = \
        len(self.paysheet_model_module.contentValues(portal_type=\
        self.paysheet_model_portal_type))

    self.model = self.createModel(self.model_id, 
                                  self.model_title, 
                                  self.person_id, 
                                  self.person_title, 
                                  self.person_career_grade, 
                                  self.organisation_id, 
                                  self.organisation_title, 
                                  self.variation_settings_category_list, 
                                  self.price_currency)

    model_count_after_add = \
        len(self.paysheet_model_module.contentValues(portal_type=\
        self.paysheet_model_portal_type))

    # check that the number of model_lines has been incremented
    self.assertEqual(model_count_before_add+1, model_count_after_add)

    #check model have been well created
    self.model = self.paysheet_model_module._getOb(self.model_id)
    self.assertEqual(self.model_id, self.model.getId())
    self.assertEqual(self.model_title, self.model.getTitle())
    self.assertEqual(self.organisation_title, 
        self.model.getDestinationSectionTitle())
    self.assertEqual(self.person_title, self.model.getSourceSectionTitle())
    self.assertEqual(self.variation_settings_category_list, 
        self.model.getVariationSettingsCategoryList(base=1))

  def test_02_addModelLine(self, quiet=QUIET, run=RUN_ALL_TESTS):
    '''
      create a Model Line and test if it has been well created
    '''
    if not run: return
    if not quiet:
      self.logMessage('Model Line Creation')
    
    #model = self.createModel()
    self.addAllSlices(self.model)

    payroll_service_portal_type = 'Payroll Service'
    payroll_service_module = self.portal.getDefaultModule(\
                                    portal_type=payroll_service_portal_type)

    model_line_id = 'URSSAF'

    variation_category_list = self.urssaf_share_list + self.urssaf_slice_list

    model_line_count_before_add = len(self.model.contentValues(portal_type=\
        self.paysheet_model_line_portal_type))

    returned_model_line = self.createModelLine(model=self.model, 
        id=model_line_id, variation_category_list=variation_category_list, 
        resource=self.urssaf, share_list=self.urssaf_share_list, 
        slice_list=self.urssaf_slice_list,
        values=[[[None, 0.01], [None, 0.02],[None, 0.03]], [[None, 0.04], 
                 [None, 0.05], [None, 0.06]]])

    model_line_count_after_add = len(self.model.contentValues(portal_type=\
        self.paysheet_model_line_portal_type))

    # check that the number of model_lines has been incremented
    self.assertEqual(model_line_count_before_add+1, model_line_count_after_add)

    model_line = self.model._getOb(model_line_id)
    self.assertEqual(returned_model_line, model_line)
    self.assertEqual(model_line_id, model_line.getId())
    payroll_service_portal_type = 'Payroll Service'
    payroll_service_module = self.portal.getDefaultModule(\
        portal_type=payroll_service_portal_type)
    resource = payroll_service_module._getOb(self.urssaf_id)
    self.assertEqual(resource, model_line.getResourceValue())
    self.assertEqual(variation_category_list, 
        model_line.getVariationCategoryList())

  def test_03_createPaySheet(self, quiet=QUIET, run=RUN_ALL_TESTS):
    '''
      create a Pay Sheet with the model specialisation and verify it was well
      created
    '''
    if not run: return
    if not quiet:
      self.logMessage('PaySheet Creation')
    
    paysheet_id = 'my_paysheet'
    paysheet_returned = self.createPaySheet(self.model, paysheet_id)
    paysheet_module = self.portal.getDefaultModule(\
                          portal_type=self.paysheet_transaction_portal_type)
    paysheet = paysheet_module._getOb(paysheet_id)
    self.assertEqual(paysheet_returned, paysheet)
    self.assertEqual(paysheet_id, paysheet.getId())
    self.assertEqual(paysheet.getDestinationSectionTitle(), 
        self.model.getDestinationSectionTitle())
    self.assertEqual(paysheet.getSourceSectionTitle(), 
        self.model.getSourceSectionTitle())
    self.assertEqual(paysheet.getSpecialiseValue(), self.model) 

  def test_04_paySheetCalculation(self, quiet=QUIET, run=RUN_ALL_TESTS):
    '''
      test if the scripts called by the 'Calculation of the Pay Sheet 
      Transaction' action create the paysheet lines
    '''
    if not run: return
    if not quiet:
      self.logMessage('PaySheet Calculation')
    
    self.addAllSlices(self.model)

    model_line_id1 = 'urssaf'
    model_line_id2 = 'salary'
    base_salary = 10000

    urssaf_slice_list = [ 'salary_range/'+self.france_settings_slice_a, 
                          'salary_range/'+self.france_settings_slice_b, 
                          'salary_range/'+self.france_settings_slice_c]

    urssaf_share_list = [ 'tax_category/'+self.tax_category_employee_share, 
                          'tax_category/'+self.tax_category_employer_share]

    salary_slice_list = ['salary_range/'+self.france_settings_forfait,]
    salary_share_list = ['tax_category/'+self.tax_category_employee_share,]

    variation_category_list_urssaf = urssaf_share_list + urssaf_slice_list
    variation_category_list_salary = salary_share_list + salary_slice_list

    model_line1 = self.createModelLine(model=self.model, 
        id=model_line_id1,
        variation_category_list=variation_category_list_urssaf, 
        resource=self.urssaf, share_list=self.urssaf_share_list, 
        slice_list=self.urssaf_slice_list,
        values=[[[None, 0.01], [None, 0.02], [None, 0.03]], [[None, 0.04], 
          [None, 0.05], [None, 0.06]]])

    model_line2 = self.createModelLine(model=self.model, 
        id=model_line_id2,
        variation_category_list=variation_category_list_salary, 
        resource=self.labour, share_list=self.salary_share_list, 
        slice_list=salary_slice_list, base_amount_list=[],
        values=[[[base_salary, None]],])

    pay_sheet_line_count = len(self.model.contentValues(portal_type=\
        self.paysheet_line_portal_type)) + 2 # because in this test, 2 lines
                                             # are added

    paysheet = self.createPaySheet(self.model)

    paysheet_line_count_before_calculation = \
        len(paysheet.contentValues(portal_type= \
        self.paysheet_line_portal_type))

    # apply the model
    #paysheet.PaySheetTransaction_applyModel()

    # calculate the pay sheet
    pay_sheet_line_list = self.calculatePaySheet(paysheet=paysheet)

    paysheet_line_count_after_calculation = \
        len(paysheet.contentValues(portal_type= \
        self.paysheet_line_portal_type))
    self.assertEqual(paysheet_line_count_before_calculation, 0)
    self.assertEqual(paysheet_line_count_after_calculation, 
        pay_sheet_line_count)

    # check the amount in the cells of the created paysheet lines
    for pay_sheet_line in pay_sheet_line_list:
      service = pay_sheet_line.getResourceId()
      if service == self.urssaf_id:
        i = 1
        correct_value_slice_list = [0, self.plafond, self.plafond*4, 
                                    self.plafond*8]

        self.assertEqualAmounts(pay_sheet_line, correct_value_slice_list,
            base_salary, i)

      elif service == self.labour_id:
        cell = pay_sheet_line.getCell(\
            'tax_category/'+ self.tax_category_employee_share,
            'salary_range/'+ self.france_settings_forfait)
        value = cell.getTotalPrice()
        self.assertEqual(base_salary, value)

      else:
        self.fail("Unknown service for line %s" % pay_sheet_line)

  def test_05_caculationWithANonNullMinimumValueSlice(self, quiet=QUIET, 
      run=RUN_ALL_TESTS):
    '''
      if the is only slice B (without previous slice A), test that
      the amount paid for this tax is correct
    '''
    if not run: return
    if not quiet:
      self.logMessage('Calculation With A Non Null Minimum Value Slice')
    
    self.addAllSlices(self.model)

    model_line_id1 = 'urssaf'
    model_line_id2 = 'salary'
    base_salary = 10000

    urssaf_slice_list = ['salary_range/'+self.france_settings_slice_b,]
    variation_category_list_urssaf = self.urssaf_share_list + urssaf_slice_list
    variation_category_list_salary = self.salary_share_list + \
        self.salary_slice_list

    model_line1 = self.createModelLine(model=self.model, 
        id=model_line_id1,
        variation_category_list=variation_category_list_urssaf, 
        resource=self.urssaf, share_list=self.urssaf_share_list, 
        slice_list=urssaf_slice_list,
        values=[[[None, 0.03]], [[None, 0.04]],])

    model_line2 = self.createModelLine(model=self.model, 
        id=model_line_id2,
        variation_category_list=variation_category_list_salary, 
        resource=self.labour, share_list=self.salary_share_list, 
        slice_list=self.salary_slice_list, base_amount_list=[],
        values=[[[base_salary, None]],])

    pay_sheet_line_count = len(self.model.contentValues(portal_type=\
        self.paysheet_line_portal_type)) + 2 # because in this test, 2 lines
                                             # are added

    paysheet = self.createPaySheet(self.model)

    paysheet_line_count_before_calculation = \
        len(paysheet.contentValues(portal_type= \
        self.paysheet_line_portal_type))

    # calculate the pay sheet
    pay_sheet_line_list = self.calculatePaySheet(paysheet=paysheet)

    paysheet_line_count_after_calculation = \
        len(paysheet.contentValues(portal_type= \
        self.paysheet_line_portal_type))
    self.assertEqual(paysheet_line_count_before_calculation, 0)
    self.assertEqual(paysheet_line_count_after_calculation, 
        pay_sheet_line_count)
    
    # check the amount in the cells of the created paysheet lines
    for pay_sheet_line in pay_sheet_line_list:
      service = pay_sheet_line.getResourceId()
      if service == self.urssaf_id:
        i = 2 # the begining max slice
        correct_value_slice_list = [0, self.plafond, self.plafond*4, 
                                    self.plafond*8]

        self.assertEqualAmounts(pay_sheet_line, correct_value_slice_list,
            base_salary, i)

      elif service == self.labour_id:
        cell = pay_sheet_line.getCell('tax_category/'+\
            self.tax_category_employee_share,
            'salary_range/'+ self.france_settings_forfait)
        value = cell.getTotalPrice()
        self.assertEqual(base_salary, value)

      else:
        self.fail("Unknown service for line %s" % pay_sheet_line)

  def test_06_model_inheritance(self, quiet=QUIET, 
      run=RUN_ALL_TESTS):
    '''
      check that a model can inherite some datas from another
      the ineritance rules are the following :
       - a DATA could be a model_line, annotation_line, ratio_line or
         payement_condition (XXX -> this last one haven't yet reference)
       - a model_line, annotation_line and a ratio_line have a REFERENCE
       - a model can have some DATA's
       - a model can inherite from another, that's mean :
         o At the calculation step, each DATA of the parent model will be
           checked : the DATA with a REFERENCE that's already in the child 
           model will not entered in the calcul. The other will.
         o This will be repeated on each parent model and on each parent of 
           the parent model,... until there is no parent model to inherite 
           (or until a max loop number has been reached).
    '''
    if not run: return
    if not quiet:
      self.logMessage('Model Inheritance')

    # create 3 models
    model_employee = self.paysheet_model_module.newContent(id='model_employee',
        portal_type='Pay Sheet Model')

    model_company = self.paysheet_model_module.newContent(id='model_company',
        portal_type='Pay Sheet Model')

    model_country = self.paysheet_model_module.newContent(id='model_country',
        portal_type='Pay Sheet Model')

    # add some content in the models
    model_employee.newContent(id='over_time_duration',
                              title='over_time_duration',
                              portal_type='Annotation Line', 
                              reference='over_time_duration',)

    model_company.newContent( id='worked_time_duration',
                              title='worked_time_duration',
                              portal_type='Annotation Line', 
                              reference='worked_time_duration',)

    model_country.newContent( id='social_insurance',
                              title='social_insurance',
                              portal_type='Annotation Line', 
                              reference='social_insurance',)

    # inherite from each other
    model_employee.setSpecialiseValue(model_company)
    model_company.setSpecialiseValue(model_country)

    # return a list of data that should contain data from all model
    portal_type_list = ['Annotation Line', ]
    model_reference_dict = model_employee.getInheritanceModelReferenceDict(\
        portal_type_list=portal_type_list)


    # check data's are corrected
    number_of_different_references = []
    for model in model_reference_dict.keys():
      number_of_different_references.extend(model_reference_dict[model])

    self.assertEqual(len(number_of_different_references), 3) # here, there is 
                                                # 3 differents annotation line

    # check the model number
    self.assertEqual(len(model_reference_dict), 3)
    self.assertEqual(model_reference_dict[model_employee.getRelativeUrl()], 
        ['over_time_duration',])
    self.assertEqual(model_reference_dict[model_company.getRelativeUrl()], 
        ['worked_time_duration',])
    self.assertEqual(model_reference_dict[model_country.getRelativeUrl()], 
        ['social_insurance',])

    # check with more values on each model
    # employee :
    model_employee.newContent(id='1',
                              portal_type='Annotation Line', 
                              reference='1',)
    # company :
    model_company.newContent( id='1',
                              portal_type='Annotation Line', 
                              reference='1',)
    model_company.newContent( id='2',
                              portal_type='Annotation Line', 
                              reference='2',)
    # country :
    model_country.newContent( id='1',
                              portal_type='Annotation Line', 
                              reference='1',)
    model_country.newContent( id='2',
                              portal_type='Annotation Line', 
                              reference='2',)
    model_country.newContent( id='3',
                              portal_type='Annotation Line', 
                              reference='3',)
    model_country.newContent( id='4',
                              portal_type='Annotation Line', 
                              reference='4',)

    # return a list of data that should contain data from all model
    portal_type_list = ['Annotation Line', ]
    model_reference_dict = {}
    model_reference_dict = model_employee.getInheritanceModelReferenceDict(\
        portal_type_list=portal_type_list)

    # check that if a reference is already present in the model_employee,
    # and the model_company contain a data with the same one, the data used at
    # the calculation step is the model_employee data.
    number_of_different_references = []
    for model in model_reference_dict.keys():
      number_of_different_references.extend(model_reference_dict[model])

    self.assertEqual(len(number_of_different_references), 7) # here, there is 
    # 4 differents annotation lines, and with the 3 ones have been had before
    # that's make 7 !



    # check the model number
    self.assertEqual(len(model_reference_dict), 3)
    self.assertEqual(set(model_reference_dict[model_employee.getRelativeUrl()]), 
        set(['1', 'over_time_duration']))
    self.assertEqual(set(model_reference_dict[model_company.getRelativeUrl()]), 
        set(['2', 'worked_time_duration']))
    self.assertEqual(set(model_reference_dict[model_country.getRelativeUrl()]), 
        set(['3','4', 'social_insurance']))


    # same test with a multi model inheritance
    model_a = self.paysheet_model_module.newContent(id='model_a', 
        title='model_a', portal_type='Pay Sheet Model')
    model_b = self.paysheet_model_module.newContent(id='model_b', 
        title='model_b', portal_type='Pay Sheet Model')
    model_c = self.paysheet_model_module.newContent(id='model_c', 
        title='model_c', portal_type='Pay Sheet Model')
    model_d = self.paysheet_model_module.newContent(id='model_d', 
        title='model_d', portal_type='Pay Sheet Model')

    # check with more values on each model
    # a :
    model_a.newContent(id='5', portal_type='Annotation Line', reference='5')
    # b :
    model_b.newContent(id='5',portal_type='Annotation Line', reference='5')
    model_b.newContent(id='6',portal_type='Annotation Line', reference='6')
    # c :
    model_c.newContent(id='5', portal_type='Annotation Line', reference='5')
    model_c.newContent(id='6', portal_type='Annotation Line', reference='6')
    model_c.newContent(id='7', portal_type='Annotation Line', reference='7')
    model_c.newContent(id='8', portal_type='Annotation Line', reference='8')
    # d :
    model_d.newContent(id='5',portal_type='Annotation Line', reference='5')
    model_d.newContent(id='6',portal_type='Annotation Line', reference='6')


    # inherite from each other
    model_a.setSpecialiseValue(model_c)
    model_country.setSpecialiseValue(model_d)
    model_company.setSpecialiseValueList([model_country, model_a, model_b])
    model_employee.setSpecialiseValue(model_company)

    # get a list of data that should contain data from all model inheritance
    # dependances tree
    portal_type_list = ['Annotation Line', ]
    model_reference_dict = {}
    model_reference_dict = model_employee.getInheritanceModelReferenceDict(\
        portal_type_list=portal_type_list)


    # check data's are corrected
    number_of_different_references = []
    for model in model_reference_dict.keys():
      number_of_different_references.extend(model_reference_dict[model])

    self.assertEqual(len(number_of_different_references), 11) # here, there is 
    # 8 differents annotation lines, and with the 3 ones have been had before
    # that's make 11 !
    
    # check the model number
    self.assertEqual(len(model_reference_dict), 6) # there is 7 model, but the
    # model_d is not take into account because it have no annotation line wich
    # are not already added by other models


    # the inheritance tree look like this :

#                                model_employee
#                           ('overtime_duration', '1')
#                                      |
#                                      |
#                                      |
#                                model_company
#                      ('worked_time_duration', '1', '2')
#                         /            |            \
#                        /             |             \
#                       /              |              \
#            model_country           model_a          model_b
#         ('social_insurance',       ('5',)          ('5', '6')
#          '1', '2', '3', '4')         |
#                  |                   |
#                  |                   |
#               model_d             model_c
#            ('5', '6')       ('5', '6', '7', '8')




    self.assertEqual(set(model_reference_dict[model_employee.getRelativeUrl()]),
        set(['1', 'over_time_duration']))
    self.assertEqual(set(model_reference_dict[model_company.getRelativeUrl()]), 
        set(['2', 'worked_time_duration']))
    self.assertEqual(set(model_reference_dict[model_country.getRelativeUrl()]), 
        set(['3','4', 'social_insurance']))
    self.assertEqual(model_reference_dict[model_a.getRelativeUrl()], ['5',])
    self.assertEqual(model_reference_dict[model_b.getRelativeUrl()], ['6',])
    self.assertEqual(set(model_reference_dict[model_c.getRelativeUrl()]), 
        set(['7', '8']))


    # get all sub objects from a paysheet witch inherite of model_employee

    # create a paysheet
    id = 'inheritance_paysheet'
    paysheet_module = self.portal.getDefaultModule(\
                            portal_type=self.paysheet_transaction_portal_type)
    if hasattr(paysheet_module, id):
      paysheet_module.manage_delObjects([id])
    paysheet = paysheet_module.newContent(\
        portal_type               = self.paysheet_transaction_portal_type,
        id                        = id,
        title                     = id,
        specialise_value          = model_employee)

    # check heneritance works
    self.assertEqual(paysheet.getSpecialiseValue(), model_employee)

    # get a list of all this subObjects:
    sub_object_list = paysheet.getInheritedObjectValueList(portal_type_list)
    self.assertEqual(len(sub_object_list), 11)
    
  def test_07_model_getCell(self, quiet=QUIET, 
      run=RUN_ALL_TESTS):
    '''
      Model objects have a overload method called getCell. This method first
      call the XMLMatrix.getCell and if the cell is not found, call
      getCell method in all it's inherited model until the cell is found or
      the cell have been searched on all inherited models.

      TODO : Currently, the method use a Depth-First Search algorithm, it will
      be better to use Breadth-First Search one.
      more about this on :
        - http://en.wikipedia.org/wiki/Breadth-first_search
        - http://en.wikipedia.org/wiki/Depth-first_search
    '''
    if not run: return
    if not quiet:
      self.logMessage('Model getCell')

    # create 3 models
    model_employee = self.paysheet_model_module.newContent(id='model_employee',
        portal_type='Pay Sheet Model')
    model_employee.edit(variation_settings_category_list=
        self.variation_settings_category_list)

    model_company = self.paysheet_model_module.newContent(id='model_company',
        portal_type='Pay Sheet Model')
    model_company.edit(variation_settings_category_list=
        self.variation_settings_category_list)

    model_country = self.paysheet_model_module.newContent(id='model_country',
        portal_type='Pay Sheet Model')
    model_country.edit(variation_settings_category_list=
        self.variation_settings_category_list)

    # add some cells in the models
    model_employee.updateCellRange(base_id='cell')
    self.addSlice(model_employee, 'salary_range/%s' % \
        self.france_settings_slice_a, 0, 1)

    model_company.updateCellRange(base_id='cell')
    self.addSlice(model_company, 'salary_range/%s' % \
        self.france_settings_slice_b, 2, 3)
    self.addSlice(model_company, 'salary_range/%s' % \
        self.france_settings_forfait, 20, 30)

    model_country.updateCellRange(base_id='cell')
    self.addSlice(model_country, 'salary_range/%s' % \
        self.france_settings_slice_c, 4, 5)
    
    # inherite from each other
    model_employee.setSpecialiseValue(model_company)
    model_company.setSpecialiseValue(model_country)


    # check getCell results

    # check model_employee could access all cells
    cell_a = model_employee.getCell('salary_range/%s' % \
                        self.france_settings_slice_a)
    self.assertNotEqual(cell_a, None)
    self.assertEqual(cell_a.getQuantityRangeMin(), 0)
    self.assertEqual(cell_a.getQuantityRangeMax(), 1)

    cell_b = model_employee.getCell('salary_range/%s' % \
                        self.france_settings_slice_b)
    self.assertNotEqual(cell_b, None)
    self.assertEqual(cell_b.getQuantityRangeMin(), 2)
    self.assertEqual(cell_b.getQuantityRangeMax(), 3)

    cell_forfait = model_employee.getCell('salary_range/%s' % \
                        self.france_settings_forfait)
    self.assertNotEqual(cell_forfait, None)
    self.assertEqual(cell_forfait.getQuantityRangeMin(), 20)
    self.assertEqual(cell_forfait.getQuantityRangeMax(), 30)

    cell_c = model_employee.getCell('salary_range/%s' % \
                        self.france_settings_slice_c)
    self.assertNotEqual(cell_c, None)
    self.assertEqual(cell_c.getQuantityRangeMin(), 4)
    self.assertEqual(cell_c.getQuantityRangeMax(), 5)

    # check model_company could access just it's own cell and this of the country
    # model
    cell_a = model_company.getCell('salary_range/%s' % \
                        self.france_settings_slice_a)
    self.assertEqual(cell_a, None)

    cell_b = model_company.getCell('salary_range/%s' % \
                        self.france_settings_slice_b)
    self.assertNotEqual(cell_b, None)
    self.assertEqual(cell_b.getQuantityRangeMin(), 2)
    self.assertEqual(cell_b.getQuantityRangeMax(), 3)

    cell_forfait = model_company.getCell('salary_range/%s' % \
                        self.france_settings_forfait)
    self.assertNotEqual(cell_forfait, None)
    self.assertEqual(cell_forfait.getQuantityRangeMin(), 20)
    self.assertEqual(cell_forfait.getQuantityRangeMax(), 30)

    cell_c = model_company.getCell('salary_range/%s' % \
                        self.france_settings_slice_c)
    self.assertNotEqual(cell_c, None)
    self.assertEqual(cell_c.getQuantityRangeMin(), 4)
    self.assertEqual(cell_c.getQuantityRangeMax(), 5)

    # check model_country could access just it's own cell
    # model
    cell_a = model_country.getCell('salary_range/%s' % \
                        self.france_settings_slice_a)
    self.assertEqual(cell_a, None)

    cell_b = model_country.getCell('salary_range/%s' % \
                        self.france_settings_slice_b)
    self.assertEqual(cell_b, None)

    cell_forfait = model_country.getCell('salary_range/%s' % \
                        self.france_settings_forfait)
    self.assertEqual(cell_forfait, None)

    cell_c = model_country.getCell('salary_range/%s' % \
                        self.france_settings_slice_c)
    self.assertNotEqual(cell_c, None)
    self.assertEqual(cell_c.getQuantityRangeMin(), 4)
    self.assertEqual(cell_c.getQuantityRangeMax(), 5)


import unittest
def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestPayroll))
  return suite
