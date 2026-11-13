# Implementazione Backend - Step by Step

## Overview del Piano

Implementazione di un sistema di gestione sessioni per file Gerber con rendering SVG on-demand:

1. **Upload ZIP** → Estrazione in cartella temporanea con session_id
2. **Gestione Sessioni** → Cache 2 ore, cleanup automatico
3. **Rendering Layer** → Parse Gerbonara + generazione SVG per layer specifico
4. **Rendering Board** → Tutti i layer sovrapposti in un unico SVG

## Fase 1: Setup Dipendenze e Struttura

### 1.1 Aggiornare requirements.txt

``` plaintext
fastapi==0.104.1
uvicorn[standard]==0.24.0
gerbonara==1.4.0
python-multipart
aiofiles
apscheduler
pydantic
```

### 1.2 Struttura Directory

``` plaintext
backend/
├── main.py
├── models/
│   ├── __init__.py
│   └── session.py          # Pydantic models
├── services/
│   ├── __init__.py
│   ├── session_manager.py  # Gestione sessioni
│   └── gerber_service.py   # Logic Gerbonara
├── api/
│   ├── __init__.py
│   └── endpoints.py        # API endpoints
└── utils/
    ├── __init__.py
    └── cleanup.py          # Background tasks
```

## Fase 2: Modelli Dati

### 2.1 models/session.py

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum

class FileType(str, Enum):
    GERBER = "gerber"
    DRILL = "drill"
    UNKNOWN = "unknown"

class GerberFile(BaseModel):
    name: str
    type: FileType
    layer: str
    size_bytes: int

class SessionMetadata(BaseModel):
    session_id: str
    created_at: datetime
    expires_at: datetime
    files: List[GerberFile]
    original_filename: str

class SessionResponse(BaseModel):
    session_id: str
    expires_in: str
    files_count: int
    message: str

class LayerListResponse(BaseModel):
    session_id: str
    layers: List[str]
    expires_at: datetime

class SVGResponse(BaseModel):
    session_id: str
    layer_name: Optional[str] = None
    svg_content: str
    generated_at: datetime
```

## Fase 3: Session Manager

### 3.1 services/session_manager.py

```python
import uuid
import json
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import UploadFile, HTTPException

from models.session import SessionMetadata, GerberFile, FileType

