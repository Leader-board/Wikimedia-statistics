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

## Notes

* Converting to SPSS using the script has a flaw in that it can only process strings up to 255 characters. This will result in the SAV file having multiple columns for the message, which will need to be concatenated. This can be done by computing a new variable, ensuring that it is a string with sufficiently large size (6600 characters worked), and entering the below as the command:

```
CONCAT(content,CONTE1,CONTE2,CONTE3,CONTE4,CONTE5, CONTE6, CONTE7, CONTE8, CONTE9, CONTEA, CONTEB, CONTEC, CONTED, CONTEE, CONTEF, CONTEG, CONTEH, CONTEI, CONTEJ, CONTEK, CONTEL, CONTEM, CONTEN)
```

This will also reduce the size of the SPSS file - from ~ 58 GB to ~ 12 GB.
* The script used up to 18 GB of RAM - make sure that the host system has a sufficient amount of memory.
