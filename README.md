
# anisearch-to-myanimelist

A little script that converts your exported .json file from anisearch.de and creates a suitable .xml file for import on myanimelist.com 🎌
Source code's in german here and there but that's probably no biggy since it's for anisearch users who are mainly german anyways.

If you have issues please contact me on [Twitter](https://twitter.com/voidedmile) or [Discord](https://discord.com/users/104627481767604224) 




## What you need

- Python installed on your machine to execute the script: https://www.python.org/downloads/
- The [requests HTTP library](https://pypi.org/project/requests/)
- A client ID to access the [MAL-API](https://myanimelist.net/clubs.php?cid=13727) which you can [configure here](https://myanimelist.net/apiconfig)


## How to Use

- Export your anisearch anime list: https://www.anisearch.de/usercp/list/anime/export
- Edit the script with your MAL developer client ID and the name of your .json file
- Make sure both the script and the .json file are in the same folder and then execute the script
- Wait for a while for it to finish (depends on the size of your list, really)
- Head over to the MAL [import page](https://myanimelist.net/import.php), choose MyAnimeList Import as the type and enjoy


## Change log:

- added timetracking
- added logfile in case of sus IDs
- added asynchronous handling of the API calls (cuts down the execution time by a lot. apparently, hitting the MAL API rate-limit's hard lol)

Feel free to contribute and have a wonderful day! c:
