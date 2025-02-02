A library that normalizes simple SQL queries and compares them first by equality of the normalized string and then using the cosette API. 

### [Beta in Development!]
 [![Build and Test](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-build.yml/badge.svg)](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-build.yml)
 [![Build and Test](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-unittests.yml/badge.svg)](https://github.com/ValentinHerrmann/sql_testing_tools/actions/workflows/python-unittests.yml)

- Submit bug reports and features requests at: https://github.com/ValentinHerrmann/sql_testing_tools
- PyPi-Package available at: https://pypi.org/project/sql-testing-tools/ 



### Getting started

Use the following code to import the SQL Testing Tools to your project:
``` python
# ensure to always use the latest version of sql_testing_tools
import os
os.system('pip install -U sql_testing_tools')

# import sql_testing_tools
import sql_testing_tools.BaseAccess as Ba
import sql_testing_tools.Helper as He
```

On global level of your test class, set the SQLite database you want to use (bases must be located in the repository of the test class, no DBs contained in sql_testing_tools).
``` python
import unittest 
class TestClass(unittest.TestCase):
    Ba.setDBName("databases/ladepunkte.db") 
```

The following methods are available for use in test methods:
``` python
try:
    Ba.runAndGetStringTable_fromFile("sqlfile.sql")
except Exception as e:
    # the execution failed 
    # (usually due to syntax or database errors)
    self.fail(e)

# (optional) set the files to be compared. The sql strings will 
# be normalized and used for all following methods (to improve 
# performance), until new  files are set. Arguments that are
# None or "" are ignored and the sql string remains the same.
# Raises an Exception if one of the files is empty.
setup("sqlfile.sql","solution.sql")

# All following methods call setup(sql,sol) before executing 
# anything else. Call without arguments to keep the last 
# normalized sql strings (and improve performance).
# Each check was successfull if "" is returned. Returns a 
# German error message if not.
# Each method compares the normalized string between the start
# keyword and the next keyword or ;

res = He.checkColumns() # starts to search at keyword "SELECT"
res = He.checkTables() # starts to search at keyword "FROM"
res = He.checkCondition() # starts to search at keyword "WHERE"
res = He.checkOrder() # starts to search at keyword "ORDER BY"
res = He.checkGroup() # starts to search at keyword "GROUP BY"

# can not be called with new sql files
res = checkKeywords("startKeyword",["end","keywords"]) 

# compares equality of the full normalized sql strings and if 
# not equal uses the Cosette API (cosette.cs.washington.edu)
# for comparison. A file 'cosette_apikey.txt' with only the 
# apikey in it on root level of the test repository is required 
# to use this feature. If not existant, only the string comparison
# is performed.
# Warning: Cosette is not maintained!
res = checkEquality()
```









### Changelog

##### V0.2.4
- Added more check methods for single parts of queries: checkColumns, checkTables, checkCondition, checkOrder, checkGroup, checkKeywords

##### V 0.2.3
- fix: ASC/DESC in ORDER BY (also with multiple columns and order directions), no direction treated as ASC
- Verified that ; and whitespaces, linebreaks at end of query are ignored

##### V 0.2.2 
- Support LIKE
- Support '<=' and '>=' (geq and leq)

##### V 0.2.1
- Support LIMIT
  
##### V 0.1.9 + 0.2.0
- Support ORDER BY

##### V 0.1.8
- Fixed linebreak problems: Linebreaks are now converted into whitespaces before parsing where tokens

##### V 0.1.6 + V 0.1.7
- Fixed import error to ensure imports working in different environments

##### V 0.1.4 + V 0.1.5
- Chained conditions (with AND,OR and Paranthesises) in WHERE statement
- Aggregate Functions

##### V 0.1.3
- SELECT: columns with our without table prefix
- FROM: one or more table from DB; no queries as tables!
- WHERE: single conditions; no Paranthesises!
- GROUP BY one or more columns

