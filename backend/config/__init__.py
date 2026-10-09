try:
    import pymysql
except ModuleNotFoundError:
    # Existing local PostgreSQL/SQLite environments do not require this
    # optional CloudBase MySQL driver.
    pymysql = None

if pymysql is not None:
    # Django expects a MySQLdb-compatible driver. PyMySQL is pure Python, which
    # keeps the CloudBase image independent from OS-level client libraries.
    pymysql.install_as_MySQLdb()
