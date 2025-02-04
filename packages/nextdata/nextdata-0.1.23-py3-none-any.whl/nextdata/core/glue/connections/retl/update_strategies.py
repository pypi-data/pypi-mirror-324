from enum import Enum

import sqlalchemy as sa


class TableUpdateStrategy(Enum):
    MATERIALIZED_VIEW = "materialized_view"
    PARTITION = "partition"
    TABLE_SWAP = "table_swap"
    VIEW = "view"


class DatabaseFeatures:
    def __init__(self, engine: sa.Engine) -> None:
        self.engine = engine
        self.dialect = engine.dialect.name

    def supports_materialized_views(self) -> bool:
        return self.dialect in ["postgresql"]

    def supports_concurrent_refresh(self) -> bool:
        if not self.supports_materialized_views():
            return False
        return self.dialect == "postgresql"

    def supports_partitioning(self) -> bool:
        return self.dialect in ["postgresql", "mysql", "oracle"]

    def supports_views(self) -> bool:
        return self.dialect in ["postgresql", "mysql", "oracle", "mssql"]

    def get_optimal_strategy(self) -> TableUpdateStrategy:
        if self.supports_materialized_views() and self.supports_concurrent_refresh():
            return TableUpdateStrategy.MATERIALIZED_VIEW
        if self.supports_partitioning():
            return TableUpdateStrategy.PARTITION
        if self.supports_views():
            return TableUpdateStrategy.VIEW
        return TableUpdateStrategy.TABLE_SWAP
