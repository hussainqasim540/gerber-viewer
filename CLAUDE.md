# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Gerber file visualization MVP consisting of two main components:

- **Backend**: Python FastAPI service for Gerber file parsing using Gerbonara library
- **Frontend**: Flutter desktop application for visualization with Skia rendering

The project follows a 3-phase development approach as outlined in `gerber_mvp_plan.md`.

## Architecture

### Backend (Python + FastAPI)

- **File Processing**: Accepts ZIP uploads containing Gerber files
- **Parsing Engine**: Uses Gerbonara library to parse Gerber files into geometric primitives
- **Geometry Processing**: "Flattens" complex geometry (arcs, regions) into simple vertices for efficient rendering
- **API Endpoints**:
  - `POST /api/v1/process-zip` - Upload and process Gerber files
  - `GET /api/v1/session/{session_id}/layers` - Get layer list
  - `GET /api/v1/session/{session_id}/layer/{layer_name}` - Get layer geometry data

### Frontend (Flutter Desktop)

- **State Management**: BLoC pattern (flutter_bloc)
- **File Upload**: file_picker package for ZIP selection
- **HTTP Client**: dio for API communication
- **Rendering**: Custom Skia-based renderer using CustomPainter
- **Optimization**: Quadtree spatial partitioning for view frustum culling
- **UI**: Layer panel with visibility controls, interactive viewport with pan/zoom

## Key Technologies

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Gerbonara, Docker
- **Frontend**: Flutter 3.x, flutter_bloc, dio, CustomPainter/Canvas
- **Deployment**: Docker & Docker Compose

## Development Commands

Note: This repository currently contains only the project plan. Actual implementation will follow the roadmap in `gerber_mvp_plan.md`.

When backend is implemented:

```bash
# Backend development
docker-compose up --build
# Health check: GET /health

# Python development
pip install -r requirements.txt
uvicorn main:app --reload
```

When frontend is implemented:

```bash
# Flutter development
flutter pub get
flutter run -d windows  # or macos/linux
flutter build windows   # for release builds
```

## Project Structure (Planned)

``` plaintext
gerber_mvp/
├── backend/           # FastAPI service
│   ├── main.py       # FastAPI app
│   ├── gerber_parser.py  # Gerbonara integration
│   └── api/          # API endpoints
├── frontend/         # Flutter desktop app
│   ├── lib/
│   │   ├── blocs/    # BLoC state management
│   │   ├── models/   # Data models
│   │   ├── services/ # API services
│   │   └── widgets/  # UI components
└── docker-compose.yml
```

## Development Notes

- Focus on stability over cutting-edge features (Skia over Flutter-GPU initially)
- Optimize for desktop PCB file sizes (medium complexity Gerber files)
- Binary data transfer for geometry to minimize network overhead
- Session-based file processing to handle multiple concurrent users
