"""
 TODO: Add copyright.
"""


import unittest
import sys, os, tempfile, stat, subprocess

def createCleanList(s):
  """
    TODO: Add doc string.
  """
  return sorted([q.strip() for q in s.split() if len(q.strip()) > 0])

class AssertPythonSoftware(unittest.TestCase):
  """
    TODO: Add doc string.
  """

  def test_python_version(self):
   """
    TODO: Add doc string.
   """
   self.assertEqual((2,4), sys.version_info[:2])

  def test_use_generated_python(self):
    """
      TODO: Add doc string.
    """
    fd, name = tempfile.mkstemp()
    try:
      f = os.fdopen(fd, 'w')
      f.write("""\
#!%s
import sys
print sys.version_info[:2]
    """ % sys.executable)
      f.close()
      f_stat = os.stat(name)
      os.chmod(name, f_stat.st_mode | stat.S_IXUSR)
      result = subprocess.Popen([name], stdout=subprocess.PIPE)\
          .communicate()[0].strip()
      self.assertEqual('(2, 4)', result)
    finally:
      os.unlink(name)

  def test_required_libraries(self):
    """
      TODO: Add doc string.
    """
    required_library_list = createCleanList("""
      ERP5Diff
      MySQLdb
      SOAPpy
      _ssl
      _xmlplus
      bz2
      cElementTree
      elementtree
      fpconst
      gdbm
      itools
      ldap
      lxml
      mechanize
      memcache
      numpy
      paramiko
      ply
      pytz
      readline
      simplejson
      socks
      threadframe
      uuid
      xml
      xml.parsers.expat
      zlib
      """)
    failed_library_list = []
    for lib in required_library_list:
      try:
        __import__(lib)
      except ImportError:
        failed_library_list.append(lib)
    self.assertEqual([], failed_library_list,
        'Python libraries not found:\n'+'\n'.join(failed_library_list))

class AssertLddLibs(unittest.TestCase):
  """
    TODO: Add doc string.
  """

  def test_tritonn_senna(self):
    """
      TODO: Add doc string.
    """
    result = os.system("ldd parts/mysql-tritonn-5.0/libexec/mysqld | grep -q "
        "'parts/senna/lib/libsenna.so.0'")
    self.assertEqual(result, 0)

  def test_MySQLdb(self):
    """
      TODO: Add doc string.
    """
    result = os.system("ldd develop-eggs/MySQL_python-1.2.3c1-py2.4-linux-x86"
       "_64.egg/_mysql.so | grep -q 'parts/mysql-tritonn-5.0/lib/mysql/libmys"
       "qlclient_r.so'")
    self.assertEqual(result, 0)

  def test_memcached_libevent(self):
    """
      TODO: Add doc string.
    """
    result = os.system("ldd parts/memcached/bin/memcached | grep -q 'parts/li"
        "bevent/lib/libevent'")

class AssertApache(unittest.TestCase):
  """
    TODO: Add doc string.
  """

  def test_modules(self):
    """
      TODO: Add doc string.
    """
    required_module_list = createCleanList("""
      authn_default_module
      log_config_module
      proxy_http_module
      authn_alias_module
      authz_dbm_module
      case_filter_in_module
      imagemap_module
      setenvif_module
      include_module
      charset_lite_module
      info_module
      cache_module
      actions_module
      proxy_connect_module
      auth_digest_module
      unique_id_module
      mime_magic_module
      disk_cache_module
      mime_module
      usertrack_module
      asis_module
      optional_hook_import_module
      negotiation_module
      proxy_module
      authz_default_module
      ext_filter_module
      auth_basic_module
      authz_owner_module
      authn_anon_module
      rewrite_module
      proxy_balancer_module
      substitute_module
      filter_module
      expires_module
      autoindex_module
      status_module
      cgid_module
      version_module
      echo_module
      optional_fn_export_module
      optional_fn_import_module
      ident_module
      cgi_module
      bucketeer_module
      optional_hook_export_module
      vhost_alias_module
      ssl_module
      authz_user_module
      env_module
      logio_module
      proxy_ftp_module
      cern_meta_module
      authz_groupfile_module
      dir_module
      log_forensic_module
      alias_module
      deflate_module
      authn_dbm_module
      case_filter_module
      authz_host_module
      headers_module
      dumpio_module
      speling_module
      authn_file_module
    """)
    parts_path_prefix = os.path.join(os.path.dirname(__file__), '../parts')
    result = os.popen("%s/apache/bin/httpd -M" % parts_path_prefix)
    loaded_module_list = [module_name for module_name in result.read().split() 
                          if module_name.endswith('module')]
    result.close()
    failed_module_list = []
    for module in required_module_list:
      if module not in loaded_module_list:
        failed_module_list.append(module)
    self.assertEqual([], failed_module_list,
        'Apache modules not found:\n'+'\n'.join(failed_module_list))

    
if __name__ == '__main__':
  unittest.main()
