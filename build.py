import PyInstaller.__main__
import os
import shutil

def build():
    print("Započinjem proces build-a pomoću PyInstaller-a...")
    
    # Ime aplikacije
    app_name = "AI Stories"
    
    # Putanja do glavne skripte
    main_script = "main.py"
    
    # Konfiguracija za PyInstaller
    args = [
        main_script,
        '--name', app_name,
        # '--onefile',  # Isključeno jer ne želimo da se širi u temp folder
        '--onedir',   # Koristimo direktorij tako da su resursi vidljivi pored exe-a
        '--console',  # Ostavljamo konzolu vidljivom
        '--add-data', f'templates{os.pathsep}templates',
        '--add-data', f'static{os.pathsep}static',
        '--hidden-import', 'uvicorn.protocols.http.httptools_impl',
        '--hidden-import', 'uvicorn.protocols.http.h11_impl',
        '--hidden-import', 'uvicorn.protocols.websockets.websockets_impl',
        '--hidden-import', 'uvicorn.lifespan.on',
        '--clean',
        '--noconfirm'
    ]
    
    # Pokretanje PyInstaller-a
    PyInstaller.__main__.run(args)
    
    # Osiguraj da 'static' direktorij postoji u _internal (potrebno za resurse u nekim verzijama)
    internal_static = os.path.join('dist', app_name, '_internal', 'static')
    if os.path.exists(os.path.join('dist', app_name, '_internal')):
        os.makedirs(internal_static, exist_ok=True)
        print(f"Osiguran 'static' direktorij u: {internal_static}")
    
    print(f"\nBuild je završen! Izvršna datoteka se nalazi u 'dist/{app_name}/{app_name}.exe'.")

if __name__ == "__main__":
    build()
