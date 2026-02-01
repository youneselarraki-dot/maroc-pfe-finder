import pandas as pd
from io import BytesIO

def export_to_csv(df: pd.DataFrame) -> str:
    """Exporte un DataFrame en CSV"""
    return df.to_csv(index=False, encoding='utf-8')

def export_to_excel(df: pd.DataFrame) -> bytes:
    """Exporte un DataFrame en Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contacts')
    output.seek(0)
    return output.getvalue()