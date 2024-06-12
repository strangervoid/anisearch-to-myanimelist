import json
import xml.etree.ElementTree as ET
import requests

# JSON-Datei und API-Schlüssel definieren
json_filename = 'YOUR JSON FILE' # deine .json File aus dem anisearch Export
xml_filename = 'converted_mal_list.xml'
client_id = 'YOUR CLIENTID'  # deine MyAnimeList Developer Client ID
current_date = "0000-00-00"

def get_anime_id(title):
    url = f'https://api.myanimelist.net/v2/anime?q={title}&limit=1'
    headers = {'X-MAL-CLIENT-ID': client_id}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]['node']['id']
    return 0

# JSON-Datei einlesen
with open(json_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# XML-Struktur erstellen
root = ET.Element("myanimelist")

# <myinfo> tag erstellen und random stuff reinkloppen damit MAL nicht rumheult (die Fehlermeldungen von denen haben echt nicht weitergeholfen lol)
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

# Es gibt beim JSON folgende Stati:
# -Completed
# -Ongoing
# -On Hold
# -Bookmarked
# -Aborted
# -Not Interested

# bei MAL gibt es die hier:
# -Watching
# -Completed
# -On-Hold
# -Dropped
# -Plan to Watch

# Mapping der Statuswerte von AniSearch auf MAL
status_mapping = {
    "Completed": "Completed",
    "Ongoing": "Watching",
    "On Hold": "On-Hold",
    "Aborted": "Dropped", 
    "Not Interested": "Dropped", # gibt's auf MAL nicht, einfach auf Dropped und gut is'
    "Bookmarked": "Plan to Watch"
}

# Anime-Informationen hinzufügen
for status in data['anime']:
    for anime in data['anime'][status]:
        anime_element = ET.SubElement(root, "anime")
        
        series_title = ET.SubElement(anime_element, "series_title")
        series_title.text = anime['title']
        
        series_episodes = ET.SubElement(anime_element, "series_episodes")
        series_episodes.text = str(anime['episodes'])
        
        my_watched_episodes = ET.SubElement(anime_element, "my_watched_episodes")
        my_watched_episodes.text = str(anime['episodes'])
        
        my_score = ET.SubElement(anime_element, "my_score")
        my_score.text = str(anime['rating'])  
        if my_score.text == "100":
            my_score.text = my_score.text[0]+my_score.text[1]
        else:
            my_score.text = my_score.text[0]  # anisearch gibt Rating mit 'ner extra 0 hinter raus, weg damit
        
        my_status = ET.SubElement(anime_element, "my_status")
        my_status.text = str(status_mapping.get(status, 6))  # auf "Plan to Watch" zurückfallen wenn's nicht angegeben ist
        
        # series_animedb_id abrufen
        series_animedb_id = ET.SubElement(anime_element, "series_animedb_id")
        series_animedb_id.text = str(get_anime_id(anime['title']))  # der Aufruf ist natürlich bei großen Listen ungünstig. Entweder Geduld aufbringen oder umschreiben lol. Ist one-time thing von daher ok I guess.
        
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

# XML-Datei speichern
tree = ET.ElementTree(root)
tree.write(xml_filename, encoding='utf-8', xml_declaration=True)

print(f"Deine anisearch JSON wurde in XML umgewandelt und als '{xml_filename}' gespeichert. Enjoy.")
