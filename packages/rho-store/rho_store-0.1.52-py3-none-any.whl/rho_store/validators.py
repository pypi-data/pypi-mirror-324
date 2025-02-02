from rho_store.exceptions import InvalidArgument
from rho_store.types import UploadStrategy


def validate_store_df_strategy(strategy: str, table_id: str | None = None, upsert_options: dict | None = None) -> None:
    if strategy not in UploadStrategy.values():
        raise InvalidArgument(f"Invalid strategy: {strategy}")

    if strategy != UploadStrategy.NEW_TABLE.value and table_id is None:
        # if not "new_table" -> table_id is required
        raise InvalidArgument(f"Cannot perform strategy {strategy} without a table_id")

    if strategy == UploadStrategy.UPSERT.value:
        # if "upsert" -> upsert_options is required
        upsert_options = upsert_options or {}
        if not upsert_options.get("columns"):
            raise InvalidArgument(f"Cannot perform strategy {strategy} without valid upsert_options")
