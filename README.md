# Geografické informační systémy

Geografické informační systémy (GIS) představují oblast, která je dnes využívána v mnoha různých aplikacích. Kurz je zaměřen na seznámení se se způsoby získání, zpracování a analýzy dat v GIS. Představeny budou techniky zpracování nejobvyklejších druhů prostorových dat, analytické nástroje a techniky pro jejich analýzu a v neposlední řadě způsoby vizualizace typické pro GIS. Bude představena cesta, jak zpracovat data z podoby tzv. surových dat, přes jejich analýzu, ukládání, až po výslednou vizualizaci koncovému uživateli. Kurz se též bude zabývat technikami vizualizace dat v prostředí Internetu.

Stránka kurzu: <https://mrl.cs.vsb.cz//people/gaura/gis_course.html>

## ⚙️ Požadavky (Arch Linux)

Nainstaluj balíčky:

```bash
sudo pacman -S --needed cmake gcc opencv proj pkgconf hdf5 vtk gdb
```

## 🛠️ Build

```bash
cmake -S . -B build
cmake --build build --parallel
```

## ▶️ Spuštění

```bash
./build/gis dummy.txt ./assets/pt000023.bin ./assets/pt000023.png
```
