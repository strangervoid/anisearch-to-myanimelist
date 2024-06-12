import json
import xml.etree.ElementTree as ET
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# JSON-Datei und API-Schlüssel definieren
json_filename = 'your json file with .json at the end'  # deine .json File aus dem anisearch Export
xml_filename = 'converted_mal_list.xml'
client_id = 'your MAL API Dev client_id'  # deine MyAnimeList Developer Client ID
current_date = "0000-00-00"
failed_log_filename = 'failed_anime_id_list.txt'

def get_anime_id(title):
    url = f'https://api.myanimelist.net/v2/anime?q={title}&limit=1'
    headers = {'X-MAL-CLIENT-ID': client_id}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['node']['id']
    return 0

def fetch_anime_id(anime):
    title = anime['title']
    anime_id = get_anime_id(title)
    return title, anime_id

# JSON-Datei einlesen
with open(json_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# XML-Struktur erstellen
root = ET.Element("myanimelist")

# <myinfo> tag erstellen und random stuff reinkloppen damit MAL nicht rumheult
myinfo_element = ET.SubElement(root, "myinfo")
user_name_element = ET.SubElement(myinfo_element, "user_name")
user_name_element.text = "username"
user_export_type_element = ET.SubElement(myinfo_element, "user_export_type")
user_export_type_element.text = "1"
user_total_anime_element = ET.SubElement(myinfo_element, "user_total_anime")
user_total_anime_element.text = str(len(data['anime']['Completed']))
user_total_watching_element = ET.SubElement(myinfo_element, "user_total_watching")
user_total_watching_element.text = "0"
user_total_completed_element = ET.SubElement(myinfo_element, "user_total_completed")
user_total_completed_element.text = str(len(data['anime']['Completed']))
user_total_onhold_element = ET.SubElement(myinfo_element, "user_total_onhold")
user_total_onhold_element.text = "0"
user_total_dropped_element = ET.SubElement(myinfo_element, "user_total_dropped")
user_total_dropped_element.text = "0"
user_total_plantowatch_element = ET.SubElement(myinfo_element, "user_total_plantowatch")
user_total_plantowatch_element.text = "0"

# Mapping der Statuswerte von AniSearch auf MAL
status_mapping = {
    "Completed": "Completed",
    "Ongoing": "Watching",
    "On Hold": "On-Hold",
    "Aborted": "Dropped",
    "Not Interested": "Dropped",  # gibt's auf MAL nicht, einfach auf Dropped und gut is'
    "Bookmarked": "Plan to Watch"
}

# Vorbereitung der Anime-Daten
animes = []
for status in data['anime']:
    for anime in data['anime'][status]:
        anime['status'] = status_mapping.get(status, "Plan to Watch")
        animes.append(anime)

# Startzeitpunkt für die Laufzeitmessung
start_time = time.time()

# Parallelisierung der API-Anfragen
failed_anime = []
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_anime = {executor.submit(fetch_anime_id, anime): anime for anime in animes}
    for future in as_completed(future_to_anime):
        anime = future_to_anime[future]
        title, anime_id = future.result()

        # Wenn keine gültige ID gefunden wurde, protokollieren
        if anime_id == 0:
            failed_anime.append(title)
        
        # Anime-Element erstellen und Daten hinzufügen
        anime_element = ET.SubElement(root, "anime")
        
        series_title = ET.SubElement(anime_element, "series_title")
        series_title.text = title
        
        series_episodes = ET.SubElement(anime_element, "series_episodes")
        series_episodes.text = str(anime['episodes'])
        
        my_watched_episodes = ET.SubElement(anime_element, "my_watched_episodes")
        my_watched_episodes.text = str(anime['episodes'])
        
        my_score = ET.SubElement(anime_element, "my_score")
        my_score.text = str(anime['rating'])
        if my_score.text == "100":
            my_score.text = my_score.text[0] + my_score.text[1]
        else:
            my_score.text = my_score.text[0]  # anisearch gibt Rating mit 'ner extra 0 hinter raus, weg damit
        
        my_status = ET.SubElement(anime_element, "my_status")
        my_status.text = anime['status']
        
        series_animedb_id = ET.SubElement(anime_element, "series_animedb_id")
        series_animedb_id.text = str(anime_id)
        
        # Hinzufügen von Standardwerten für obligatorische Felder
        series_type = ET.SubElement(anime_element, "series_type")
        series_type.text = "0"
        
        my_id = ET.SubElement(anime_element, "my_id")
        my_id.text = "0"
        
        my_start_date = ET.SubElement(anime_element, "my_start_date")
        my_start_date.text = current_date
        
        my_finish_date = ET.SubElement(anime_element, "my_finish_date")
        my_finish_date.text = current_date
        
        my_rewatching = ET.SubElement(anime_element, "my_rewatching")
        my_rewatching.text = "0"
        
        my_rewatching_ep = ET.SubElement(anime_element, "my_rewatching_ep")
        my_rewatching_ep.text = "0"
        
        update_on_import = ET.SubElement(anime_element, "update_on_import")
        update_on_import.text = "1"

# Endzeitpunkt für die Laufzeitmessung
end_time = time.time()
elapsed_time = end_time - start_time

# XML-Datei speichern
tree = ET.ElementTree(root)
tree.write(xml_filename, encoding='utf-8', xml_declaration=True)

# Protokolliere die fehlgeschlagenen Anfragen in einer Textdatei
if failed_anime:
    with open(failed_log_filename, 'w', encoding='utf-8') as f:
        f.write("Für folgende Titel konnte keine Anime-ID gefunden werden (eventuell noch mal manuell rübergucken):\n")
        for title in failed_anime:
            f.write(f"{title}\n")
    print(f"Für einige Titel konnte keine Anime-ID gefunden werden. Details siehe '{failed_log_filename}'.")

print(f"Deine anisearch JSON wurde in XML umgewandelt und als '{xml_filename}' gespeichert. Enjoy.")
print(f"Laufzeit des Programms: {elapsed_time:.2f} Sekunden")
