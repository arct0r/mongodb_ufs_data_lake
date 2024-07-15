# UFS Data Lake: Progetto MongoDB

Questo progetto implementa un Data Lake utilizzando MongoDB, con un'interfaccia utente creata tramite Streamlit.

## Installazione e Avvio

Per eseguire l'interfaccia localmente:

1. Installare le dipendenze:
   ```
   pip install -r requirements.txt
   ```

2. Avviare l'applicazione:
   ```
   streamlit run Homepage.py
   ```

In alternativa, è possibile accedere al progetto online all'indirizzo: https://mongolake.streamlit.app/

## Struttura e Funzionalità

### Homepage

- Visualizzazione dei concerti in ordine cronologico ascendente
  - Di default vengono mostrati solo gli eventi futuri
  - Un pulsante permette di includere anche gli eventi passati
- Funzionalità di ricerca avanzata tramite la scheda "Filters"
- Filtri disponibili:
  - Nome evento
  - Artista
  - Tags
  - Intervallo di date
  - Luogo (convertito in coordinate)
  - Distanza da un punto specifico
- Visualizzazione in tempo reale della query MongoDB generata
- Possibilità di aggiungere al carrello eventi con posti disponibili e date future

### Cart

- Gestione dell'acquisto dei biglietti
- Generazione di codici univoci UUID per ogni biglietto
- Salvataggio dei biglietti emessi in una collection dedicata

### Load

- Interfaccia per l'aggiunta di nuovi dati al database:
  - Eventi
  - Artisti
  - Locations
- Nota: Per aggiungere un evento, è necessario prima creare l'artista e la location corrispondenti
