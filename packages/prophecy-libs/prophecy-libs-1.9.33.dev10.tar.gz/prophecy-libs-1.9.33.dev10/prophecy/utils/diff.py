from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DataType,
    NullType,
    BooleanType,
    IntegerType,
    LongType,
    FloatType,
    DoubleType,
    DecimalType,
    DateType,
    TimestampType,
    StringType,
)
import uuid

COMPUTED_DIFFS = {}

def get_precedence(dt: DataType) -> int:
    """
    Assign a numeric precedence/rank to Spark data types.
    Lower value = narrower type, Higher value = broader type.
    """
    if isinstance(dt, NullType):
        # Null can be promoted to anything else
        return 0
    elif isinstance(dt, BooleanType):
        return 1
    elif isinstance(dt, IntegerType):
        return 2
    elif isinstance(dt, LongType):
        return 3
    elif isinstance(dt, FloatType):
        return 4
    elif isinstance(dt, DoubleType):
        return 5
    elif isinstance(dt, DecimalType):
        # Treat decimal as broader than basic floats/doubles for numeric contexts
        return 6
    elif isinstance(dt, DateType):
        return 7
    elif isinstance(dt, TimestampType):
        return 8
    elif isinstance(dt, StringType):
        return 9
    # Fallback for complex or unhandled types
    return 99


def find_common_type(dt1: DataType, dt2: DataType) -> DataType:
    """
    Find a 'common' Spark data type for dt1 and dt2 based on simplified precedence rules.
    """
    # If they're exactly the same (including decimal precision/scale), just return dt1
    if dt1 == dt2:
        return dt1

    # Both are DecimalType but differ in precision or scale
    if isinstance(dt1, DecimalType) and isinstance(dt2, DecimalType):
        # Pick the "wider" decimal
        precision = max(dt1.precision, dt2.precision)
        scale = max(dt1.scale, dt2.scale)
        return DecimalType(precision=precision, scale=scale)

    # If either is NullType, pick the other
    if isinstance(dt1, NullType):
        return dt2
    if isinstance(dt2, NullType):
        return dt1

    # Otherwise, compare precedence
    prec1 = get_precedence(dt1)
    prec2 = get_precedence(dt2)

    # If both are numeric (including decimals), pick the broader
    numeric_types = (
        BooleanType,
        IntegerType,
        LongType,
        FloatType,
        DoubleType,
        DecimalType,
    )
    if isinstance(dt1, numeric_types) and isinstance(dt2, numeric_types):
        return dt1 if prec1 >= prec2 else dt2

    # Date <-> Timestamp => Timestamp
    if (isinstance(dt1, DateType) and isinstance(dt2, TimestampType)) or (
        isinstance(dt2, DateType) and isinstance(dt1, TimestampType)
    ):
        return TimestampType()

    # In all other cases (e.g. one is StringType, or higher precedence):
    # todo recursive handling for array and struct types.
    return dt1 if prec1 > prec2 else dt2


def align_dataframes_schemas(df1: DataFrame, df2: DataFrame) -> (DataFrame, DataFrame):
    """
    Aligns df1 and df2 so that columns with the same name have the same data type.
    Returns two new DataFrames (df1_aligned, df2_aligned).
    """
    df1_aligned = df1
    df2_aligned = df2

    # Columns that exist in both DataFrames
    common_cols = set(df1.columns).intersection(set(df2.columns))

    for col_name in common_cols:
        dt1 = df1.schema[col_name].dataType
        dt2 = df2.schema[col_name].dataType

        # Determine the common type
        common_dt = find_common_type(dt1, dt2)

        # Important: Compare the entire DataType object, not just the class.
        if dt1 != common_dt:
            df1_aligned = df1_aligned.withColumn(
                col_name, F.col(col_name).cast(common_dt)
            )
        if dt2 != common_dt:
            df2_aligned = df2_aligned.withColumn(
                col_name, F.col(col_name).cast(common_dt)
            )

    return df1_aligned, df2_aligned


