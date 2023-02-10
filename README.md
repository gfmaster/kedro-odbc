# kedro-odbc

## Introduction

kedro-odbc provides ODBCQueryDataSet, which makes pyODBC connection and passes to pandas.read_sql(), instead of SQLAlchemy engine object. I needed this because of Tibero database, which has some market share in South Korea. Tibero does not provide SQLAlchemy dialect plugin, thus the need for dataset that accepts vanilla pyodbc connection.

## Requirement
pyodbc

'Tibero 6 ODBC Driver' installed

kedro < 0.19


Kedro sourcecode says 
```
# NOTE: kedro.extras.datasets will be removed in Kedro 0.19.0.
# Any contribution to datasets should be made in kedro-datasets
# in kedro-plugins (https://github.com/kedro-org/kedro-plugins)
```

This dataset is simply subclass of SQLQueryDataSet with create_connection() class method overriden with using pyodbc. Therefore if kedro 0.19 changes DataSet class method hierarchy, ODBCQueryDataSet will raise error.

# Installation
Copy odbc_dataset.py into \<your kedro project base folder\>/src/\<your kedro project name\>/extras/dataset/

# Usage

Examine example setup below.

credentials.yml
```yaml
tibero_connection:
    con: DRIVER={Tibero 6 ODBC Driver};SERVER=172.0.0.1;PORT=8629;DB=MYDB;UID=myuser;PWD=mysupersecretpasswordpleasechangeme
```

catalog.yml
```yaml
tibero_test:
  type: my_kedro_project.extras.datasets.odbc_dataset.ODBCQueryDataSet
  sql: "SELECT * FROM TEST_TABLE WHERE ROWNUM <=30;"
  credentials: tibero_connection

tibero_test_csv:
  type: pandas.CSVDataSet
  filepath: data/01_raw/tibero_test.csv

```

pipeline.py
```python
# previous lines are omitted
node(
    func=passthrough,
    inputs=['tibero_test'],
    outputs='tibero_test_csv',
    name='tib1'
),
# other lines are omitted, too
```

