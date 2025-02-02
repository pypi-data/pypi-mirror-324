import os
import pandas as pd
import datetime
import platform
from typing import Optional, Dict, Any, Union
from .cursor import Cursor
from .exceptions import InterfaceError, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError

class Connection:
    """
    Database connection class that manages DataFrames and cursors
    DataFrameとカーソルを管理するデータベース接続クラス
    """
    def __init__(self, base_dir: str = ".", dataframes: Optional[Dict[str, pd.DataFrame]] = None):
        """
        Initialize connection with base directory and optional dataframes
        基準ディレクトリとオプションのDataFrameで接続を初期化

        Args:
            base_dir (str): Base directory for CSV files
                           CSVファイルの基準ディレクトリ
            dataframes (Dict[str, pd.DataFrame], optional): Dictionary of table names and their DataFrames
                                                          テーブル名とDataFrameの辞書
        """
        self.base_dir = base_dir
        self._tables: Dict[str, pd.DataFrame] = {}
        self._schemas: Dict[str, Dict] = {}
        
        # Register initial dataframes if provided
        # 初期DataFrameが提供された場合に登録
        if dataframes:
            for table_name, df in dataframes.items():
                self._tables[table_name] = df.copy()

    @property
    def tables(self) -> Dict[str, pd.DataFrame]:
        """
        Get registered tables
        登録されているテーブルを取得

        Returns:
            Dict[str, pd.DataFrame]: Dictionary of table names and their DataFrames
                                   テーブル名とDataFrameの辞書
        """
        return self._tables

    def create_table(self, name: str, schema: dict) -> None:
        """Create a new table
        テーブルを作成

        Args:
            name (str): Table name
                       テーブル名
            schema (dict): Column names and their types
                          カラム名と型の定義

        Raises:
            ProgrammingError: When table name is invalid
                             テーブル名が無効な場合
            DataError: When schema definition is invalid
                      スキーマ定義が無効な場合
            DatabaseError: For other database operation errors
                          その他のデータベース操作エラー
        """
        if not name or not isinstance(name, str):
            raise ProgrammingError("Invalid table name")
        if not schema or not isinstance(schema, dict):
            raise DataError("Invalid schema definition")
        if name in self._tables:
            raise IntegrityError(f"Table {name} already exists")

        try:
            df = pd.DataFrame(columns=schema.keys())
            df = self._convert_dataframe_types(df, schema)
            self._tables[name] = df
            self._schemas[name] = schema
        except ValueError as e:
            raise DataError(f"Failed to convert data types: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Failed to create table: {str(e)}")

    def register_table(self, name: str, dataframe: Any, schema: dict) -> None:
        """Register existing DataFrame as a table
        既存のDataFrameをテーブルとして登録

        Args:
            name (str): Table name
                       テーブル名
            dataframe: pandas DataFrame
                      pandas DataFrame
            schema (dict): Column names and their types
                          カラム名と型の定義

        Raises:
            ProgrammingError: When table name or schema is invalid
                             テーブル名やスキーマが無効な場合
            DataError: When DataFrame type conversion fails
                      DataFrameの型変換に失敗した場合
            IntegrityError: When table already exists
                           テーブルが既に存在する場合
        """
        if not name or not isinstance(name, str):
            raise ProgrammingError("Invalid table name")
        if name in self._tables:
            raise IntegrityError(f"Table {name} already exists")
        if not isinstance(dataframe, pd.DataFrame):
            raise ProgrammingError("dataframe must be a pandas DataFrame")

        try:
            dataframe = self._convert_dataframe_types(dataframe, schema)
            self._tables[name] = dataframe
            self._schemas[name] = schema
        except ValueError as e:
            raise DataError(f"Failed to convert data types: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Failed to register table: {str(e)}")

    def register_schema(self, name: str, schema: dict) -> None:
        """Register schema for a table
        テーブルのスキーマを登録

        Args:
            name (str): Table name
                       テーブル名
            schema (dict): Column names and their types
                          カラム名と型の定義

        Raises:
            ProgrammingError: When table name or schema is invalid
                             テーブル名やスキーマが無効な場合
            DataError: When DataFrame type conversion fails
                      DataFrameの型変換に失敗した場合
        """
        if not name or not isinstance(name, str):
            raise ProgrammingError("Invalid table name")
        if not schema or not isinstance(schema, dict):
            raise DataError("Invalid schema definition")
        if name not in self._tables:
            raise ProgrammingError(f"Table {name} does not exist")

        try:
            df = self._convert_dataframe_types(self._tables[name], schema)
            self._tables[name] = df
            self._schemas[name] = schema
        except ValueError as e:
            raise DataError(f"Failed to convert data types: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Failed to register schema: {str(e)}")

    def _convert_dataframe_types(self, df: pd.DataFrame, schema: dict) -> pd.DataFrame:
        """Convert DataFrame types based on schema
        データフレームの型をスキーマに基づいて変換

        Args:
            df (pd.DataFrame): Target DataFrame
                             変換対象のDataFrame
            schema (dict): Type definitions
                          型定義

        Returns:
            pd.DataFrame: DataFrame with converted types
                         型変換後のDataFrame

        Raises:
            DataError: When type conversion fails
                      型変換に失敗した場合
            ValueError: When type definition is invalid
                       無効な型定義の場合
        """
        valid_types = {"INTEGER", "REAL", "BOOLEAN", "DATE", "TEXT"}
        try:
            for col, dtype in schema.items():
                if dtype not in valid_types:
                    raise ValueError(f"Invalid data type: {dtype}")
                
                if dtype == "INTEGER":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif dtype == "REAL":
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                elif dtype == "BOOLEAN":
                    df[col] = df[col].map(lambda x: x.lower() == "true" if isinstance(x, str) else bool(x))
                elif dtype == "DATE":
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
            return df
        except ValueError as e:
            raise DataError(f"Failed to convert data types: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error occurred: {str(e)}")

    def _get_csv_path(self, table_name: str) -> str:
        """Get CSV file path for the table
        テーブルに対応する CSV ファイルのパスを取得
        """
        return os.path.join(self.base_dir, f"{table_name}.csv")

    def commit(self) -> None:
        """Save changes to CSV files
        変更をCSVファイルに保存

        Raises:
            OperationalError: When file operation fails
                             ファイル操作に失敗した場合
            DatabaseError: For other database operation errors
                          その他のデータベース操作エラー
        """
        try:
            for table_name, df in self._tables.items():
                file_path = self._get_csv_path(table_name)
                df.to_csv(file_path, index=False)
        except OSError as e:
            raise OperationalError(f"Failed to save file: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Failed to commit: {str(e)}")

    def rollback(self) -> None:
        """Restore to last saved CSV state
        最後に保存したCSVの状態に戻す

        Raises:
            OperationalError: When file operation fails
                             ファイル操作に失敗した場合
            DataError: When data loading fails
                      データの読み込みに失敗した場合
            DatabaseError: For other database operation errors
                          その他のデータベース操作エラー
        """
        try:
            for table_name in list(self._tables.keys()):
                file_path = self._get_csv_path(table_name)
                if not os.path.exists(file_path):
                    raise OperationalError(f"File does not exist: {file_path}")
                
                try:
                    df = pd.read_csv(file_path, dtype=str)
                    df = self._convert_dataframe_types(df, self._schemas.get(table_name, {}))
                    self._tables[table_name] = df
                except pd.errors.EmptyDataError:
                    raise DataError(f"Empty CSV file: {file_path}")
                except pd.errors.ParserError:
                    raise DataError(f"Failed to parse CSV file: {file_path}")
        except (OperationalError, DataError):
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to rollback: {str(e)}")

    def cursor(self) -> Cursor:
        """Get cursor object
        カーソルオブジェクトを取得

        Returns:
            Cursor: New cursor object
                   新しいカーソルオブジェクト

        Raises:
            InterfaceError: When cursor creation fails
                           カーソルの作成に失敗した場合
        """
        try:
            return Cursor(self)
        except Exception as e:
            raise InterfaceError(f"Failed to create cursor: {str(e)}")

    def close(self) -> None:
        """Close the connection
        接続を閉じる
        """
        self._tables.clear()

    def get_table(self, table_name: str) -> pd.DataFrame:
        """
        Retrieve a table DataFrame by name. If not registered, attempt to load from a CSV file in the base directory.
        登録されていないテーブル名の場合、基準ディレクトリから CSV ファイルを読み込み登録する。

        Args:
            table_name (str): The name of the table.

        Returns:
            pd.DataFrame: The DataFrame associated with the table.

        Raises:
            FileNotFoundError: If the CSV file is not found in the base directory.
            DataError: If reading the CSV file fails.
        """
        print("DEBUG: Entering get_table with table_name =", table_name)
        if table_name in self._tables:
            print("DEBUG: Table found in registered tables.")
            return self._tables[table_name]

        import os
        file_path = os.path.join(self.base_dir, f"{table_name}.csv")
        if not os.path.exists(file_path):
            print("DEBUG: CSV file does not exist for table", table_name)
            raise FileNotFoundError(f"CSV file for table {table_name} not found at {file_path}")

        try:
            df = pd.read_csv(file_path)
            self._tables[table_name] = df
            print("DEBUG: CSV file loaded and table registered for", table_name)
            return df
        except Exception as e:
            print("DEBUG: Failed to read CSV file for table", table_name, "Error:", e)
            from .exceptions import DataError
            raise DataError(f"Failed to load CSV file for table {table_name}: {e}")

