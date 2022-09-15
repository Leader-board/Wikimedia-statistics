# Discord analyser

This takes in JSON files created using [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) and outputs

* Excel files for every channel, and overall (as long as row limits are met)
* pickle files as dataframes (Pandas) - helps for future analysis
* SPSS (.sav) files for overall.
* User frequency (by number of messages) for each channel, and overall.

It is also easy to export to CSV, but from my experience this doesn't work as well. This is because of line breaks which most programs struggle to differentiate from new lines. 

This can be customised as necessary. 

The statistical results themselves for the Wikipedia Discord are available at https://github.com/Leader-board/Wikimedia-statistics/releases.

## Getting the JSON files

Use [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter). With 10 parallel imports, this took about 3 hours for the Wikipedia Discord, with most of the time being from the new page feed (which is handled by a bot). 
