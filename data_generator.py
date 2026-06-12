import pandas as pd
import random
from datetime import datetime, timedelta

def genera_dati_fittizi(nome_file="bilancio_fittizio.xlsx"):
    categorie_uscite = ["Spesa Alimentare", "Affitto", "Bollette", "Trasporti", "Svago"]
    categorie_entrate = ["Stipendio", "Vendita Usato", "Rimborsi"]
    
    dati = []
    data_inizio = datetime(2025, 1, 1)
    
    # Genera 100 transazioni casuali
    for i in range(100):
        giorni_random = random.randint(0, 365)
        data_transazione = data_inizio + timedelta(days=giorni_random)
        
        tipo = random.choices(["Entrata", "Uscita"], weights=[0.2, 0.8])[0]
        
        if tipo == "Uscita":
            categoria = random.choice(categorie_uscite)
            importo = round(random.uniform(10.0, 500.0), 2)
            if categoria == "Affitto":
                importo = round(random.uniform(600.0, 1000.0), 2)
        else:
            categoria = random.choice(categorie_entrate)
            importo = round(random.uniform(1500.0, 3000.0), 2) if categoria == "Stipendio" else round(random.uniform(50.0, 200.0), 2)
            
        dati.append({
            "Data": data_transazione.strftime("%Y-%m-%d"),
            "Tipo": tipo,
            "Categoria": categoria,
            "Importo_EUR": importo
        })
        
    df = pd.DataFrame(dati)
    df = df.sort_values(by="Data").reset_index(drop=True)
    df.to_excel(nome_file, index=False)
    print(f" File '{nome_file}' generato con successo!")

if __name__ == "__main__":
    genera_dati_fittizi()
