
# anisearch-to-myanimelist

A little script that converts your exported .json file from anisearch.de and creates a suitable .xml file for import on myanimelist.com 🎌

If you have issues please contact me on [Twitter](https://twitter.com/voidedmile) or [Discord](https://discord.com/users/104627481767604224) 





## What you need

- Python installed on your machine to execute the script: https://www.python.org/downloads/
- The [requests HTTP library](https://pypi.org/project/requests/)
- A client ID to access the [MAL-API](https://myanimelist.net/clubs.php?cid=13727) which you can [configure here](https://myanimelist.net/apiconfig)
## Possible Improvements

Now, as you need the series_animedb_id from MAL there'll be an API call for each anime to figure it out. To speed up the script you could probably add multithreading or work through the API calls in a batch instead.

For reference, my list that has 273 anime took around 5 minutes to complete. That's around 1 second per anime. I personally think that's okay since I didn't want to hit any rate limits with the MAL API.

Feel free to contribute and have a wonderful day! c:
