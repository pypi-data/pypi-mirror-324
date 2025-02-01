import sqlite3
import pickle
import functools


class PersistentMap:
  def __init__(self, db_path="data.db"):
    """Initialize the SQLite key-value store."""
    self.db_path = db_path
    self._ensure_table()

  def _ensure_table(self):
    """Ensures that the key-value table exists."""
    with sqlite3.connect(self.db_path) as conn:
      conn.execute("""
        CREATE TABLE IF NOT EXISTS kv (
          key TEXT PRIMARY KEY,
          value BLOB
        )
      """)

  def set(self, key, value):
    """Insert or update a key-value pair."""
    if not isinstance(value, bytes):
      value = pickle.dumps(value)

    with sqlite3.connect(self.db_path) as conn:
      conn.execute(
        "INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)", (key, value)
      )

  def get(self, key):
    """Retrieve a value by key. Returns None if the key does not exist."""
    with sqlite3.connect(self.db_path) as conn:
      row = conn.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
      if row:
        return pickle.loads(row[0])
    return None

  def delete(self, key):
    """Delete a key from the database."""
    with sqlite3.connect(self.db_path) as conn:
      conn.execute("DELETE FROM kv WHERE key=?", (key,))

  def keys(self):
    """Return all stored keys."""
    with sqlite3.connect(self.db_path) as conn:
      return [row[0] for row in conn.execute("SELECT key FROM kv").fetchall()]


# From functools.
def _make_key(args, kwds):
  """Generate a cache key based on function arguments."""
  key_parts = list(map(repr, args)) + [f"{k}={repr(v)}" for k, v in kwds.items()]
  return "_".join(key_parts)


def diskoize(db_path="data.db"):
  def decorator(func):
    cache = PersistentMap(db_path)
    @functools.wraps(func)
    def wrapper(*args, **kwds):
      key = _make_key(args, kwds)
      result = cache.get(key)
      if result is not None:
        return result
      result = func(*args, **kwds)
      cache.set(key, result)
      return result
    return wrapper
  return decorator


# TODO:
#   - don't use None value for cache miss, this is a terrible idea. (Depickle only if not None.)
#   - add sugar for file name choice (including temp files)
#   - add methods for interacting with the cache
#   - add more examples
#   - add flush() method, and a lru_cache to support it
#   - fix _make_key


# Usage example
# import requests
# @diskoize("/tmp/scrape_google.db")
# def scrape_google():
#   return requests.get("https://www.google.com").text
#
# print(scrape_google())
# print(scrape_google())  # Cached result, even after rerunning the script