class SessionManager:
    def __init__(self, base_path: str = "/tmp/gerber_sessions"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.session_duration = timedelta(hours=2)
    
    async def create_session(self, zip_file: UploadFile) -> str:
        """
        Crea una nuova sessione:
        1. Genera session_id
        2. Crea directory temporanea
        3. Estrae ZIP
        4. Analizza file contenuti
        5. Salva metadata
        """
        # TODO: Implementare
        pass
    
    def get_session_path(self, session_id: str) -> Path:
        """Restituisce il path della directory di sessione"""
        return self.base_path / session_id
    
    def get_session_metadata(self, session_id: str) -> Optional[SessionMetadata]:
        """Carica metadata di sessione da file JSON"""
        # TODO: Implementare
        pass
    
    def is_session_expired(self, session_id: str) -> bool:
        """Controlla se una sessione è scaduta"""
        # TODO: Implementare
        pass
    
    def cleanup_expired_sessions(self):
        """Pulisce le sessioni scadute (background task)"""
        # TODO: Implementare
        pass
    
    def _identify_file_type(self, filename: str) -> FileType:
        """Identifica il tipo di file Gerber"""
        # TODO: Implementare logica riconoscimento
        # .gbr, .gbl, .gtl = GERBER
        # .drl, .txt = DRILL
        pass
    
    def _extract_layer_name(self, filename: str) -> str:
        """Estrae nome layer dal filename"""
        # TODO: Implementare
        pass
```

### 3.2 Punti di Implementazione Session Manager

**create_session() - Steps:**

1. Genera UUID per session_id
2. Valida che il file sia ZIP
3. Crea directory `/tmp/gerber_sessions/{session_id}/`
4. Estrae ZIP nella directory
5. Analizza file estratti (tipo, layer, dimensione)
6. Crea SessionMetadata
7. Salva metadata.json
8. Restituisce session_id

**File Type Recognition:**

```python
# Esempi pattern comuni Gerber
GERBER_EXTENSIONS = {
    '.gbr': 'gerber',
    '.gtl': 'top_copper',
    '.gbl': 'bottom_copper',
    '.gts': 'top_soldermask',
    '.gbs': 'bottom_soldermask'
}
```

## Fase 4: Gerber Service

### 4.1 services/gerber_service.py

```python
from gerbonara import GerberFile
from pathlib import Path
from typing import Optional
import tempfile

class GerberService:
    @staticmethod
    def parse_gerber_to_svg(file_path: Path) -> str:
        """
        Parse un file Gerber e genera SVG
        1. Apre file con Gerbonara
        2. Genera SVG
        3. Restituisce stringa SVG
        """
        # TODO: Implementare
        pass
    
    @staticmethod
    def combine_layers_to_svg(layer_paths: List[Path]) -> str:
        """
        Combina multiple layer in un unico SVG
        """
        # TODO: Implementare
        pass
    
    @staticmethod
    def get_layer_bounds(file_path: Path) -> dict:
        """
        Calcola bounding box del layer
        """
        # TODO: Implementare
        pass
```

## Fase 5: API Endpoints

### 5.1 api/endpoints.py

```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.session_manager import SessionManager
from services.gerber_service import GerberService
from models.session import SessionResponse, LayerListResponse, SVGResponse

router = APIRouter(prefix="/api/v1")
session_manager = SessionManager()
gerber_service = GerberService()

@router.post("/process-zip", response_model=SessionResponse)
async def process_zip(file: UploadFile = File(...)):
    """
    Upload e processamento ZIP Gerber
    """
    # TODO: Implementare
    pass

@router.get("/session/{session_id}/layers", response_model=LayerListResponse)
async def get_layers(session_id: str):
    """
    Lista layer disponibili per sessione
    """
    # TODO: Implementare
    pass

@router.get("/session/{session_id}/layer/{layer_name}/svg", response_model=SVGResponse)
async def render_layer_svg(session_id: str, layer_name: str):
    """
    Rendering SVG di un layer specifico
    """
    # TODO: Implementare
    pass

@router.get("/session/{session_id}/board/svg", response_model=SVGResponse)
async def render_board_svg(session_id: str):
    """
    Rendering SVG di tutti i layer combinati
    """
    # TODO: Implementare
    pass
```

## Fase 6: Background Tasks

### 6.1 utils/cleanup.py

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.session_manager import SessionManager

def setup_cleanup_scheduler(session_manager: SessionManager):
    """
    Setup del task di cleanup automatico
    """
    scheduler = AsyncIOScheduler()
    
    # Cleanup ogni 30 minuti
    scheduler.add_job(
        session_manager.cleanup_expired_sessions,
        'interval',
        minutes=30,
        id='cleanup_sessions'
    )
    
    scheduler.start()
    return scheduler
```

## Fase 7: Integrazione in main.py

### 7.1 Aggiornare main.py

```python
from fastapi import FastAPI
from datetime import datetime
import os

from api.endpoints import router
from utils.cleanup import setup_cleanup_scheduler
from services.session_manager import SessionManager

app = FastAPI(
    title="Gerber MVP Backend",
    version="1.0.0"
)

# Setup session manager e cleanup
session_manager = SessionManager()
cleanup_scheduler = setup_cleanup_scheduler(session_manager)

# Include API routes
app.include_router(router)

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "gerber-backend",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "active_sessions": len(list(session_manager.base_path.iterdir()))
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/")
def root():
    return {"message": "Gerber MVP Backend is running!"}

@app.on_event("shutdown")
def shutdown_event():
    cleanup_scheduler.shutdown()
```

## Ordine di Implementazione Consigliato

### Step 1: Struttura Base

- [ ] Creare directory structure
- [ ] Aggiornare requirements.txt
- [ ] Creare modelli Pydantic

### Step 2: Session Manager Base

- [ ] Implementare create_session() senza Gerbonara
- [ ] Test con ZIP semplici
- [ ] Implementare get_session_metadata()

### Step 3: File Analysis

- [ ] Implementare _identify_file_type()
- [ ] Implementare _extract_layer_name()
- [ ] Test con file Gerber reali

### Step 4: Gerber Service

- [ ] Implementare parse_gerber_to_svg()
- [ ] Test rendering singolo layer
- [ ] Implementare combine_layers_to_svg()

### Step 5: API Endpoints

- [ ] Implementare process_zip endpoint
- [ ] Implementare get_layers endpoint
- [ ] Implementare render_layer_svg endpoint
- [ ] Implementare render_board_svg endpoint

### Step 6: Cleanup & Testing

- [ ] Implementare background cleanup
- [ ] Test completo del flusso
- [ ] Error handling e validazioni

## Testing Strategy

### Test Manuali

```bash
# 1. Test upload
curl -X POST "http://localhost:8000/api/v1/process-zip" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_gerber.zip"

# 2. Test layer list
curl "http://localhost:8000/api/v1/session/{session_id}/layers"

# 3. Test SVG rendering
curl "http://localhost:8000/api/v1/session/{session_id}/layer/top_copper/svg"
```

### File di Test

- Procurati alcuni file ZIP con Gerber semplici
- KiCad può esportare file Gerber di esempio
- EasyEDA ha progetti open source

## Note Implementative

### Error Handling Comuni

- Session not found (404)
- Session expired (410 Gone)
- Invalid ZIP format (400)
- Gerber parsing errors (422)
- File too large (413)

### Performance Considerations

- Limite dimensione ZIP (es. 50MB)
- Timeout parsing Gerbonara
- Cache SVG già generati (opzionale)
- Async I/O per file operations

### Security

- Validazione UUID session_id
- Sanitizzazione nomi file
- Limite spazio disco per sessioni
- Rate limiting upload

## Prossimi Passi dopo Backend

Una volta completato il backend, il prossimo step sarà:

1. **Frontend Flutter**: Upload interface
2. **Layer Panel**: UI per selezione layer
3. **SVG Viewer**: Rendering SVG con pan/zoom
4. **Integration Testing**: End-to-end flow

---

*Questo documento verrà aggiornato durante l'implementazione con dettagli specifici e lessons learned.*
