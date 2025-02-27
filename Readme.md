## Visuales Scrapper
Visuales url: visuales.uclv.cu

Programa/Herramienta para facilitar la descarga de contenido audiovisual de la plataforma Visuales [visuales.uclv.cu](url).

!!!!!!Quieres descargar una serie, película o cualquier contenido audiovisual de Visuales pero no quieres tener que descargarlo uno a uno !!!!
Con esta herramienta basta con poner la url de la serie o contenido que quieres descargar y automáticamente te devolverá los links organizados por carpetas.
Puedes exportar los links extraidos hacia Internet Downloader Manager(IDM), lo cual realiza la descarga por ti o en forma de archivos .txt para futura descarga. 

With this program we can:
- Get links to download the content that we want to get in visuales and export them to IDM or just get a text file with the links.
- Map an entire section of Visuales Ex. Movies, and save it into a json file for future media searching and downloading.
- Search in the built databases for the content that you wanna see and download.  

## Create a virtual environment
```bash
python -m venv env
```
## Activate the virtual environment
```bash
source env/Scripts/activate
```
## Install dependencies
```bash
pip install -r requirements.txt
```
## Run the program
```bash
python main.py
```