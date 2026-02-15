def extract_id_usd(file_path):

    raw = pd.read_excel(file_path, header=None)

    header_row = None
    for i, row in raw.iterrows():
        row_text = row.astype(str).str.lower().tolist()
        if "id" in row_text and "value in usd" in row_text:
            header_row = i
            break

    if header_row is None:
        raise ValueError(f"Header not found in {file_path.name}")

    df = pd.read_excel(file_path, header=header_row)

    def find_col(cols, target):
        for c in cols:
            if target in c.lower():
                return c

    id_col = find_col(df.columns, "id")
    usd_col = find_col(df.columns, "value")

    out = df[[id_col, usd_col]].dropna(subset=[id_col])
    out.columns = ["ID", "USD_Value"]

    return out
