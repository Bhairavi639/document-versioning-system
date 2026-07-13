from itertools import combinations


def detect_key_columns(df,
                        uniqueness_threshold=0.95,
                        nonnull_threshold=0.95):
    """
    Detect the best key columns for a dataframe.

    Priority:
    1. Single-column keys
    2. Two-column composite keys
    3. Fallback to row index
    """

    total_rows = max(len(df), 1)

    # Empty dataframe
    if total_rows == 0:
        return [], "row_index"

    # -------------------------
    # Step 1: Single-column keys
    # -------------------------
    for col in df.columns:

        nonnull_ratio = (df[col] != "").sum() / total_rows
        unique_ratio = df[col].nunique() / total_rows

        if (
            nonnull_ratio >= nonnull_threshold
            and unique_ratio >= uniqueness_threshold
        ):
            return [col], "single"

    # -------------------------
    # Step 2: Two-column keys
    # -------------------------
    for cols in combinations(df.columns, 2):

        combined = (
            df[list(cols)]
            .astype(str)
            .agg("||".join, axis=1)
        )

        nonnull_ratio = (
            (combined != "||").sum()
            / total_rows
        )

        unique_ratio = (
            combined.nunique()
            / total_rows
        )

        if (
            nonnull_ratio >= nonnull_threshold
            and unique_ratio >= uniqueness_threshold
        ):
            return list(cols), "composite"

    # -------------------------
    # Step 3: Fallback
    # -------------------------
    return [], "row_index"