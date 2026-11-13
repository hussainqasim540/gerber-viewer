# Roadmap e To-Do List Dettagliata per l'MVP del Visualizzatore Gerber (Modulo 2)

## Fase 1: Fondamenta del Backend (API e Parsing)

**Obiettivo:** Creare un servizio backend in grado di ricevere un file zip, processare i file Gerber al suo interno e esporre i dati geometrici e la lista dei layer tramite API.

| ID | Task | Priorità | Dipendenze | Risorse e Tecnologie | Criteri di Accettazione |
|----|------|----------|------------|---------------------|-------------------------|
| **BE-01** | **Setup Progetto Backend** | P1 | - | • Python 3.10+• FastAPI• Uvicorn• Docker & Docker Compose | Un endpoint di health check (`/health`) risponde correttamente quando il servizio viene avviato tramite Docker. |
| **BE-02** | **Endpoint di Upload** | P1 | BE-01 | • FastAPI UploadFile | Un endpoint `POST /api/v1/process-zip` accetta un file `.zip`, lo salva temporaneamente e restituisce un ID di sessione univoco. |
| **BE-03** | **Logica di Decompressione e Identificazione Layer** | P1 | BE-02 | • Python zipfile library• Gerbonara | Il backend decomprime il file zip in una cartella temporanea. Viene generata una lista dei file Gerber e di foratura identificati. |
| **BE-04** | **Parsing dei Layer con Gerbonara** | P1 | BE-03 | • Gerbonara: `GerberFile.open()`• Iterazione su GraphicObject (`Line`, `Arc`, `Region`) | Per ogni file Gerber, il sistema è in grado di parsarlo con Gerbonara e accedere alle primitive geometriche senza errori. |
| **BE-05** | **"Appiattimento" della Geometria (Tessellation)** | P1 | BE-04 | • Logica custom per convertire Arc in segmenti e Region in triangoli | Una funzione prende in input una lista di GraphicObject e restituisce una lista flat di vertici (coordinate x, y) come float32. |
| **BE-06** | **API per Lista Layer e Dati Geometrici** | P1 | BE-05 | • FastAPI• Formato di trasferimento binario (es. bytes di un array NumPy) | • `GET /api/v1/session/{session_id}/layers` restituisce una lista JSON dei layer disponibili (es. `[{ "name": "top_copper.gbr", "color": "#FF0000" }]`).• `GET /api/v1/session/{session_id}/layer/{layer_name}` restituisce i dati dei vertici appiattiti in formato binario. |

## Fase 2: Sviluppo del Frontend (UI e Rendering di Base)

**Obiettivo:** Creare l'interfaccia utente Flutter per l'upload, la visualizzazione della lista dei layer e il rendering iniziale utilizzando un approccio stabile e affidabile.

| ID | Task | Priorità | Dipendenze | Risorse e Tecnologie | Criteri di Accettazione |
|----|------|----------|------------|---------------------|-------------------------|
| **FE-01** | **Setup Progetto Flutter** | P1 | - | • Flutter 3.x• Pattern BLoC (flutter_bloc)• dio per le chiamate HTTP | Un nuovo progetto Flutter desktop viene creato. La struttura delle cartelle e i BLoC iniziali (GerberProjectBloc) sono definiti. |
| **FE-02** | **UI per Upload File** | P1 | FE-01 | • file_picker package | L'utente può cliccare un pulsante, selezionare un file `.zip` dal proprio computer e un evento BLoC viene triggerato con il file selezionato. |
| **FE-03** | **Integrazione API di Upload** | P1 | BE-02, FE-02 | • dio per richieste multipart/form-data | Il file `.zip` selezionato viene inviato all'endpoint backend. L'app riceve e memorizza il session_id restituito. |
| **FE-04** | **UI Pannello Layer** | P1 | FE-03, BE-06 | • ListView.builder• CheckboxListTile | Dopo l'upload, l'app chiama l'API `/layers`, riceve la lista dei layer e la visualizza in un pannello laterale con checkbox per ogni layer. |
| **FE-05** | **Rendering di Base con Skia** | P1 | FE-04, BE-06 | • CustomPainter & Canvas• InteractiveViewer per Pan/Zoom | Viene creato un widget GerberCanvas che, quando un layer è selezionato, scarica i dati binari, li converte in Float32List e li disegna usando `canvas.drawRawPoints` o `canvas.drawVertices`. Il pan e lo zoom sono funzionanti. |
| **FE-06** | **Gestione Stato Visibilità Layer** | P1 | FE-05 | • GerberProjectBloc | Selezionando/deselezionando una checkbox nel pannello layer, il GerberCanvas si aggiorna dinamicamente, mostrando o nascondendo il layer corrispondente. L'app gestisce il rendering di più layer sovrapposti. |

## Fase 3: Ottimizzazione e Finalizzazione MVP

**Obiettivo:** Migliorare le performance di rendering per garantire un'esperienza fluida anche con file di medie dimensioni e aggiungere le ottimizzazioni necessarie per la validazione del concetto.

| ID | Task | Priorità | Dipendenze | Risorse e Tecnologie | Criteri di Accettazione |
|----|------|----------|------------|---------------------|-------------------------|
| **FE-07** | **Implementazione Struttura Dati Quadtree** | P2 | - | • Logica custom in Dart• Articoli su Quadtree per partizionamento spaziale | Una classe Quadtree in Dart è implementata e testata. Può contenere rettangoli (le bounding box dei segmenti) e può essere interrogata per trovare tutti gli oggetti che intersecano un'area specifica. |
| **FE-08** | **Integrazione Quadtree nel Flusso di Rendering** | P2 | FE-06, FE-07 | • InteractiveViewer onInteractionUpdate per ottenere la viewport visibile | Al caricamento di un layer, tutte le sue primitive vengono inserite nel Quadtree. Ad ogni frame (durante pan/zoom), il renderer interroga il Quadtree per ottenere solo le geometrie visibili (View Frustum Culling) e passa solo queste al CustomPainter. |
| **FE-09** | **(Opzionale) Ricerca su Rendering Accelerato** | P3 | FE-06 | • Flutter-GPU• Shader GLSL• Canale `main` di Flutter | Si crea un branch separato per sperimentare l'implementazione di un renderer basato su Flutter-GPU. L'obiettivo è validare la fattibilità e confrontare le performance con l'approccio Skia. **Nota:** Dato lo stato di preview, questo task è ad alto rischio e non è strettamente necessario per il primo MVP. |
| **QA-01** | **Test End-to-End** | P1 | Tutti | • Set di file Gerber di test (semplici e complessi) | Il flusso completo (upload → elaborazione → visualizzazione) funziona correttamente con diversi set di dati. L'applicazione è stabile su almeno una piattaforma desktop target (es. Windows). |

## Legenda Priorità

- **P1**: Priorità Alta (Essenziale per l'MVP)
- **P2**: Priorità Media (Importante per le performance)
- **P3**: Priorità Bassa (Opzionale/Ricerca)

## Note Tecniche

- **Backend**: Utilizzo di Python con FastAPI per garantire performance e facilità di sviluppo
- **Frontend**: Flutter desktop per un'interfaccia nativa cross-platform
- **Rendering**: Approccio ibrido con Skia come base stabile e Flutter-GPU come opzione sperimentale
- **Ottimizzazioni**: Implementazione di Quadtree per il view frustum culling e miglioramento delle performance
