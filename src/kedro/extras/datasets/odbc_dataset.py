from typing import Any, Dict, List, NoReturn, Optional
from kedro.extras.datasets.pandas.sql_dataset import SQLQueryDataSet
import pandas as pd
import pyodbc
from datetime import datetime

import copy
import warnings

from kedro.io.core import (
    AbstractDataSet,
    DataSetError,
    get_filepath_str,
    get_protocol_and_path,
)


class ODBCQueryDataSet(SQLQueryDataSet):
    """
    Will load data from database, via pandas.read_sql, but providing pyodbc connection.
    """

    def __init__(  # pylint: disable=too-many-arguments
            self,
            sql: str = None,
            credentials: Dict[str, Any] = None,
            load_args: Dict[str, Any] = None,
            fs_args: Dict[str, Any] = None,
            filepath: str = None,
            execution_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Creates a new ``ODBCQueryDataSet``, by calling super.__init__"""
        super().__init__(sql, credentials, load_args, fs_args, filepath, execution_options)

    @classmethod
    def create_connection(cls, connection_str: str) -> None:
        """ make pyODBC connection instead of SQLAlchemy engine.
        """
        if connection_str in cls.engines:
            return

        try:
            engine = pyodbc.connect(connection_str)
        except ImportError as import_error:
            raise super()._get_missing_module_error(import_error) from import_error
        except NoSuchModuleError as exc:
            raise super()._get_sql_alchemy_missing_error() from exc

        cls.engines[connection_str] = engine

    def _load(self) -> pd.DataFrame:
        load_args = copy.deepcopy(self._load_args)

        # temporarily ignore warning about giving pyodbc connection instead of SQLAlchemy engine.
        warnings.simplefilter("ignore")

        # execution_options are ignored for the time being...
        # engine = self.engines[self._connection_str].execution_options(
        #     **self._execution_options
        # )  # type: ignore
        engine = self.engines[self._connection_str]

        if self._filepath:
            load_path = get_filepath_str(PurePosixPath(self._filepath), self._protocol)
            with self._fs.open(load_path, mode="r") as fs_file:
                load_args["sql"] = fs_file.read()

        return pd.read_sql_query(con=engine, **load_args)

    def _save(self, data: pd.DataFrame) -> None:
        """Not supported. will raise error"""
        return super()._save(data)

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset"""
        return super()._describe()
