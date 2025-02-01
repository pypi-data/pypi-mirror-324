
from datasette import hookimpl
import sqlite_tg

__version__ = "0.0.1a19"
__version_info__ = tuple(__version__.split("."))

@hookimpl
def prepare_connection(conn):
  conn.enable_load_extension(True)
  sqlite_tg.load(conn)
  conn.enable_load_extension(False)
