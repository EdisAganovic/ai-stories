# Generator priča za djecu - Primjeri korištenja

## Instalacija
1. Instalirajte potrebne zavisnosti:
   ```bash
   pip install -r requirements.txt
   ```

2. Postavite vaš OpenRouter API ključ kao varijablu okruženja:
   ```bash
   # Na Windowsu
   set OPENROUTER_API_KEY=vaš_api_ključ_ide_ovdje

   # Na macOS/Linuxu
   export OPENROUTER_API_KEY=vaš_api_ključ_ide_ovdje
   ```

## Korištenje

### Interaktivni režim
Pokrenite skriptu bez argumenata da biste koristili interaktivne upute:
```bash
python story_generator.py
```

### Režim argumenata komandne linije
Pružite sve potrebne parametre direktno kao argumente:
```bash
python story_generator.py -i "putanja/do/crteza.jpg" -n "Amar" -s "pustolovina" -l "duga"
```

### Dostupni argumenti
- `-i, --image`: Putanja do dječijeg crteža (JPG, PNG, BMP, ili WebP)
- `-n, --name`: Dječije ime za personalizaciju priče
- `-s, --style`: Stil priče (fairy tale, sci-fi, adventure, mystery, comedy, everyday life)
- `-l, --length`: Dužina priče (short: ~5 paragrafa, long: ~10 paragrafa)

### Primjer komandi
Generišite kratku basnu za dijete po imenu Amar:
```bash
python story_generator.py -i "amar_crtez.png" -n "Amar" -s "fairy tale" -l "short"
```

Generišite dugu pustolovinsku priču za dijete po imenu Lejla:
```bash
python story_generator.py -i "lejla_skica.jpg" -n "Lejla" -s "adventure" -l "long"
```

## Podržani formati slika
- JPG/JPEG
- PNG
- BMP
- WebP

## Rukovanje greškama
Aplikacija rukuje različite uslove greške:
- Neispravne ili nedostajuće putanje do datoteke slike
- Nepodržani formati slike
- Nedostaje API ključ
- Mrežne/API greške
- Prazni ili neispravni korisnički unosi