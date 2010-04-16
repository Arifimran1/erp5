##############################################################################
#
# Copyright (c) 2006-2009 Nexedi SA and Contributors. All Rights Reserved.
#          Jerome Perrin <jerome@nexedi.com>
#          Vincent Pelletier <vincent@nexedi.com>
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

import unittest
from Products.ZSQLCatalog.SQLCatalog import Catalog as SQLCatalog
from Products.ZSQLCatalog.SQLCatalog import Query
from Products.ZSQLCatalog.SQLCatalog import ComplexQuery
from Products.ZSQLCatalog.SQLCatalog import SimpleQuery
from Products.ZSQLCatalog.Query.EntireQuery import EntireQuery
from Products.ZSQLCatalog.Query.RelatedQuery import RelatedQuery
from DateTime import DateTime
from Products.ZSQLCatalog.SQLExpression import MergeConflictError

class ReferenceQuery:
  """
    This class is made to be able to compare a generated query tree with a
    reference one.

    It supports the following types of queries:
      SimpleQuery
        This can be compared with a ReferenceQuery in the form:
        ReferenceQuery(operator=some_operator, column=value)
        Where:
        - operator is the expected comparison operator (see
          ZSQLCatalog/Operator/ComparisonOperator.py:operator_dict keys)
        - column is the expected column name (without table mapping)
        - value is the expected value (rendered as text)
      ComplexQuery
        This can be compares with a ReferenceQuery in the form:
        ReferenceQuery(*arg, operator=logical_operator)
        Where:
        - args is a list of sub-queries (each will be searched for into
          compared query tree, so order doesn't matter)
        - operator is a logical operator name (see ComplexQuery class)
      EntireQuery
        This type of query is considered as an operator-less, single-subquery
        ComplexQuery. Its embeded query will be recursed into.
      RelatedQuery
        This type of query is considered as an operator-less, single-subquery
        ComplexQuery. Its "join condition" query will be recursed into (raw sql
        will not).
      AutoQuery (known here as "Query")
        This type of query is considered as an operator-less, single-subquery
        ComplexQuery. Its wrapped (=auto-generated equivalent query) query will
        be recursed into.

    Note: This code is quite ugly as it references query classes and access
    instance attributes directly.
    But I (Vincent) believe that it would be pointless to design individual
    __eq__ methods on all queries, as anyway they must know the compared query
    class, and as such it would spread the dirtyness among code which is not
    limited to tests.
  """
  operator = None
  column = None
  value = None

  def __init__(self, *args, **kw):
    self.operator = kw.pop('operator', None)
    assert len(args) == 0 or len(kw) == 0
    self.args = []
    for arg in args:
      if isinstance(arg, (tuple, list)):
        self.args.extend(arg)
      else:
        self.args.append(arg)
    if len(kw) == 1:
      self.column, self.value = kw.items()[0]
    elif len(kw) > 1:
      raise ValueError, 'kw must not have more than one item: %r' % (kw, )

  def __eq__(self, other):
    if isinstance(other, SimpleQuery):
      return self.column is not None and \
             other.getColumn() == self.column and \
             other.getValue() == self.value and \
             other.comparison_operator == self.operator
    elif isinstance(other, ComplexQuery):
      if not (len(other.query_list) == len(self.args) and \
              other.logical_operator == self.operator):
        return False
      other_query_list = other.query_list[:]
      for subquery in self.args:
        for other_query_id in xrange(len(other_query_list)):
          other_query = other_query_list[other_query_id]
          if subquery == other_query:
            other_query_list.pop(other_query_id)
            break
        else:
          return False
      return len(other_query_list) == 0
    elif isinstance(other, EntireQuery):
      return len(self.args) == 1 and \
             self.args[0] == other.query
    elif isinstance(other, RelatedQuery):
      return self == other.join_condition
    elif isinstance(other, Query):
      return self == other.wrapped_query
    else:
      raise TypeError, 'Compared value is not a (known) Query instance: (%s) %r' % (other.__class__.__name__, other)

  def __repr__(self):
    return '<%s column=%r operator=%r value=%r args=%r>' % \
      (self.__class__.__name__, self.column, self.operator, self.value, self.args)

