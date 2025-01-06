import pandas as pd


def read_file(file_path, filters=None):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Le fichier doit être au format CSV ou XLSX")

    if filters:
        for key, value in filters.items():
            if key in df.columns:
                df = df[df[key] == value]
            else:
                raise ValueError(f"Filtre non valide : '{key}' non trouvé dans les colonnes")

    return df.to_dict(orient='records')
