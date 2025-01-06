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
                # Si la colonne est numérique
                if pd.api.types.is_numeric_dtype(df[key]):
                    try:
                        # Cas de filtre supérieur (>)
                        if '>' in value:
                            filter_value = float(value.replace('>', '').strip())
                            df = df[df[key] > filter_value]
                        # Cas de filtre inférieur (<)
                        elif '<' in value:
                            filter_value = float(value.replace('<', '').strip())
                            df = df[df[key] < filter_value]
                        # Cas de filtre égal (=)
                        elif '=' in value:
                            filter_value = float(value.replace('=', '').strip())
                            df = df[df[key] == filter_value]
                        # Cas spécifique pour récupérer les top n éléments
                        elif 'top' in value:
                            try:
                                n = int(value.replace('top', '').strip())
                                df = df.nlargest(n, key)
                            except ValueError:
                                pass
                        else:
                            # Si aucune comparaison n'est spécifiée, utiliser la valeur exacte
                            filter_value = float(value)
                            df = df[df[key] == filter_value]
                    except ValueError:
                        pass
                else:
                    # Si la colonne est de type texte, on applique une comparaison simple
                    if '=' in value:
                        df = df[df[key] == value.replace('=', '').strip()]
                    else:
                        df = df[df[key] == value]
            else:
                raise ValueError(f"Filtre non valide : '{key}' non trouvé dans les colonnes")

    return df.to_dict(orient='records')
