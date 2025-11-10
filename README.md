# Generator priča za djecu

Ovaj alat pretvara dječije crteže u fantastične priče koristeći OpenRouter API (sa Google Gemini modelom). Kreira personalizovane priče koje uključuju vizuelne elemente iz slike sa imenom djeteta i željenim stilom priče.

## Značajke

- Prihvata JPG, PNG, BMP, ili WebP datoteke slika
- Personalizuje priče sa imenom djeteta
- Nudi 6 stilova priče: Basna, Naučna fantastika, Pustolovina, Misterija, Komedija, i Svakodnevni život
- Dozvoljava izbor kratkih (~5 paragrafa) ili dugih (~10 paragrafa) priča
- Kreira priče prikladne za djecu i zanimljive na osnovu crteža
- Podržava interaktivni režim i CLI argumente

## Preduvjeti

- Python 3.7 ili noviji
- OpenRouter API ključ

## Instalacija

1. Klonirajte ili preuzmite ovaj repozitorij
2. Instalirajte potrebne zavisnosti:
   ```bash
   pip install -r requirements.txt
   ```
3. Postavite vaš OpenRouter API ključ u `.env` datoteku:
   ```
   OPENROUTER_API_KEY=vaš_pravi_api_ključ_ide_ovdje
   ```

## Korištenje

### Interaktivni režim
Jednostavno pokrenite skriptu i slijedite upute:
```bash
python story_generator.py
```

### Režim CLI argumenata
Možete pružiti sve parametre kao CLI argumente:
```bash
python story_generator.py -i "putanja/do/crteza.jpg" -n "Emma" -s "pustolovina" -l "duga"
```

#### Dostupni argumenti
- `-i, --image`: Putanja do dječijeg crteža (JPG, PNG, BMP, ili WebP)
- `-n, --name`: Dječije ime
- `-s, --style`: Stil priče (basna, naučna fantastika, pustolovina, misterija, komedija, svakodnevni život)
- `-l, --length`: Dužina priče (kratka, duga)

## Primjer

```bash
python story_generator.py -i "moj_crtez.png" -n "Amar" -s "basna" -l "kratka"
```

Ovo će generisati kratku basnu za Amara na osnovu datog crteža.

## Rukovanje greškama

Aplikacija rukuje različite uslove greške:
- Neispravne putanje do datoteke slike
- Nepodržani formati slike
- Nedostaje API ključ
- Mrežne/API greške