def split_df_by_pk_uniqueness(df, key_columns):
    """
    Returns two DataFrames:
      1) df_unique: Rows where 'key_columns' is unique (exactly 1 occurrence)
      2) df_not_unique: Rows where 'key_columns' occur more than once
    """
    # Create a unique column name for counting that does not collide with existing columns
    count_alias = f"__count_{uuid.uuid4().hex}"

    # 1) Group by the key columns and count (using the alias)
    pk_counts = df.groupBy(key_columns).agg(F.count("*").alias(count_alias))

    # 2) Separate the PKs that appear once vs. more than once, and drop the aggregator column
    pk_once = pk_counts.filter(F.col(count_alias) == 1).select(
        *key_columns
    )  # Only select key columns to avoid carrying the count_alias
    pk_not_once = pk_counts.filter(F.col(count_alias) > 1).select(
        *key_columns
    )  # Only select key columns

    # 3) Join with the original df to get rows
    df_unique = df.join(pk_once, on=key_columns, how="inner")
    df_not_unique = df.join(pk_not_once, on=key_columns, how="inner")

    return df_unique, df_not_unique


def create_joined_df(df1, df2, key_columns, value_columns):
    """
    Compare two DataFrames and identify presence in left, right, and differences in values.

    :param df1: First / Calculated DataFrame (left)
    :param df2: Second / Expected DataFrame (right)
    :param key_columns: List of key columns for joining
    :param value_columns: List of value columns to compare
    :return: Resultant DataFrame with key columns, presence flags, and value comparison
    """

    df1, df2 = align_dataframes_schemas(df1, df2)

    # Perform a full outer join on the key columns
    joined_df = df1.alias("left").join(
        df2.alias("right"), on=key_columns, how="full_outer"
    )

    # Compute coalesced key columns and presence flags
    coalesced_keys = [
        F.coalesce(F.col(f"left.{col}"), F.col(f"right.{col}")).alias(col)
        for col in key_columns
    ]

    presence_in_left = (
        F.when(
            F.expr(
                " AND ".join(
                    [
                        f"coalesce(left.{col}, right.{col}) = left.{col}"
                        for col in key_columns
                    ]
                )
            ),
            1,
        )
        .otherwise(0)
        .alias("presence_in_left")
    )

    presence_in_right = (
        F.when(
            F.expr(
                " AND ".join(
                    [
                        f"coalesce(left.{col}, right.{col}) = right.{col}"
                        for col in key_columns
                    ]
                )
            ),
            1,
        )
        .otherwise(0)
        .alias("presence_in_right")
    )

    # Group value columns into left and right structs
    left_struct = F.struct(
        *[F.col(f"left.{col}").alias(col) for col in value_columns]
    ).alias("left_values")
    right_struct = F.struct(
        *[F.col(f"right.{col}").alias(col) for col in value_columns]
    ).alias("right_values")

    # Select the final result
    result_df = joined_df.select(
        *coalesced_keys,  # Coalesced key columns
        presence_in_left,  # Presence flag for left
        presence_in_right,  # Presence flag for right
        left_struct,  # Struct containing left values
        right_struct,  # Struct containing right values
    )

    return result_df


def add_row_matches_column(joined_df):
    """
    Adds a new column 'row_matches' to the DataFrame that indicates whether
    the values in 'left_values' and 'right_values' columns are equal.
    """

    left_struct = "left_values"
    right_struct = "right_values"
    return joined_df.withColumn(
        "row_matches", F.expr(f"{left_struct} = {right_struct}")
    )


def add_column_comparison_results(joined_df):
    """
    Adds a new column to the DataFrame containing comparison results between two struct columns.

    This function compares corresponding fields within two specified struct columns (`left_struct` and `right_struct`)
    and aggregates the comparison results into a new struct column (`comparison_struct`). Each field in the new struct
    indicates whether the corresponding fields in the input structs are equal.
    """
    left_struct = "left_values"
    right_struct = "right_values"
    comparison_struct = "compared_values"

    # Retrieve the list of fields from the left struct column
    left_fields = joined_df.select(f"{left_struct}.*").columns

    # Generate comparison expressions for each field in the struct
    comparison_expressions = [
        (F.col(f"{left_struct}.{field}") == F.col(f"{right_struct}.{field}")).alias(
            field
        )
        for field in left_fields
    ]

    # Combine individual comparison results into a single struct column
    comparison_struct_col = F.struct(*comparison_expressions)

    # Add the comparison struct column to the DataFrame
    return joined_df.withColumn(comparison_struct, comparison_struct_col)


def compute_mismatch_summary(joined_df):
    """
    Computes summary statistics for mismatches across specified columns in the joined DataFrame.

    This function calculates:
    - The number of rows where all specified columns match.
    - The number of rows with at least one mismatch.
    - The total number of mismatches across all specified columns and rows.
    - The count of matches and mismatches for each individual specified column.

    Args:
        joined_df (DataFrame): The input Spark DataFrame containing a `compared_values` struct column
                               with boolean fields indicating match status for each specified column,
                               and a `row_matches` boolean column indicating if the entire row matches.

    Returns:
        DataFrame: A summary DataFrame with the following columns:
            - rows_matching (Long): Number of rows where all specified columns match.
            - rows_not_matching (Long): Number of rows with at least one mismatch.
            - <column>_match_count (Long): Number of matches for each specified column.
            - <column>_mismatch_count (Long): Number of mismatches for each specified column.
    """

    comparison_struct = "compared_values"

    fields = joined_df.select(f"{comparison_struct}.*").columns

    # Build aggregators for match and mismatch counts for each specified column
    per_column_aggregators = []
    for column in fields:
        # Aggregator for the number of matches in the current column
        match_aggregator = F.sum(
            F.when(F.col(f"{comparison_struct}.{column}"), 1).otherwise(0)
        ).alias(f"{column}_match_count")
        per_column_aggregators.append(match_aggregator)

        # Aggregator for the number of mismatches in the current column
        mismatch_aggregator = F.sum(
            F.when(~F.col(f"{comparison_struct}.{column}"), 1).otherwise(0)
        ).alias(f"{column}_mismatch_count")
        per_column_aggregators.append(mismatch_aggregator)

    # Aggregate all summary statistics into a single DataFrame
    summary_df = joined_df.agg(
        # Count of rows where all specified columns match
        F.sum(F.when(F.col("row_matches"), 1).otherwise(0)).alias("rows_matching"),
        # Count of rows with at least one mismatch
        F.sum(F.when(~F.col("row_matches"), 1).otherwise(0)).alias("rows_not_matching"),
        # Include all per-column match and mismatch aggregators
        *per_column_aggregators,
    )

    return summary_df


def get_value_columns(df1, df2, key_columns):
    _all_columns = set(df1.columns).union(set(df2.columns))
    return list(_all_columns - set(key_columns))


def get_columns_schema(df):
    return [
        {"name": field.name, "type": str(field.dataType)} for field in df.schema.fields
    ]


def get_diff_summary_dict(summary_df,value_columns):
    summary_row = summary_df.collect()[0].asDict()
    rows_matching = summary_row["rows_matching"]
    rows_not_matching = summary_row["rows_not_matching"]

    total_rows = rows_matching + rows_not_matching

    overall_stats = {
        "rows_matching": rows_matching,
        "rows_not_matching": rows_not_matching,
    }

    column_comparisions = {}
    for col in value_columns:
        match_key = f"{col}_match_count"
        mismatch_key = f"{col}_mismatch_count"

        match_count = summary_row[match_key]
        mismatch_count = summary_row[mismatch_key]

        column_comparisions[col] = {
            "matches": match_count,
            "mismatches": mismatch_count,
        }

    return {"overall_stats": overall_stats, "column_comparisions": column_comparisions}


def create_diff(expected_df, generated_df, key_columns, diff_key):    
    value_columns = get_value_columns(expected_df, generated_df, key_columns)
    joined_df = create_joined_df(
        df1=expected_df, df2=generated_df, key_columns=key_columns, value_columns=value_columns
    )
    joined_df = add_row_matches_column(joined_df)
    joined_df = add_column_comparison_results(joined_df)
    summary_df = compute_mismatch_summary(joined_df)
    # summary_dict = get_diff_summary_dict(summary_df,value_columns)

    COMPUTED_DIFFS[diff_key] = {
        "joined": joined_df,
        "keyCols": key_columns,
        "valueCols": value_columns,
        "expected": expected_df,
        "generated": generated_df,
    }
