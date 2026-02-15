import pandas as pd
import re

def extract_mtd(file_path):

    print("\nReading MTD file:", file_path.name)

    raw = pd.read_excel(file_path, header=None)

    # ---------- find BridgeId row ----------
    bridge_row = None

    for i, row in raw.iterrows():
        if row.astype(str).str.contains("bridge", case=False).any():
            bridge_row = i
            break

    if bridge_row is None:
        raise ValueError("BridgeId row not found")

    print("Bridge row:", bridge_row)

    mtd_records = []

    row_vals = raw.loc[bridge_row]

    for col_idx, val in row_vals.items():

        if isinstance(val, str) and "bridge" in val.lower():

            # extract ID number
            match = re.search(r'(\d+)', val)
            if not match:
                continue

            fund_id = match.group(1)

            monthly_col = col_idx + 1   # MonthlyGross column

            series = raw.iloc[bridge_row+2:, monthly_col]

            # find last numeric value
            series_num = pd.to_numeric(series, errors="coerce").dropna()

            if len(series_num) == 0:
                continue

            last_val = series_num.iloc[-1]

            mtd_records.append({
                "ID": fund_id,
                "MTD": last_val
            })

            print("MTD found:", fund_id, last_val)

    out = pd.DataFrame(mtd_records)

    print("Extracted MTD rows:", len(out))

    return out
