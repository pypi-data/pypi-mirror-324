import math
from typing import Any, Optional, Union

import numpy as np
import pandas as pd
import polars as pl
import sqlalchemy as sa
from sqlalchemy import Column, MetaData, Table, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine


def _infer_sqlalchemy_type(series: pd.Series) -> type[sa.types.TypeEngine]:
    """
    Infer a basic SQLAlchemy type from a pandas Series dtype.
    This mapping can be expanded as needed.
    """
    dt = series.dtype
    if np.issubdtype(dt, np.integer):
        return sa.Integer
    elif np.issubdtype(dt, np.floating):
        return sa.Float
    elif np.issubdtype(dt, np.datetime64):
        return sa.DateTime
    elif np.issubdtype(dt, np.bool_):
        return sa.Boolean
    else:
        return sa.Text


def _infer_sqlalchemy_type_from_polars_dtype(pl_dtype: Any) -> type[sa.types.TypeEngine]:
    """
    Infer a basic SQLAlchemy type from a Polars dtype.
    This mapping may be extended as needed.
    """
    # Polars integer types
    if pl_dtype in {
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    }:
        return sa.Integer
    # Polars floating types
    elif pl_dtype in {pl.Float32, pl.Float64}:
        return sa.Float
    # Boolean type
    elif pl_dtype == pl.Boolean:
        return sa.Boolean
    # Datetime or Date types
    elif pl_dtype in {pl.Datetime, pl.Date}:
        return sa.DateTime
    # Utf8 (string) type
    elif pl_dtype == pl.Utf8:
        return sa.Text
    else:
        return sa.Text


