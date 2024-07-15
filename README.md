# UFS Data Lake: Progetto di MongoDB
Progetto di Data Lake per MongoDB

per eseguire l'interfaccia installate i requirements ed eseguite:
```
streamlit run Homepage.py
```
In alternativa il progetto è fluibile su questo sito: https://mongolake.streamlit.app/

## Pagine e funzioni

### Homepage
- è possibile visualizzare tutti i concerti in ordine ascendente
    - Di base vengono visualizzati solo quelli futuri. Attraverso un pulsante in alto è possibile visualizzare anche quelli passati
- Dalla scheda "filters" è possibile caricare tutta una serie di filtri per le ricerche
- è possibile filtrare per:
    - Nome evento
    - Artista
    - Tags
    - Intervallo di Date
    - Luogo (che viene convertito in coordinate)
    - Distanza da un luogo
- I filtri vengono processati e caricati in una query "find" che è possibile visualizzare in tempo reale
- è possibile aggiungere al carrello ogni evento che abbia posti disponibili e non sia passato

### Cart
- è possibile acquistare i biglietti aggiungere al carrello. Ogni biglietto genera un codice univoco uuid.
- Una volta acquistati i biglietti emessi vengono salvati in una collection specifica

### Load
- Schermata per aggiungere eventi, artisti e locations al database.
- Per poter aggiungere un evento bisogna prima aggiungere un artista e una location
