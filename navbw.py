import pandas as pd

def extract_nav(file_path):

    print("\nReading NAV file:", file_path.name)

    # ---------- pass 1: read raw ----------
    raw = pd.read_excel(file_path, header=None)

    header_row = None

    # find header row dynamically
    for i, row in raw.iterrows():
        vals = row.astype(str).str.lower().str.strip().tolist()

        if "id" in vals and any("value" in v and "usd" in v for v in vals):
            header_row = i
            break

    if header_row is None:
        raise ValueError(f"Could not detect NAV header row in {file_path.name}")

    print("Detected header row:", header_row)

    # ---------- pass 2: read with header ----------
    df = pd.read_excel(file_path, header=header_row)

    # normalize column names
    df.columns = df.columns.astype(str).str.strip()

    # ---------- find needed columns ----------
    id_col = None
    nav_col = None

    for c in df.columns:
        c_low = c.lower()

        if id_col is None and c_low == "id":
            id_col = c

        if nav_col is None and ("value" in c_low and "usd" in c_low):
            nav_col = c

    if id_col is None or nav_col is None:
        raise ValueError(f"Required NAV columns not found in {file_path.name}")

    print("Using columns:", id_col, "|", nav_col)

    # ---------- extract ----------
    out = df[[id_col, nav_col]].copy()

    out.columns = ["ID", "NAV"]

    # clean ID
    out["ID"] = out["ID"].astype(str).str.strip()

    # clean NAV numeric
    out["NAV"] = (
        out["NAV"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    out["NAV"] = pd.to_numeric(out["NAV"], errors="coerce")

    # drop junk rows
    out = out.dropna(subset=["ID", "NAV"])

    print("Extracted rows:", len(out))

    return out
