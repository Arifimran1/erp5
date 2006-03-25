"""Exception Classes for ERP5"""

# These classes are placed here so that they can be imported into TTW Python
# scripts. To do so, add the following line to your Py script:
# from Products.ERP5.Errors import DeferredCatalogError

from Products.PythonScripts.Utility import allow_class
from Products.CMFCore.WorkflowCore import WorkflowException

class DeferredCatalogError(Exception):

    def __init__(self, error_key, context):
        Exception.__init__(self, error_key)
        self.error_key = error_key
        self.field_id = context.getRelativeUrl()

class ImmobilisationValidityError(Exception):pass
class ImmobilisationCalculationError(Exception):pass

allow_class(DeferredCatalogError)
allow_class(ImmobilisationValidityError)
allow_class(ImmobilisationCalculationError)
allow_class(WorkflowException)