class RelatedReferenceQuery:
  """
    This class has the same objective as ReferenceQuery, but it is limited to
    RelatedQuery comparison: the compared query *must* be a RelatedQuery
    instance for equality to be confirmed.
  """
  def __init__(self, reference_subquery):
    self.subquery = reference_subquery

  def __eq__(self, other):
    return isinstance(other, RelatedQuery) and \
           self.subquery == other.join_condition

  def __repr__(self):
    return '<%s %r>' % (self.__class__.__name__, self.subquery)

class DummyCatalog(SQLCatalog):
  """
    Mimic a table stucture definition.
    Removes the need to instanciate a complete catalog and the need to create
    associated tables. This offers a huge flexibility.
  """

  sql_catalog_keyword_search_keys = ('keyword', )
  sql_catalog_datetime_search_keys = ('date', )
  sql_catalog_full_text_search_keys = ('fulltext', )
  sql_catalog_scriptable_keys = ('scriptable_keyword | scriptableKeyScript', )

  def getColumnMap(self):
    """
      Fake table structure description.
    """
    return {
      'uid': ['foo', 'bar'],
      'default': ['foo', ],
      'keyword': ['foo', ],
      'date': ['foo', ],
      'fulltext': ['foo', ],
      'other_uid': ['bar', ],
      'ambiguous_mapping': ['foo', 'bar'],
    }

  def getSQLCatalogRelatedKeyList(self, key_list):
    """
      Fake auto-generated related key definitions.
    """
    return [
      'related_default | bar,foo/default/z_related_table',
      'related_keyword | bar,foo/keyword/z_related_table',
      'related_date | bar,foo/date/z_related_table'
    ]

  def z_related_table(self, *args, **kw):
    """
      Mimics a ZSQLMethod subobject.
    """
    assert kw.get('src__', False)
    assert 'query_table' in kw
    assert 'table_0' in kw
    assert 'table_1' in kw
    assert len(kw) == 4
    return '%(table_0)s.uid = %(query_table)s.uid AND %(table_0)s.other_uid = %(table_1)s' % kw

  def scriptableKeyScript(self, value):
    """
      Mimics a scriptable key (PythonScript) subobject.
    """
    return SimpleQuery(comparison_operator='=', keyword=value)

