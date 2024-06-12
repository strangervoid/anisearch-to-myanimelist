
# anisearch-to-myanimelist

A little script that converts your exported .json file from anisearch.de and creates a suitable .xml file for import on myanimelist.com 🎌

If you have issues please contact me on [Twitter](https://twitter.com/voidedmile) or [Discord](https://discord.com/users/104627481767604224) 





## What you need

- Python installed on your machine to execute the script: https://www.python.org/downloads/
- The [requests HTTP library](https://pypi.org/project/requests/)
- A client ID to access the [MAL-API](https://myanimelist.net/clubs.php?cid=13727) which you can [configure here](https://myanimelist.net/apiconfig)


## How to Use

- Export your anisearch anime list: https://www.anisearch.de/usercp/list/anime/export
- Make sure both the script and the .json file are in the same folder and then execute the script
- Wait for a while for it to finish (depends on the size of your list, really)
- Head over to the MAL [import page](https://myanimelist.net/import.php), choose MyAnimeList Import as the type and enjoy


## Possible Improvements

Now, as you need the series_animedb_id from MAL there'll be an API call for each anime to figure it out. To speed up the script you could probably add multithreading or work through the API calls in a batch instead.

For reference, my list that has 273 anime took around 5 minutes to complete. That's around 1 second per anime. I personally think that's okay since I didn't want to hit any rate limits with the MAL API.

Feel free to contribute and have a wonderful day! c:
