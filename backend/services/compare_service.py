from utils.excel_reader import get_sheet_names, read_sheet
from utils.key_detector import detect_key_columns
import pandas as pd


def compare_excel(file1_path, file2_path):

    differences = []

    # Get sheet names
    sheets1 = set(get_sheet_names(file1_path))
    sheets2 = set(get_sheet_names(file2_path))

    common_sheets = sheets1.intersection(sheets2)

    # Added and removed sheets
    for sheet in sheets2 - sheets1:
        differences.append({
            "sheet": sheet,
            "key": "",
            "column": "",
            "type": "Sheet Added",
            "old": "",
            "new": sheet
        })

    for sheet in sheets1 - sheets2:
        differences.append({
            "sheet": sheet,
            "key": "",
            "column": "",
            "type": "Sheet Removed",
            "old": sheet,
            "new": ""
        })

    # Compare common sheets
    for sheet in common_sheets:

        df1 = read_sheet(file1_path, sheet)
        print("\nSHEET =", sheet)
        print(df1.head(10))
        df2 = read_sheet(file2_path, sheet)

        # Skip non-data sheets
        print("Sheet:", sheet)
        print("df1 shape =", df1.shape)
        print("df2 shape =", df2.shape)

        if sheet.lower() == "info":
            print(f"Skipping {sheet}")
            continue

        # Handle Change Log separately
        if sheet.lower() == "change log":

            # Summary row
            differences.append({
                "sheet": sheet,
                "key": "Change Log",
                "column": "",
                "type": "Summary",
                "old": f"{len(df1)} entries",
                "new": f"{len(df2)} entries"
            })

            # Added entries
            for _, row in df2.iterrows():

                if row["Change"] not in df1["Change"].astype(str).values:

                    differences.append({
                        "sheet": sheet,
                        "key": str(row["Date"]),
                        "column": "Change",
                        "type": "Log Added",
                        "old": "",
                        "new": str(row["Change"])
                    })

            # Removed entries
            for _, row in df1.iterrows():

                if row["Change"] not in df2["Change"].astype(str).values:

                    differences.append({
                        "sheet": sheet,
                        "key": str(row["Date"]),
                        "column": "Change",
                        "type": "Log Removed",
                        "old": str(row["Change"]),
                        "new": ""
                    })

            continue


        # ✅ Skip non-tabular sheets (IMPORTANT FIX)
        if (
            len(df1.columns) < 2
            or len(df2.columns) < 2
        ):
            print(f"Skipping sheet '{sheet}'")
            continue
            

        if df1.shape[0] == 0 or df2.shape[0] == 0:
            print(f"Skipping sheet '{sheet}' (no rows)")
            continue

        # Detect key columns
        print("\n-------------------")
        print("Sheet:", sheet)
        print("DF1 Columns:", list(df1.columns))
        print("DF2 Columns:", list(df2.columns))



        common_cols = [
            col
            for col in df1.columns
            if col in df2.columns
        ]

        df1_common = df1[common_cols]
        df2_common = df2[common_cols]

        key_cols, method = detect_key_columns(df1_common)

        if not key_cols:
            key_cols, method = detect_key_columns(df2_common)

        print("\n====================")
        print("Sheet:", sheet)
        print("Method:", method)
        print("Key Columns:", key_cols)
        print("Columns:", list(df1.columns))
        print("====================")



        print("====================")
        # fallback if df1 fails
        if not key_cols:
            key_cols, method = detect_key_columns(df2)

        # ---------- ROW INDEX FALLBACK ----------
        if method == "row_index":

            max_rows = max(len(df1), len(df2))

            common_columns = list(
                set(df1.columns).union(set(df2.columns))
            )

            for i in range(max_rows):

                for col in common_columns:

                    old_val = ""

                    new_val = ""

                    if (
                        i < len(df1)
                        and col in df1.columns
                    ):
                        old_val = str(df1.iloc[i][col])

                    if (
                        i < len(df2)
                        and col in df2.columns
                    ):
                        new_val = str(df2.iloc[i][col])

                    if old_val != new_val:

                        if old_val == "":
                            change_type = "Added"

                        elif new_val == "":
                            change_type = "Removed"

                        else:
                            change_type = "Modified"

                        differences.append({
                            "sheet": sheet,
                            "key": f"Row {i+2}",
                            "column": col,
                            "type": change_type,
                            "old": old_val,
                            "new": new_val
                        })

        # ---------- KEY-BASED COMPARISON ----------
        else:

            df1_copy = df1.copy()
            df2_copy = df2.copy()

            df1_copy["__key__"] = (
                df1_copy[key_cols]
                .astype(str)
                .agg("||".join, axis=1)
            )

            df2_copy["__key__"] = (
                df2_copy[key_cols]
                .astype(str)
                .agg("||".join, axis=1)
            )

            df1_copy = df1_copy.set_index("__key__")
            df2_copy = df2_copy.set_index("__key__")

            keys1 = set(df1_copy.index)
            keys2 = set(df2_copy.index)

            # Added records
            for key in keys2 - keys1:

                differences.append({
                    "sheet": sheet,
                    "key": key.replace("||", " | "),
                    "column": "",
                    "type": "Record Added",
                    "old": "",
                    "new": "Entire Record Added"
                })

            # Removed records
            for key in keys1 - keys2:

                differences.append({
                    "sheet": sheet,
                    "key": key,
                    "column": "",
                    "type": "Record Removed",
                    "old": "Entire Record Removed",
                    "new": ""
                })

            # Modified records
            for key in keys1.intersection(keys2):

                common_columns = list(
                    set(df1.columns).union(set(df2.columns))
                )

                for col in common_columns:

                    if col == "__key__":
                        continue

                    old_val = ""

                    new_val = ""

                    if col in df1.columns:
                        old_val = df1_copy.loc[key][col]

                    if col in df2.columns:
                        new_val = df2_copy.loc[key][col]
                    
                    old_val = "" if pd.isna(old_val) else str(old_val)
                    new_val = "" if pd.isna(new_val) else str(new_val)

                    if old_val != new_val:

                        differences.append({
                            "sheet": sheet,
                            "key": key,
                            "column": col,
                            "type": "Modified",
                            "old": old_val,
                            "new": new_val
                        })
        print("\nTOTAL DIFFS =", len(differences))

        for d in differences:
            if d["sheet"] == "Change Log":
                print("CHANGE LOG DIFF:", d)

    return differences