def write_dataframe_to_postgres(
    df: Union[pd.DataFrame, pl.DataFrame],
    engine: Engine,
    table_name: str,
    dtypes: Optional[dict[str, Any]] = None,
    write_method: str = "upsert",
    chunksize: Optional[Union[int, str]] = None,
    index: Optional[Union[str, list[str]]] = None,
    clean_column_names: bool = False,
    case_type: str = "snake",
    truncate_limit: int = 55,
) -> None:
    """
    Write a DataFrame to a PostgreSQL table with conflict resolution,
    automatic addition of missing columns, optional processing in chunks,
    and support for a custom primary key.

    This function supports both pandas and Polars DataFrames.

    Parameters:
      df:
          The DataFrame to be written to the PostgreSQL table. Can be either a pandas or Polars DataFrame.
      engine:
          SQLAlchemy engine object to connect to the PostgreSQL database.
      table_name:
          The name of the PostgreSQL table to write the DataFrame to.
      dtypes:
          Optional dictionary mapping column names (including primary key columns)
          to SQLAlchemy types. If not provided for a given column, the type is inferred.
      write_method:
          One of the following options (default is 'upsert'):
            - 'insert': Insert rows; if the primary key(s) already exist, skip that row.
            - 'replace': Insert rows; if the primary key(s) already exist, update every
                         non-key column with the new value.
            - 'upsert':  Insert rows; if the primary key(s) already exist, update only those
                         non-key columns whose new value is not null (leaving existing values
                         intact when the new value is null).
      chunksize:
          Either None, a positive integer, or the string "auto". If provided, the data
          will be processed in chunks. When set to "auto", the chunksize is computed as:
              math.floor(30000 / number_of_columns)
          (ensuring the computed chunksize is at least 1).
      index:
          Optional parameter specifying the primary key column(s). For pandas DataFrames,
          if not provided, the DataFrame's index (or MultiIndex) is used. For Polars DataFrames,
          this parameter is required and must be a string or list of strings specifying the primary key column(s).
      clean_column_names:
          If True, the DataFrame's column names will be cleaned using pyjanitors' `clean_names`
          method.
      case_type:
          The case type to pass to pyjanitors' `clean_names` method (default is "snake").
      truncate_limit:
          The truncate limit to pass to pyjanitors' `clean_names` method (default is 55).

    Raises:
      ValueError: If write_method is invalid, if chunksize is invalid, if a Polars
                  DataFrame is passed without specifying the index parameter, or if
                  column cleaning is requested but not supported.
    """

    allowed_methods = ["insert", "replace", "upsert"]
    if write_method not in allowed_methods:
        raise ValueError(f"write_method must be one of {allowed_methods}, got {write_method}")

    # --- Clean column names if requested using pyjanitors ---
    if clean_column_names:
        try:
            # This assumes that the DataFrame has the `clean_names` method (pyjanitor must be installed).
            df = df.clean_names(case_type=case_type, truncate=truncate_limit)
        except AttributeError as e:
            raise ValueError(
                "clean_column_names requested but the DataFrame does not support clean_names. "
                "Please ensure pyjanitors is installed and up-to-date."
            ) from e
        except Exception as e:
            raise ValueError("Error cleaning column names using pyjanitors: " + str(e)) from e

    # --- Determine DataFrame type via module name ---
    module_name = type(df).__module__
    if "polars" in module_name:
        is_polars = True
    elif "pandas" in module_name:
        is_polars = False
    else:
        raise ValueError("df must be either a pandas.DataFrame or a polars.DataFrame")

    # --- Determine primary key columns and prepare records accordingly ---
    pk_names: list[str] = []
    records: list[dict[str, Any]] = []

    if is_polars:
        # For Polars, the caller must supply the index parameter.
        if index is None:
            raise ValueError("For a Polars DataFrame the 'index' parameter is required.")
        if isinstance(index, str):
            pk_names = [index]
        elif isinstance(index, list) and all(isinstance(x, str) for x in index):
            pk_names = index
        else:
            raise ValueError("The 'index' parameter must be a string or a list of strings.")

        # Check that all key columns exist in the DataFrame.
        for key in pk_names:
            if key not in df.columns:
                raise ValueError(f"Primary key column '{key}' not found in the Polars DataFrame.")

        # Get the Polars schema (a dict mapping column names to their dtypes)
        schema: dict[str, Any] = df.schema

        # Build table columns: primary key columns first (in the order specified), then all others.
        table_columns: list[Column] = []
        for col_name in pk_names:
            if dtypes is not None and col_name in dtypes:
                col_type = dtypes[col_name]
            else:
                col_type = _infer_sqlalchemy_type_from_polars_dtype(schema[col_name])
            table_columns.append(Column(col_name, col_type, primary_key=True))
        for col in df.columns:
            if col in pk_names:
                continue
            if dtypes is not None and col in dtypes:
                col_type = dtypes[col]
            else:
                col_type = _infer_sqlalchemy_type_from_polars_dtype(schema[col])
            table_columns.append(Column(col, col_type))

        # Convert the Polars DataFrame to a list of dictionaries.
        records = df.to_dicts()

    else:
        # Pandas DataFrame branch.
        if index is not None:
            if isinstance(index, str):
                pk_names = [index]
            elif isinstance(index, list) and all(isinstance(x, str) for x in index):
                pk_names = index
            else:
                raise ValueError("The 'index' parameter must be a string or a list of strings.")
            # Ensure that all primary key columns exist; if not, reset the index.
            if not all(col in df.columns for col in pk_names):
                df = df.reset_index(drop=False)
        else:
            # Use the DataFrame's index.
            if isinstance(df.index, pd.MultiIndex):
                pk_names = [name if name is not None else f"index_level_{i}" for i, name in enumerate(df.index.names)]
            else:
                pk_names = [df.index.name if df.index.name is not None else "index"]
            df = df.reset_index(drop=False)

        # Build table columns: primary key columns first (in the order specified), then the others.
        table_columns = []
        for col_name in pk_names:
            if dtypes is not None and col_name in dtypes:
                col_type = dtypes[col_name]
            else:
                col_type = _infer_sqlalchemy_type(df[col_name])
            table_columns.append(Column(col_name, col_type, primary_key=True))
        for col in df.columns:
            if col in pk_names:
                continue
            if dtypes is not None and col in dtypes:
                col_type = dtypes[col]
            else:
                col_type = _infer_sqlalchemy_type(df[col])
            table_columns.append(Column(col, col_type))

        # Reorder the DataFrame columns to match the table definition.
        expected_columns: list[str] = [col.name for col in table_columns]
        df = df[expected_columns]
        records = df.to_dict(orient="records")

    # --- Create the SQLAlchemy Table object and update (or create) the schema in Postgres ---
    metadata = MetaData()
    table = Table(table_name, metadata, *table_columns)

    with engine.connect() as conn:
        inspector = sa.inspect(conn)
        if not inspector.has_table(table_name):
            metadata.create_all(conn, tables=[table])
        else:
            # Determine which columns exist in the table.
            existing_columns = {col_info["name"] for col_info in inspector.get_columns(table_name)}
            expected_columns = [col.name for col in table.columns]
            missing_columns = [col for col in expected_columns if col not in existing_columns]
            for col_name in missing_columns:
                col_obj = table.columns[col_name]
                col_type_str = col_obj.type.compile(dialect=engine.dialect)
                alter_stmt = f'ALTER TABLE {table_name} ADD COLUMN "{col_name}" {col_type_str}'
                conn.execute(text(alter_stmt))

    # --- Build the INSERT statement with conflict handling ---
    stmt = insert(table)
    if write_method == "insert":
        stmt = stmt.on_conflict_do_nothing(index_elements=pk_names)
    elif write_method == "replace":
        stmt = stmt.on_conflict_do_update(
            index_elements=pk_names,
            set_={col.name: stmt.excluded[col.name] for col in table.columns if col.name not in pk_names},
        )
    elif write_method == "upsert":
        stmt = stmt.on_conflict_do_update(
            index_elements=pk_names,
            set_={
                col.name: sa.func.coalesce(stmt.excluded[col.name], table.c[col.name])
                for col in table.columns
                if col.name not in pk_names
            },
        )

    # --- Execute the INSERT statement, processing records in chunks if requested ---
    with engine.begin() as conn:
        if chunksize is not None:
            # Validate and/or compute chunksize.
            if isinstance(chunksize, str):
                if chunksize.lower() == "auto":
                    computed_chunksize = math.floor(30000 / (len(records[0]) if records else 1))
                    chunksize = max(1, computed_chunksize)
                else:
                    raise ValueError("chunksize must be a positive integer or 'auto'")
            elif isinstance(chunksize, int):
                if chunksize <= 0:
                    raise ValueError("chunksize must be greater than 0")
            else:
                raise ValueError("chunksize must be a positive integer or 'auto'")

            # Process the records in chunks.
            for i in range(0, len(records), chunksize):
                chunk: list[dict[str, Any]] = records[i : i + chunksize]
                conn.execute(stmt, chunk)
        else:
            conn.execute(stmt, records)
