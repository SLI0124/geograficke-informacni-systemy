# Geografické informační systémy

Geografické informační systémy (GIS) představují oblast, která je dnes využívána v mnoha různých aplikacích. Kurz je zaměřen na seznámení se se způsoby získání, zpracování a analýzy dat v GIS. Představeny budou techniky zpracování nejobvyklejších druhů prostorových dat, analytické nástroje a techniky pro jejich analýzu a v neposlední řadě způsoby vizualizace typické pro GIS. Bude představena cesta, jak zpracovat data z podoby tzv. surových dat, přes jejich analýzu, ukládání, až po výslednou vizualizaci koncovému uživateli. Kurz se též bude zabývat technikami vizualizace dat v prostředí Internetu.

Stránka kurzu: <https://mrl.cs.vsb.cz//people/gaura/gis_course.html>

## ⚙️ Požadavky

### C++

- **CMake** (3.10+)
- **GCC** nebo **Clang**
- **OpenCV**
- **PROJ**
- **PkgConfig**

### Python

- **Python 3**
- **Matplotlib**

## 🛠️ C++ Projekt

### Build

```bash
cd cpp
cmake -S . -B build
cmake --build build --parallel
```

### Spuštění (C++)

```bash
./build/gis ../data/dummy.txt ../data/pt000023.bin ../data/pt000023.png
```

## 🐍 Python Projekt

### Nastavení prostředí

Pro instalaci závislostí můžete použít virtuální prostředí:

```bash
cd python
python3 -m venv .venv --prompt geo_vsb  
source .venv/bin/activate
pip install -r requirements.txt
```

### Spuštění (Python 3)

```bash
python tutorial_7.py
python tutorial_8.py
```
