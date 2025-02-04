from __future__ import annotations

import datetime
import uuid
from typing import Any, Callable

import sqlalchemy as sa
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from sqlalchemy import Column, Date, DateTime, Float, Index, Integer, MetaData, String, Table, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from nextdata.core.glue.connections.jdbc import RemoteDBConnection
from nextdata.core.glue.connections.retl.update_strategies import (
    DatabaseFeatures,
    TableUpdateStrategy,
)


class RetlWriteError(Exception):
    """Exception raised when a retl write operation fails."""


class Base(DeclarativeBase):
    pass


class RetlOutputHistory(Base):
    __tablename__ = "retl_output_history"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    table_name: Mapped[str] = mapped_column(String)


class RetlDbConnection(RemoteDBConnection):
    def __init__(self, url: str, connect_args: dict[str, Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(url, connect_args)
        self.retl_output_history_table = "retl_output_history"
        self.base_table_name = str(kwargs["sql_table"])
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.timestamp_str = self.timestamp.strftime("%Y%m%d%H%M%S")
        self.timestamped_table_name = f"{self.base_table_name}_{self.timestamp_str}"
        metadata = Base.metadata
        metadata.create_all(self.engine)
        self.features = DatabaseFeatures(self.engine)
        self.strategy = kwargs.get("force_strategy", self.features.get_optimal_strategy())

    def _dataframe_to_sql_schema(self, df: DataFrame) -> str:
        """Convert a dataframe to a sql schema."""
        return f"({', '.join([f'{col} {dtype}' for col, dtype in df.dtypes])})"

    def _map_dtype_to_sql_type(self, col_name: str, dtype: str) -> Column:
        if dtype == "string":
            return Column(col_name, String)
        if dtype.startswith("int"):
            return Column(col_name, Integer)
        if dtype.startswith(("float", "double")):
            return Column(col_name, Float)
        if dtype.startswith("date"):
            return Column(col_name, Date)
        if dtype.startswith("timestamp"):
            return Column(col_name, DateTime)
        msg = f"Unsupported dtype: {dtype}"
        raise ValueError(msg)

    def create_table_from_df(
        self,
        df: DataFrame,
        indices: list[str | set[str]] | None,
        table_name: str | None = None,
        additional_columns: list[tuple[str, str]] | None = None,
    ) -> None:
        """Create a table."""
        metadata_obj = MetaData()
        columns = []
        created_indices = []
        for col, dtype in df.dtypes:
            columns.append(self._map_dtype_to_sql_type(col, dtype))

        if additional_columns:
            for col, dtype in additional_columns:
                columns.append(self._map_dtype_to_sql_type(col, dtype))

        if indices:
            for idx in indices:
                if isinstance(idx, set):
                    index_name = f"{self.timestamped_table_name}_{'_'.join(idx)}"
                    index = Index(index_name, *idx)
                    created_indices.append(index)
                else:
                    index_name = f"{self.timestamped_table_name}_{idx}"
                    index = Index(index_name, idx)
                    created_indices.append(index)
        table = Table(
            table_name or self.timestamped_table_name,
            metadata_obj,
            *columns,
            *created_indices,
        )
        table.create(self.engine, checkfirst=True)

    def write_to_table(self, df: DataFrame, table_name: str | None = None) -> None:
        """Write data to a table."""
        df.toPandas().to_sql(
            table_name or self.timestamped_table_name,
            self.engine,
            if_exists="append",
            chunksize=10000,
            index=False,
        )

    def add_to_retl_output_history(self) -> None:
        """Add a table to the retl output history."""
        with Session(self.engine) as session:
            output_history = RetlOutputHistory(
                timestamp=self.timestamp,
                table_name=self.base_table_name,
            )
            session.add(output_history)
            session.commit()

    def cleanup_old_tables(self, keep_n_tables: int) -> None:
        """Cleanup old tables."""
        with Session(self.engine) as session:
            all_tables = (
                session.query(RetlOutputHistory)
                .filter(
                    RetlOutputHistory.table_name == self.base_table_name,
                )
                .order_by(RetlOutputHistory.timestamp.asc())
                .all()
            )
            # drop the tables
            for table in all_tables[:-keep_n_tables]:
                timestamped_table_name = (
                    f"{self.base_table_name}_{table.timestamp.strftime('%Y%m%d%H%M%S')}"
                )
                session.execute(sa.text(f"DROP TABLE IF EXISTS {timestamped_table_name}"))

            # delete the rows from the retl_output_history table
            drop_ids = [table.id for table in all_tables[:-keep_n_tables]]
            session.query(RetlOutputHistory).filter(RetlOutputHistory.id.in_(drop_ids)).delete()
            session.commit()

    def _write_materialized_view(self, df: DataFrame, indices: list[str | set[str]] | None) -> None:
        """Write the result of a retl job to a materialized view."""
        with Session(self.engine) as session:
            self.create_table_from_df(df, indices, table_name=self.timestamped_table_name)
            self.write_to_table(df, table_name=self.timestamped_table_name)
            # Create materialized view if it doesn't exist
            session.execute(
                sa.text(f"""
                CREATE MATERIALIZED VIEW IF NOT EXISTS {self.base_table_name}_mv 
                AS SELECT * FROM {self.timestamped_table_name}
                WITH NO DATA
            """),
            )

            # Refresh the materialized view concurrently
            try:
                session.execute(
                    sa.text(f"""
                    REFRESH MATERIALIZED VIEW CONCURRENTLY {self.base_table_name}_mv
                """),
                )
            except Exception as e:
                if "concurrent refresh is not enabled" in str(e).lower():
                    # Fall back to regular refresh
                    session.execute(
                        sa.text(f"""
                        REFRESH MATERIALIZED VIEW {self.base_table_name}_mv
                        """),
                    )
                else:
                    raise
            session.commit()

    def _write_partitioned(self, df: DataFrame, indices: list[str | set[str]] | None) -> None:
        """Write the result of a retl job to a partitioned table."""
        version_col = "version"

        with Session(self.engine) as session:
            # Create partitioned table if it doesn't exist
            version_col = ("version", "timestamp")
            self.create_table_from_df(
                df,
                indices,
                table_name=self.base_table_name,
                additional_columns=[version_col],
            )

            # Create new partition
            partition_name = self.timestamped_table_name
            session.execute(
                sa.text(f"""
                CREATE TABLE IF NOT EXISTS {partition_name} 
                PARTITION OF {self.base_table_name} 
                FOR VALUES IN ('{self.timestamp}')
            """),
            )

            # Write data to new partition
            df_with_version = df.withColumn(version_col[0], F.lit(self.timestamp))
            self.write_to_table(df_with_version, table_name=partition_name)

            # Update default partition
            session.execute(
                sa.text(f"""
                ALTER TABLE {self.base_table_name} 
                EXCHANGE PARTITION ({version_col}) 
                WITH TABLE {partition_name}
            """),
            )
            session.commit()

    def _write_view(self, df: DataFrame, indices: list[str | set[str]] | None) -> None:
        """Write the result of a retl job to a view."""
        with Session(self.engine) as session:
            # Write new data to timestamped table
            self.create_table_from_df(df, indices, table_name=self.timestamped_table_name)
            self.write_to_table(df, table_name=self.timestamped_table_name)

            # Drop existing view if it exists
            session.execute(sa.text(f"DROP VIEW IF EXISTS {self.base_table_name}"))

            # Create new view pointing to latest table
            session.execute(
                sa.text(f"""
                CREATE VIEW {self.base_table_name} AS 
                SELECT * FROM {self.timestamped_table_name}
            """),
            )
            session.commit()

    def _write_table_swap(self, df: DataFrame, indices: list[str | set[str]] | None) -> None:
        """Write the result of a retl job to a table swap."""
        temp_table = f"{self.base_table_name}_temp"

        old_table = f"{self.base_table_name}_old"
        with Session(self.engine) as session:
            self.create_table_from_df(df, indices, table_name=temp_table)

            # Write to temp table
            df.toPandas().to_sql(
                temp_table,
                self.engine,
                if_exists="append",
                chunksize=10000,
                index=False,
            )

            # Perform atomic swap
            session.execute(sa.text(f"DROP TABLE IF EXISTS {old_table}"))
            session.execute(
                sa.text(f"ALTER TABLE IF EXISTS {self.base_table_name} RENAME TO {old_table}"),
            )
            session.execute(sa.text(f"ALTER TABLE {temp_table} RENAME TO {self.base_table_name}"))
            session.execute(sa.text(f"DROP TABLE IF EXISTS {old_table}"))
            session.commit()

    def write_retl_result(self, df: DataFrame, indices: list[str | set[str]] | None = None) -> None:
        """Write the result of a retl job to the retl output table."""
        if self.strategy == TableUpdateStrategy.MATERIALIZED_VIEW:
            self._write_with_rollback(df, indices, self._write_materialized_view)
        elif self.strategy == TableUpdateStrategy.PARTITION:
            self._write_with_rollback(df, indices, self._write_partitioned)
        elif self.strategy == TableUpdateStrategy.VIEW:
            self._write_with_rollback(df, indices, self._write_view)
        else:  # TABLE_SWAP
            self._write_with_rollback(df, indices, self._write_table_swap)

        self.add_to_retl_output_history()
        self.cleanup_old_tables(keep_n_tables=3)

    def _write_with_rollback(
        self,
        df: DataFrame,
        indices: list[str | set[str]] | None,
        write_func: Callable[[DataFrame, list[str | set[str]] | None], None],
    ) -> None:
        """Execute write operation with rollback on failure."""
        try:
            write_func(df, indices)
        except Exception as e:
            with Session(self.engine) as session:
                session.rollback()
            msg = f"Failed to write data: {e!s}"
            raise RetlWriteError(msg) from e