class TestSQLCatalog(unittest.TestCase):
  def setUp(self):
    self._catalog = DummyCatalog('dummy_catalog')

  def assertCatalogRaises(self, exception, kw):
    self.assertRaises(exception, self._catalog, src__=1, query_table='foo', **kw)

  def catalog(self, reference_tree, kw, check_search_text=True):
    reference_param_dict = self._catalog._queryResults(query_table='foo', **kw)
    query = self._catalog.buildQuery(kw)
    self.assertEqual(reference_tree, query)
    search_text = query.asSearchTextExpression(self._catalog)
    if check_search_text:
      # XXX: sould "keyword" be always used for search text searches ?
      search_text_param_dict = self._catalog._queryResults(query_table='foo', keyword=search_text)
      self.assertEqual(reference_param_dict, search_text_param_dict,
          'Query: %r\nSearchText: %r\nReference: %r\nSecond rendering: %r' % \
                       (query, search_text, reference_param_dict, search_text_param_dict))

  def asSQLExpression(self, kw):
    entire_query = self._catalog.buildEntireQuery(kw)
    return entire_query.asSQLExpression(self._catalog, False)

  def _testDefaultKey(self, column):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='a'), operator='and'),
                 {column: 'a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', default='%a'), operator='and'),
                 {column: '%a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<', default='a'), operator='and'),
                 {column: '<a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<=', default='a'), operator='and'),
                 {column: '<=a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>=', default='a'), operator='and'),
                 {column: '>=a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>', default='a'), operator='and'),
                 {column: '>a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='!=', default='a'), operator='and'),
                 {column: '!=a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='a b'), operator='and'),
                 {column: 'a b'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='=', default='a'), ReferenceQuery(operator='>', default='b'), operator='and'), operator='and'),
                 {column: 'a >b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='a > b'), operator='and'),
                 {column: 'a > b'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='>', default='a'), ReferenceQuery(operator='>', default='b'), operator='and'), operator='and'),
                 {column: '>a >b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='>a >b'), operator='and'),
                 {column: '">a >b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>', default='>a >b'), operator='and'),
                 {column: '>">a >b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', default=['a', 'b']), operator='and'),
                 {column: 'a OR b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='a OR b'), operator='and'),
                 {column: '"a OR b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<', default='path'), operator='and'),
                 {column: {'query': 'path', 'range': 'max'}})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', default=['a', 'b']), operator='and'),
                 {column: ['a', 'b']})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', default=['a', 'b']), operator='and'),
                 {column: ['=a', '=b']})

  def test_DefaultKey(self):
    self._testDefaultKey('default')

  def test_relatedDefaultKey(self):
    self._testDefaultKey('related_default')

  def test_002_keyOverride(self):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='%a'), operator='and'),
                 {'default': {'query': '%a', 'key': 'ExactMatch'}},
                 check_search_text=False)
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='<a'), operator='and'),
                 {'default': {'query': '<a', 'key': 'ExactMatch'}},
                 check_search_text=False)

  def _testDateTimeKey(self, column):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>=', date=DateTime('2008/10/01 12:10:21')), operator='and'),
                 {column: {'query': '>2008/10/01 12:10:20', 'format': '%y/%m/%d'}})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>=', date=DateTime('2008/10/01 12:10:21 CEST')), operator='and'),
                 {column: {'query': '>2008/10/01 12:10:20 CEST', 'format': '%y/%m/%d'}})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>=', date=DateTime('2008/10/01 12:10:21 CET')), operator='and'),
                 {column: {'query': '>2008/10/01 12:10:20 CET', 'format': '%y/%m/%d'}})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/10/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/10/02 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/10/01 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/01/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2009/01/01 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/01/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/02/01 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/01 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/10/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/10/02 UTC'))
                 , operator='and'), operator='and'),
                 {column: {'type': 'date', 'query': '10/01/2008 UTC', 'format': '%m/%d/%Y'}})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/10/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/10/02 UTC'))
                 , operator='and'), operator='and'),
                 {column: {'type': 'date', 'query': '01/10/2008 UTC', 'format': '%d/%m/%Y'}})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', date=[DateTime('2008/01/10 UTC'), DateTime('2008/01/09 UTC')]), operator='and'),
                 {column: {'query': ['2008/01/10 UTC', '2008/01/09 UTC'], 'operator': 'in'}},
                 check_search_text=False)
    self.catalog(ReferenceQuery(ReferenceQuery(operator='>', date=DateTime('2008/01/10 UTC')), operator='and'),
                 {column: {'query': '2008/01/10 UTC', 'range': 'nlt'}},
                 check_search_text=False)
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/01/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2009/01/01 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/02/01 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/03/01 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/02 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/02/02 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/02/03 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/02/02 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/02/02 10:00:00 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/02/02 11:00:00 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/02/02 10 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/02/02 10:10:00 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/02/02 10:11:00 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/02/02 10:10 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(
                   ReferenceQuery(operator='>=', date=DateTime('2008/02/02 10:10:10 UTC')),
                   ReferenceQuery(operator='<', date=DateTime('2008/02/02 10:10:11 UTC'))
                 , operator='and'), operator='and'),
                 {column: '2008/02/02 10:10:10 UTC'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='is', date=None), operator='and'),
                 {column: None}, check_search_text=False)
        
  def test_DateTimeKey(self):
    self._testDateTimeKey('date')

  def test_relatedDateTimeKey(self):
    self._testDateTimeKey('related_date')

  def _testKeywordKey(self, column):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a%'), operator='and'),
                 {column: 'a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a b%'), operator='and'),
                 {column: 'a b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a b%'), operator='and'),
                 {column: '"a b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='!=', keyword='a'), operator='and'),
                 {column: '!=a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='not like', keyword='%a'), operator='and'),
                 {column: '!=%a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a'), operator='and'),
                 {column: '%a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<', keyword='a'), operator='and'),
                 {column: '<a'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a%'), ReferenceQuery(operator='like', keyword='%b%'), operator='and'), operator='and'),
                 {column: 'a AND b'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a%'), ReferenceQuery(operator='like', keyword='%b%'), operator='or'), operator='and'),
                 {column: 'a OR b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<', keyword='path'), operator='and'),
                 {column: {'query': 'path', 'range': 'max'}})
    self.catalog(ReferenceQuery(ReferenceQuery(
                     ReferenceQuery(operator='like', keyword='%a%'),
                     ReferenceQuery(operator='like', keyword='%b%')
                   , operator='or'), operator='and'),
                 {column: ['a', 'b']})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', keyword=['a', 'b']), operator='and'),
                 {column: ['=a', '=b']})
    self.catalog(ReferenceQuery(ReferenceQuery(
                     ReferenceQuery(operator='like', keyword='%a%'),
                     ReferenceQuery(operator='<', keyword='b')
                   , operator='or'), operator='and'),
                 {column: ['a', '<b']})
    self.catalog(ReferenceQuery(ReferenceQuery(
                     ReferenceQuery(operator='like', keyword='%a%'),
                     ReferenceQuery(operator='like', keyword='%b')
                   , operator='or'), operator='and'),
                 {column: ['a', '%b']})

  def test_KeywordKey(self):
    self._testKeywordKey('keyword')

  def test_relatedKeywordKey(self):
    self._testKeywordKey('related_keyword')

  def test_005_SearchText(self):
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='like', keyword='%=a%'), ReferenceQuery(operator='like', keyword='%=b%'), operator='or'), operator='and'),
                 {'keyword': '"=a" OR "=b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', keyword=['a', 'b']), operator='and'),
                 {'keyword': '="a" OR ="b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', keyword=['a', 'b']), operator='and'),
                 {'keyword': '=a OR =b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='in', keyword=['a', 'b', 'c']), operator='and'),
                 {'keyword': '=a OR =b OR =c'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a%'), operator='and'),
                 {'keyword': 'keyword:a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='a'), operator='and'),
                 {'keyword': 'default:a'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%a b%'), operator='and'),
                 {'keyword': 'a b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%=a OR =b%'), operator='and'),
                 {'keyword': '"=a OR =b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', keyword='=a OR =b'), operator='and'),
                 {'keyword': '="=a OR =b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='<', keyword='=a OR =b'), operator='and'),
                 {'keyword': '<"=a OR =b"'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', keyword='%"a" OR "b"%'), operator='and'),
                 {'keyword': '"\\"a\\" OR \\"b\\""'})
    # This example introduces impossible-to-merge search text criterion, which
    # is allowed as long as 
    reference_query = ReferenceQuery(
        ReferenceQuery(ReferenceQuery(operator='match', fulltext='a'),
        ReferenceQuery(ReferenceQuery(operator='match', fulltext='b'),
      operator='not'), operator='and'), operator='and')
    self.catalog(reference_query, {'fulltext': 'a NOT b'})
    # The same, with an order by, must raise
    self.assertRaises(MergeConflictError, self.catalog, reference_query,
      {'fulltext': 'a NOT b', 'order_by_list': [('fulltext', ), ]},
      check_search_text=False)
    # If one want to sort on, he must use the equivalent FullText syntax:
    self.catalog(ReferenceQuery(ReferenceQuery(operator='match_boolean', fulltext='a -b'), operator='and'),
      {'fulltext': 'a -b', 'order_by_list': [('fulltext', ), ]},
      check_search_text=False)
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a'),
                                               ReferenceQuery(ReferenceQuery(operator='match', fulltext='b'), operator='not'), operator='or'), operator='and'),
                 {'fulltext': 'a OR NOT b'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a'),
                                               ReferenceQuery(ReferenceQuery(operator='match', fulltext='b'), operator='not'), operator='and'), operator='and'),
                 {'fulltext': 'a AND NOT b'})

  def test_006_testRelatedKey_with_multiple_join(self):
    # The name of catalog parameter does not matter at all
    # ComplexQuery(ComplexQuery(AutoQuery(RelatedQuery(SimpleQuery())), AutoQuery(RelatedQuery(SimpleQuery()))))
    # 'AutoQuery' doesn't need any ReferenceQuery equivalent.
    self.catalog(ReferenceQuery(ReferenceQuery(
                     ReferenceQuery(RelatedReferenceQuery(ReferenceQuery(operator='=', default='a')), operator='and'),
                     ReferenceQuery(RelatedReferenceQuery(ReferenceQuery(operator='=', default='b')), operator='and')
                   , operator='and'), operator='and'),
                 {'query': ComplexQuery(Query(related_default='a'), Query(related_default='b'))})

  def test_007_testScriptableKey(self):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', keyword='%a%'), operator='and'),
                 {'scriptable_keyword': '%a%'})

  def test_008_testRawKey(self):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='%a%'), operator='and'),
                 {'default': {'query': '%a%', 'key': 'RawKey'}},
                 check_search_text=False)
    self.catalog(ReferenceQuery(ReferenceQuery(operator='=', default='>a'), operator='and'),
                 {'default': {'query': '>a', 'key': 'RawKey'}},
                 check_search_text=False)

  def test_009_testFullTextKey(self):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a'), operator='and'),
                 {'fulltext': 'a'})

  def test_isAdvancedSearchText(self):
    self.assertFalse(self._catalog.isAdvancedSearchText('a')) # No operator, no explicit column
    self.assertTrue(self._catalog.isAdvancedSearchText('a AND b')) # "AND" is an operator
    self.assertTrue(self._catalog.isAdvancedSearchText('default:a')) # "default" exists as a column
    self.assertFalse(self._catalog.isAdvancedSearchText('b:a')) # "b" doesn't exist as a column

  def test_FullTextSearchMergesQueries(self):
    """
      FullText criterion on the same scope must be merged into one query.
      Logical operator is ignored, as fulltext operators are expected instead.
    """
    self.catalog(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a b'), operator='and'),
                 {'fulltext': 'a AND b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a b'), operator='and'),
                 {'fulltext': 'a OR b'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='match', fulltext='a b'), operator='not'), operator='and'),
                 {'fulltext': 'NOT (a b)'})

  def test_NoneValueToSimpleQuery(self):
    """
      When a SimpleQuery receives a python None value and an "=" comparison
      operator (be it the default or explictely provided), it must change that
      operator into an "is" operator.
      If "is" compariton operator is explicitely provided with a non-None
      value, raise.
      If non-"=" compariton operator is provided with a None value, raise.
    """
    self.assertEqual(ReferenceQuery(operator='is', default=None),
                     SimpleQuery(default=None))
    self.assertEqual(ReferenceQuery(operator='is', default=None),
                     SimpleQuery(default=None, comparison_operator='='))
    self.assertRaises(ValueError, SimpleQuery, default=None, comparison_operator='>=')
    self.assertRaises(ValueError, SimpleQuery, default=1, comparison_operator='is')

  def test_FullTextBooleanMode(self):
    """
      Fulltext searches must switch automatically to boolean mode if boolean
      operators are found in search value.
    """
    self.catalog(ReferenceQuery(ReferenceQuery(operator='match_boolean', fulltext='a+b'), operator='and'),
                 {'fulltext': 'a+b'})
    self.catalog(ReferenceQuery(ReferenceQuery( ReferenceQuery(operator='=', uid='foo'),
                ReferenceQuery(operator='match_boolean', fulltext='+a b'), operator='and'
    ), operator='and'), {'fulltext': '+a b uid:foo'})

  def test_DefaultKeyTextRendering(self):
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', default='a% b'), operator='and'),
                 {'default': 'a% b'})
    self.catalog(ReferenceQuery(ReferenceQuery(operator='like', default='%a%'), operator='and'),
                 {'default': '%a%'})
    self.catalog(ReferenceQuery(ReferenceQuery(ReferenceQuery(operator='like', default='a% b'),
                                               ReferenceQuery(operator='like', default='a%'), operator='or'), operator='and'),
                 {'default': ['a% b', 'a%']})

  def test_SelectDict(self):
    # Simple case: no mapping hint, no ambiguity in table schema
    sql_expression = self.asSQLExpression({'select_dict': {'default': None}})
    select_dict = sql_expression.getSelectDict()
    self.assertTrue('default' in select_dict, select_dict)
    # Case with a valid hint
    sql_expression = self.asSQLExpression({'select_dict': {'default': 'foo'}})
    select_dict = sql_expression.getSelectDict()
    self.assertTrue('default' in select_dict, select_dict)
    # Case with an invalid hint: we trust user
    sql_expression = self.asSQLExpression({'select_dict': {'default': 'bar'}})
    select_dict = sql_expression.getSelectDict()
    self.assertTrue('default' in select_dict, select_dict)
    self.assertTrue('bar' in select_dict['default'], select_dict['default'])
    # Ambiguous case: mapping must raise if there is no hint
    self.assertRaises(ValueError, self.asSQLExpression, {'select_dict':
      {'ambiguous_mapping': None}})
    # Ambiguous case, but with a hint: must succeed
    sql_expression = self.asSQLExpression({'select_dict': {'ambiguous_mapping': 'bar'}})
    select_dict = sql_expression.getSelectDict()
    self.assertTrue('ambiguous_mapping' in select_dict, select_dict)
    self.assertTrue('bar' in select_dict['ambiguous_mapping'], select_dict['ambiguous_mapping'])
    # Ambiguous case, without a direct hint, but one of the tables is used in
    # the query: must succeed
    sql_expression = self.asSQLExpression({'select_dict': {'ambiguous_mapping': None},
      'other_uid': None})
    select_dict = sql_expression.getSelectDict()
    self.assertTrue('ambiguous_mapping' in select_dict, select_dict)
    self.assertTrue('bar' in select_dict['ambiguous_mapping'], select_dict['ambiguous_mapping'])

  def test_hasColumn(self):
    self.assertTrue(self._catalog.hasColumn('uid'))
    self.assertFalse(self._catalog.hasColumn('foobar'))

  def test_fulltextOrderBy(self):
    # No order_by_list, resulting "ORDER BY" must be empty.
    sql_expression = self.asSQLExpression({'fulltext': 'foo'})
    self.assertEqual(sql_expression.getOrderByExpression(), '')
    # order_by_list on fulltext column, resulting "ORDER BY" must be non-empty.
    sql_expression = self.asSQLExpression({'fulltext': 'foo',
      'order_by_list': [('fulltext', ), ]})
    self.assertNotEqual(sql_expression.getOrderByExpression(), '')

##return catalog(title=Query(title='a', operator='not'))
#return catalog(title={'query': 'a', 'operator': 'not'})
#return catalog(title={'query': ['a', 'b'], 'operator': 'not'})
#return context.portal_catalog(source_title="toto", source_description="tutu", src__=1)
#print catalog(query=ComplexQuery(Query(title='1'), ComplexQuery(Query(portal_type='Foo') ,Query(portal_type='Bar'), operator='or'), operator='and'))
#print catalog(title={'query': ('path', 2), 'operator': 'and'}, exception=TypeError)
#print catalog(sort_on=[('source_title', )], check_search_text=False)
#print catalog(query=ComplexQuery(Query(source_title='foo'), Query(source_title='bar')), sort_on=[('source_title', ), ('source_title_1', )], check_search_text=False)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestSQLCatalog))
  return suite

