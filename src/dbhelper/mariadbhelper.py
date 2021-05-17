import os
import configparser
import mariadb


class PotentialSQLInjectionAttempt(Exception):
    """
    Exception that indicates a POTENTIAL attempt of SQL injection.
    It does NOT, however, confirm for certain that it is one!
    """

    def __init__(self, message="Potential SQL Injection Attempt"):
        self.message = message
        super().__init__(self.message)


class MariaDBHelper(object):
    """
    MariaDB Class Helper: manages a connection to a local or remote MariaDB database.
    """

    # MariaDB Reserved keywords
    KEYWORDS = [
        "ACCESSIBLE",
        "ADD",
        "ALL",
        "ALTER",
        "ANALYZE",
        "AND",
        "AS",
        "ASC",
        "ASENSITIVE",
        "BEFORE",
        "BETWEEN",
        "BIGINT",
        "BINARY",
        "BLOB",
        "BOTH",
        "BY",
        "CALL",
        "CASCADE",
        "CASE",
        "CHANGE",
        "CHAR",
        "CHARACTER",
        "CHECK",
        "COLLATE",
        "COLUMN",
        "CONDITION",
        "CONSTRAINT",
        "CONTINUE",
        "CONVERT",
        "CREATE",
        "CROSS",
        "CURRENT_DATE",
        "CURRENT_ROLE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "CURRENT_USER",
        "CURSOR",
        "DATABASE",
        "DATABASES",
        "DAY_HOUR",
        "DAY_MICROSECOND",
        "DAY_MINUTE",
        "DAY_SECOND",
        "DEC",
        "DECIMAL",
        "DECLARE",
        "DEFAULT",
        "DELAYED",
        "DELETE",
        "DESC",
        "DESCRIBE",
        "DETERMINISTIC",
        "DISTINCT",
        "DISTINCTROW",
        "DIV",
        "DO_DOMAIN_IDS",
        "DOUBLE",
        "DROP",
        "DUAL",
        "EACH",
        "ELSE",
        "ELSEIF",
        "ENCLOSED",
        "ESCAPED",
        "EXCEPT",
        "EXISTS",
        "EXIT",
        "EXPLAIN",
        "FALSE",
        "FETCH",
        "FLOAT",
        "FLOAT4",
        "FLOAT8",
        "FOR",
        "FORCE",
        "FOREIGN",
        "FROM",
        "FULLTEXT",
        "GENERAL",
        "GRANT",
        "GROUP",
        "HAVING",
        "HIGH_PRIORITY",
        "HOUR_MICROSECOND",
        "HOUR_MINUTE",
        "HOUR_SECOND",
        "IF",
        "IGNORE",
        "IGNORE_DOMAIN_IDS",
        "IGNORE_SERVER_IDS",
        "IN",
        "INDEX",
        "INFILE",
        "INNER",
        "INOUT",
        "INSENSITIVE",
        "INSERT",
        "INT",
        "INT1",
        "INT2",
        "INT3",
        "INT4",
        "INT8",
        "INTEGER",
        "INTERSECT",
        "INTERVAL",
        "INTO",
        "IS",
        "ITERATE",
        "JOIN",
        "KEY",
        "KEYS",
        "KILL",
        "LEADING",
        "LEAVE",
        "LEFT",
        "LIKE",
        "LIMIT",
        "LINEAR",
        "LINES",
        "LOAD",
        "LOCALTIME",
        "LOCALTIMESTAMP",
        "LOCK",
        "LONG",
        "LONGBLOB",
        "LONGTEXT",
        "LOOP",
        "LOW_PRIORITY",
        "MASTER_HEARTBEAT_PERIOD",
        "MASTER_SSL_VERIFY_SERVER_CERT",
        "MATCH",
        "MAXVALUE",
        "MEDIUMBLOB",
        "MEDIUMINT",
        "MEDIUMTEXT",
        "MIDDLEINT",
        "MINUTE_MICROSECOND",
        "MINUTE_SECOND",
        "MOD",
        "MODIFIES",
        "NATURAL",
        "NOT",
        "NO_WRITE_TO_BINLOG",
        "NULL",
        "NUMERIC",
        "OFFSET",
        "ON",
        "OPTIMIZE",
        "OPTION",
        "OPTIONALLY",
        "OR",
        "ORDER",
        "OUT",
        "OUTER",
        "OUTFILE",
        "OVER",
        "PAGE_CHECKSUM",
        "PARSE_VCOL_EXPR",
        "PARTITION",
        "POSITION",
        "PRECISION",
        "PRIMARY",
        "PROCEDURE",
        "PURGE",
        "RANGE",
        "READ",
        "READS",
        "READ_WRITE",
        "REAL",
        "RECURSIVE",
        "REF_SYSTEM_ID",
        "REFERENCES",
        "REGEXP",
        "RELEASE",
        "RENAME",
        "REPEAT",
        "REPLACE",
        "REQUIRE",
        "RESIGNAL",
        "RESTRICT",
        "RETURN",
        "RETURNING",
        "REVOKE",
        "RIGHT",
        "RLIKE",
        "ROWS",
        "SCHEMA",
        "SCHEMAS",
        "SECOND_MICROSECOND",
        "SELECT",
        "SENSITIVE",
        "SEPARATOR",
        "SET",
        "SHOW",
        "SIGNAL",
        "SLOW",
        "SMALLINT",
        "SPATIAL",
        "SPECIFIC",
        "SQL",
        "SQLEXCEPTION",
        "SQLSTATE",
        "SQLWARNING",
        "SQL_BIG_RESULT",
        "SQL_CALC_FOUND_ROWS",
        "SQL_SMALL_RESULT",
        "SSL",
        "STARTING",
        "STATS_AUTO_RECALC",
        "STATS_PERSISTENT",
        "STATS_SAMPLE_PAGES",
        "STRAIGHT_JOIN",
        "TABLE",
        "TERMINATED",
        "THEN",
        "TINYBLOB",
        "TINYINT",
        "TINYTEXT",
        "TO",
        "TRAILING",
        "TRIGGER",
        "TRUE",
        "UNDO",
        "UNION",
        "UNIQUE",
        "UNLOCK",
        "UNSIGNED",
        "UPDATE",
        "USAGE",
        "USE",
        "USING",
        "UTC_DATE",
        "UTC_TIME",
        "UTC_TIMESTAMP",
        "VALUES",
        "VARBINARY",
        "VARCHAR",
        "VARCHARACTER",
        "VARYING",
        "WHEN",
        "WHERE",
        "WHILE",
        "WINDOW",
        "WITH",
        "WRITE",
        "XOR",
        "YEAR_MONTH",
        "ZEROFILL"
    ]

    EXCEPTIONS = [
        "ACTION",
        "BIT",
        "DATE",
        "ENUM",
        "NO",
        "TEXT",
        "TIME",
        "TIMESTAMP"
    ]

    ORACLE_MODE = [
        "BODY",
        "ELSIF",
        "GOTO",
        "HISTORY",
        "OTHERS",
        "PACKAGE",
        "PERIOD",
        "RAISE",
        "ROWTYPE",
        "SYSTEM",
        "SYSTEM_TIME",
        "VERSIONING",
        "WITHOUT"
    ]

    def __init__(self, inipath = None):
        """ Initializes with a decrypted config.ini file """
        self.config = configparser.ConfigParser()
        self.config.read(os.getcwd() + '/login/config.ini' if inipath is None else inipath)
        self.query = ""
        self.isconn = False


    def bindErrorCallback(self, errcall):
        """
        !!! YET TO BE TESTED !!!
        Binds a remote callback function to print out error messages.
        """
        self.err = errcall


    def resetQuery(self):
        """ Clears the current query. """
        self.query = ""


    def checkString(self, string):
        """
        Checks if a string or a list of strings are potentially harmful to the integrity of the database.
            Throws: `PotentialSQLInjectionAttempt`
        """
        if type(string) is list:
            for s in string:
                self.checkString(s)
        if type(string) is str:
            if string in MariaDBHelper.KEYWORDS:
                self.resetQuery()
                raise PotentialSQLInjectionAttempt(f"{string} is a reserved keyword!")
            if string in MariaDBHelper.EXCEPTIONS:
                self.resetQuery()
                raise PotentialSQLInjectionAttempt(f"{string} is a reserved exception!")
            if string in MariaDBHelper.ORACLE_MODE:
                self.resetQuery()
                raise PotentialSQLInjectionAttempt(f"{string} is a reserved special keyword!")


    def connect(self):
        """
        Tries to connect to the MariaDB database, and returns the respective cursor if available.
        """
        try:
            self.connection = mariadb.connect(
                user     = self.config['DATABASE']['user'],
                password = self.config['DATABASE']['password'],
                host     = self.config['DATABASE']['host'],
                port     = int(self.config['DATABASE']['port']),
                database = self.config['DATABASE']['database']
            )
            self.isconn = True
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None
        
        self.cursor = self.connection.cursor()
        return self.getCursor()


    def isConnected(self):
        """ Indicates if the helper has a connection running. """
        return self.isconn


    def disconnect(self):
        """ Disconnects from the database. """
        self.connection.close()
        self.isconn = False


    def commit(self):
        """ Commits the last queries to the database. """
        self.connection.commit()


    def getCursor(self):
        """ Returns the cursor of the connection to the database. """
        return self.cursor


    def Select(self, fields):
        """
        Query constructor: SELECT
            Adds from a list of tuples (field, alias), such that
            `SELECT field AS alias`.
            If no alias is desired, put `None` or an empty string.
        """
        self.query += "SELECT "
        for field, alias in fields:
            self.checkString([field, alias])
            self.query += field
            if alias != "" and alias is not None:
                self.query += f" AS '{alias}'"
            self.query += ", "
        self.query = self.query[:-2] + " "
        return self


    def From(self, table, alias=None):
        """
        Query constructor: FROM
            Adds a table and alias from the database, such that
            `FROM table alias`.
            If no alias is desired, put `None` or an empty string.
        """
        self.checkString([table, alias])
        if alias is None:
            alias = ""
        self.query += f"FROM {table} {alias} "
        return self


    def InnerJoin(self, table, condition):
        """
        Query constructor: INNER JOIN
            Adds a table and a condition, such that
            `INNER JOIN table ON condition`.
        """
        self.checkString([table, condition])
        self.query += f"INNER JOIN {table} ON {condition} "
        return self


    def OpenSubQuery(self):
        """
        Query constructor: OPEN SUBQUERY
            Adds left parenthesis.
        """
        self.query += " ( "
        return self


    def CloseSubQuery(self):
        """
        Query constructor: CLOSE SUBQUERY
            Adds right parenthesis.
        """
        self.query += " ) "
        return self


    @PendingDeprecationWarning
    def AddCustomQuery(self, query):
        """
        Query constructor: CUSTOM QUERY
            Temporary fix while the helper is not exhaustive enough.
            THIS METHOD IS NOT SAFE AND DOES NOT CHECK FOR SQL INJECTION!
        """
        self.query += f"{query} "
        return self


    def getQuery(self):
        """ Returns the current query. """
        return self.query


    def execute(self, args=None):
        """ Executes the current query. """
        if args is not None:
            self.cursor.execute(self.query, args)
        else:
            self.cursor.execute(self.query)


    def do(self):
        """
        Does the following methods in order: `execute()`, `commit()`, `resetQuery()`.
        `commit()` is executed only if `execute()` does not return any exception.
        Despite any exception that might occur, the query will be emptied.
        The exception will be thrown.
        """
        exc = None
        try:
            self.execute()
            self.commit()
        except Exception as e:
            exc = e
        finally:
            self.resetQuery()
            raise exc



# TESTE
if __name__ == "__main__":
    from prettytable import from_db_cursor

    # Instancia um objecto com o Helper
    helper = MariaDBHelper()

    # Faz a conexão, o qual recorre ao config.ini na localização predefinida
    helper.connect()

    # Verifica se a ligação foi efetuada. Se não foi, manda abaixo o programa.
    if not helper.isConnected():
        print("A coisa não ligou!")
        exit(-1)

    # Constrói uma query usando o construtor de queries próprio do helper
    helper \
        .Select([
            ('desafios_hash.id_desafio_hash', 'ID'),
            ('desafios_hash.algoritmo', None),
            ('utilizadores.username', 'Proposto por')]) \
        .From('desafios_hash') \
        .InnerJoin('utilizadores', 'desafios_hash.id_user=utilizadores.id_user')

    # Obtém a query para verificar o que o construtor fez
    print(helper.getQuery())

    # Executa a query na base de dados
    helper.execute()

    # Obtém o cursor do helper e constrói uma fancy table a partir dele
    print(from_db_cursor(helper.getCursor()))

    # Disconecta da base de dados
    helper.disconnect()
