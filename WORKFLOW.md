# Objašnjenje Rada Aplikacije Generator Priča za Djecu

## Šta su Vision-Language (VL) modeli?

Vision-Language (VL) modeli su vrsta vještačke inteligencije koja može istovremeno razumjeti i slike i tekst. Zamislite da imate prijatelja koji može pogledati sliku i odmah ispričati priču o svemu što vidi na njoj. To je upravo ono što VL modeli rade – analiziraju slike i zatim generišu tekstualne odgovore, poput priča, opisa ili odgovora na pitanja.

## Kako smo napravili ovu aplikaciju?

### 1. Ideja i cilj
Naš cilj bio je napraviti aplikaciju koja pretvara dječije crteže u zanimljive priče. Umjesto da odrasli pišu priče, mašina može pomoći da se iz slike napravi priča koja uključuje elemente iz dječjeg crteža, uz dodavanje imena djeteta i izabranog stila priče.

### 2. Tehnologija: Google Gemini preko OpenRouter-a
Za ovaj projekat koristili smo **Google Gemini** model, koji je vrlo napredan VL model. Google Gemini može analizirati slike i generisati tekstualne odgovore na osnovu sadržaja slike. Umjesto da direktno pristupamo modelu, koristili smo **OpenRouter API**, koji je platforma koja omogućava jednostavan pristup različitim AI modelima.

### 3. Kako OpenRouter pomaže?
OpenRouter djeluje kao most između naše aplikacije i Google Gemini modela. Umjesto da gradimo kompleksnu infrastrukturu za komunikaciju s Google-ovim serverima, koristimo OpenRouter koji olakšava ovu komunikaciju. Potrebno je samo imati API ključ (kao "šifru za pristup") i možemo šaljiti slike i tekstualne zahtjeve.

### 4. Proces izrade priče
Evo kako tačno aplikacija funkcioniše:

#### Korak 1: Učitavanje slike
Korisnik šalje dječiji crtež (u formatima JPG, PNG, BMP ili WebP). Aplikacija provjerava da li je slika ispravna i da li je u podržanom formatu.

#### Korak 2: Generisanje upita (prompt)
Aplikacija kombinuje informacije koje korisnik pruži (ime djeteta, stil priče, dužina priče) sa specijalno dizajniranim tekstualnim upitom koji opisuje šta želimo da AI uradi.

#### Korak 3: Slanje zahtjeva AI modelu
Slika i tekstualni upit šalju se Google Gemini modelu preko OpenRouter API-ja. Model analizira sadržaj slike i generiše priču koja uključuje elemente iz slike, uz prilagođavanje za dijete i u skladu sa željenim stilom.

#### Korak 4: Prikaz rezultata
Kada AI model napravi priču, aplikacija je vraća korisniku u lako čitljivom obliku.

## Zašto je ovo korisno?
- **Kreativnost**: Djeci možemo omogućiti da vide kako ih mašine mogu podržati u kreativnom izražavanju
- **Personalizacija**: Svaka priča je prilagođena imenom djeteta i njegovim interesovanjima
- **Interaktivnost**: Djeca mogu eksperimentisati s različitim stilovima i dužinama priča
- **Učenje**: Demonstrira kako mogu funkcionišati AI sistemi za generisanje sadržaja

## Tehničke pojedinosti
- **Model**: Google Gemini (pomoću OpenRouter API-ja)
- **Formati slika**: JPG, PNG, BMP, WebP
- **Stilovi priča**: Basna, Naučna fantastika, Pustolovina, Misterija, Komedija, Svakodnevni život
- **Dužina priče**: Kratka (~5 paragrafa) ili Duga (~10 paragrafa)

## Zaključak
Ova aplikacija predstavlja kombinaciju jednostavne korisničke interakcije i napredne AI tehnologije. Kroz upotrebu VL modela, možemo pretvoriti vizuelne ideje iz dječjih crteža u pripovijetke koje djeca mogu uživati, a s kojima se mogu identifikovati. Ovo je primjer kako se danas koristi AI za stvaranje personalizovanog i kreativnog sadržaja za djecu.