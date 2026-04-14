
def neteja_noms_columnes(df):
    """
    Funció per netejar els noms de les columnes d'un DataFrame.
    Elimina espais, converteix a minúscules i reemplaça caràcters especials.
    
    Args:
        df (pd.DataFrame): DataFrame al qual se li vol netejar els noms de les columnes.
    
    Returns:
        pd.DataFrame: DataFrame amb els noms de les columnes netejats.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    return df