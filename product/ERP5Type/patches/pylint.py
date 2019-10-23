# -*- coding: utf-8 -*-
#
# Copyright (c) 2003-2012 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# Copyright (c) 2013 Nexedi SA and Contributors. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from __future__ import absolute_import
from inspect import getargspec
import sys

try:
    # TODO: Add support for newer versions pylint. Meanwhile, make sure that
    #       trying to use it does not import isort, because the latter hacks
    #       Python in order to execute:
    #           sys.setdefaultencoding('utf-8')
    #       This changes the behaviour of some ERP5 code.
    sys.modules.setdefault('isort', None)

    from pylint.checkers.imports import ImportsChecker
    import astroid
    ImportsChecker.get_imported_module
except (AttributeError, ImportError):
    pass
else:
    def _get_imported_module(self, importnode, modname):
        try:
            return importnode.do_import_module(modname)
        except astroid.InferenceError, ex:
            # BEGIN

            # XXX-arnau: Ignore ERP5 dynamic modules, hackish but required
            # until proper introspection is implemented because otherwise it
            # is impossible to validate Components importing other Components
            # and as it is static analysis, the module should not be loaded
            # anyway
            if modname.startswith('erp5'):
                return

            # Handle ImportError try/except checking for missing module before
            # falling back to code handling such case (#9386)
            pnode = importnode.parent
            if pnode and isinstance(pnode, astroid.TryExcept):
                for handler in pnode.handlers:
                    # Handling except:
                    if not handler.type:
                        return

                    # Handling ImportError and its Exception base classes
                    for klass in ImportError.mro():
                        if klass is object:
                            break
                        elif klass.__name__ == handler.type.name:
                            return
            # END

            if str(ex) != modname:
                args = '%r (%s)' % (modname, ex)
            else:
                args = repr(modname)
            self.add_message("F0401", args=args, node=importnode)

    if 'modnode' in getargspec(ImportsChecker.get_imported_module).args:
        # BBB for pylint < 1.4.0
        def get_imported_module(self, modnode, importnode, modname):
            return _get_imported_module(self, importnode, modname)
    else:
        get_imported_module = _get_imported_module

    ImportsChecker.get_imported_module = get_imported_module

    # All arguments are passed as arguments and this needlessly outputs a 'No
    # config file found, using default configuration' message on stderr.
    from logilab.common.configuration import OptionsManagerMixIn
    OptionsManagerMixIn.read_config_file = lambda *args, **kw: None

    ## Patch to generate AST for ZODB Components
    def _buildAstroidModuleFromComponentModuleName(modname):
        from Products.ERP5.ERP5Site import getSite
        from Acquisition import aq_base
        portal = getSite()
        component_tool = aq_base(portal.portal_components)
        component_obj = None
        component_id = modname[len('erp5.component.'):]
        if '_version' in modname:
            try:
                obj = getattr(component_tool,
                              component_id.replace('_version', '', 1))
            except AttributeError:
                return
            if obj.getValidationState() in ('modified', 'validated'):
                component_obj = obj
        else:
            try:
                package, reference = component_id.split('.', 1)
            except ValueError:
                return
            for version in portal.getVersionPriorityNameList():
                try:
                    obj = getattr(component_tool,
                                  '%s.%s.%s' % (package, version, reference))
                except AttributeError:
                    continue

                if obj.getValidationState() in ('modified', 'validated'):
                    component_obj = obj
                    break

        if component_obj is None:
            return

        from astroid.builder import AstroidBuilder
        from astroid import MANAGER
        # 'module_build()' could also be used but this requires importing
        # the ZODB Component and also monkey-patch it to support PEP-302
        # for __file__ starting with '<'
        return AstroidBuilder(MANAGER).string_build(
            component_obj.getTextContent(validated_only=True),
            modname)

    from pylint.checkers.variables import VariablesChecker
    VariablesChecker_visit_from = VariablesChecker.visit_from
    from pylint.checkers.utils import check_messages
    @check_messages('import-error', 'no-name-in-module')
    def visit_from(self, node):
        if not node.modname.startswith('erp5.component.'):
            return VariablesChecker_visit_from(self, node)

        module = _buildAstroidModuleFromComponentModuleName(node.modname)
        if module is None:
            self.add_message('import-error', args=repr(node.modname), node=node)
            return

        for name, _ in node.names:
            if name == '*':
                continue
            self._check_module_attrs(node, module, name.split('.'))
    VariablesChecker.visit_from = visit_from

    VariablesChecker_visit_import = VariablesChecker.visit_import
    @check_messages('import-error', 'no-name-in-module')
    def visit_import(self, node):
        """check modules attribute accesses"""
        for name, _ in node.names:
            if name.startswith('erp5.component.'):
                module = _buildAstroidModuleFromComponentModuleName(name)
                if module is None:
                    self.add_message('import-error', args=repr(name), node=node)
                    continue
            else:
                parts = name.split('.')
                try:
                    module = next(node.infer_name_module(parts[0]))
                except astroid.ResolveError:
                    continue
                self._check_module_attrs(node, module, parts[1:])
    VariablesChecker.visit_import = visit_import

finally:
    if sys.modules['isort'] is None:
        del sys.modules['isort']
