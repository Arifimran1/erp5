import os
import shutil
import socket
import sys
import glob
import threading
import ZODB
from asyncore import socket_map
from ZODB.DemoStorage import DemoStorage
from ZODB.FileStorage import FileStorage
from Products.ERP5Type.tests.utils import getMySQLArguments, instance_random
from Products.ERP5Type.tests.runUnitTest import static_dir_list

def _print(message):
  sys.stderr.write(message + "\n")

instance_home = os.environ['INSTANCE_HOME']
zserver_list = os.environ.get('zserver', '').split(',')
os.environ['zserver'] = zserver_list[0]

zeo_client = os.environ.get('zeo_client')
if zeo_client:
  zeo_client = zeo_client.rsplit(':', 1)
  zeo_client = (len(zeo_client) == 1 and 'localhost' or zeo_client[0],
                int(zeo_client[-1]))
try:
  activity_node = int(os.environ['activity_node'])
except KeyError:
  activity_node = (zeo_client or 'zeo_server' in os.environ) and 1 or None

data_fs_path = os.environ.get('erp5_tests_data_fs_path',
                              os.path.join(instance_home, 'Data.fs'))
load = int(os.environ.get('erp5_load_data_fs', 0))
save = int(os.environ.get('erp5_save_data_fs', 0))
save_mysql = int(os.environ.get('erp5_dump_sql') or not zeo_client) or None

if save_mysql:
  def save_mysql(verbosity=1):
    # The output of mysqldump needs to merge many lines at a time
    # for performance reasons (merging lines is at most 10 times
    # faster, so this produce somewhat not nice to read sql
    command = 'mysqldump %s > dump.sql' % getMySQLArguments()
    if verbosity:
      _print('Dumping MySQL database with %s...' % command)
    os.system(command)

_print("Cleaning static files ... ")
for dir in static_dir_list:
  for f in glob.glob(os.path.join(instance_home, dir, '*')):
    os.remove(f)

if load:
  if save_mysql:
    dump_sql = os.path.join(instance_home, 'dump.sql')
    if os.path.exists(dump_sql):
      _print("Restoring MySQL database ... ")
      ret = os.system("mysql %s < %s" % (getMySQLArguments(), dump_sql))
      assert not ret
    else:
      _print("Could not find MySQL dump, will recreate catalog ... ")
      os.environ['erp5_tests_recreate_catalog'] = '1'
  _print("Restoring static files ... ")
  live_instance_path = os.environ.get('live_instance_path')
  for dir in static_dir_list:
    full_path = os.path.join(instance_home, dir)
    if live_instance_path:
      backup_path = os.path.join(live_instance_path, dir)
    else:
      backup_path = full_path + '.bak'
    if os.path.exists(backup_path):
      os.rmdir(full_path)
      shutil.copytree(backup_path, full_path, symlinks=True)
elif save and not zeo_client and os.path.exists(data_fs_path):
  os.remove(data_fs_path)

zeo_server_pid = None
zeo_client_pid_list = []

ZEvent = sys.modules.get('ZServer.PubCore.ZEvent')
def fork():
  pid = os.fork()
  if pid:
    # recreate the event pipe if it already exists
    for obj in socket_map.values():
      assert obj is ZEvent.the_trigger
      obj.close()
      ZEvent.the_trigger = ZEvent.simple_trigger()
    # make sure parent and child have 2 different RNG
    instance_random.seed(instance_random.random())
  return pid

while not zeo_client:
  if activity_node:
    r, zeo_client = os.pipe()
    zeo_server_pid = fork()
    if zeo_server_pid:
      save_mysql = None
      os.close(zeo_client)
      zeo_client = eval(os.fdopen(r).read())
      continue
    else:
      zeo_client_pid_list = activity_node = None
      os.close(r)
  elif activity_node is not None:
    # run ZEO server but no need to fork
    zeo_server_pid = 0

  if save:
    Storage = FileStorage(data_fs_path)
  elif load:
    Storage = DemoStorage(base=FileStorage(data_fs_path, read_only=True))
  else:
    Storage = DemoStorage()
  break
else:
  for i in xrange(1, activity_node):
    pid = fork()
    if not pid:
      zeo_client_pid_list = None
      os.environ['zserver'] = i < len(zserver_list) and zserver_list[i] or ''
      break
    zeo_client_pid_list.append(pid)
  # Zope 2.12: do not import ClientStorage before forking due to client trigger
  from ZEO.ClientStorage import ClientStorage
  Storage = ClientStorage(zeo_client)

if zeo_client_pid_list is not None:
  _print("Instance at %r loaded ... " % instance_home)
