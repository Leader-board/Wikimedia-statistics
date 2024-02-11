#!/bin/bash
cd /statdata/Wikimedia-statistics
git pull
pip install --user iso639-lang requests pandas mysql-connector-python # useful if not already installed
mysql --defaults-file="$HOME"/replica.my.cnf -h meta.analytics.db.svc.wikimedia.cloud meta_p -e "SELECT GROUP_CONCAT(dbname SEPARATOR ' ') FROM wiki;" INTO OUTFILE wiki_list.txt;
time ./scripter.sh "$(<wiki_list.txt)" # wiki_list = space_separated list of wikis, obtained programmatically
# time ./scripter.sh aawiki aawikibooks aawiktionary abwiki abwiktionary acewiki advisorywiki adywiki afwiki afwikibooks afwikiquote afwiktionary akwiki akwikibooks akwiktionary alswiki altwiki amiwiki amwiki amwikimedia amwikiquote amwiktionary angwiki angwikibooks angwikiquote angwikisource angwiktionary anpwiki anwiki anwiktionary apiportalwiki arcwiki arwiki arwikibooks arwikimedia arwikinews arwikiquote arwikisource arwikiversity arwiktionary arywiki arzwiki astwiki astwikibooks astwikiquote astwiktionary aswiki aswikibooks aswikiquote aswikisource aswiktionary atjwiki avkwiki avwiki avwiktionary awawiki aywiki aywikibooks aywiktionary azbwiki azwiki azwikibooks azwikimedia azwikiquote azwikisource azwiktionary banwiki banwikisource barwiki bat_smgwiki bawiki bawikibooks bclwiki bclwikiquote bclwiktionary bdwikimedia betawikiversity bewiki bewikibooks bewikimedia bewikiquote bewikisource bewiktionary be_x_oldwiki bgwiki bgwikibooks bgwikinews bgwikiquote bgwikisource bgwiktionary bhwiki bhwiktionary biwiki biwikibooks biwiktionary bjnwiki bjnwiktionary blkwiki bmwiki bmwikibooks bmwikiquote bmwiktionary bnwiki bnwikibooks bnwikiquote bnwikisource bnwikivoyage bnwiktionary bowiki bowikibooks bowiktionary bpywiki brwiki brwikimedia brwikiquote brwikisource brwiktionary bswiki bswikibooks bswikinews bswikiquote bswikisource bswiktionary bugwiki bxrwiki cawiki cawikibooks cawikimedia cawikinews cawikiquote cawikisource cawiktionary cbk_zamwiki cdowiki cebwiki cewiki chowiki chrwiki chrwiktionary chwiki chwikibooks chwiktionary chywiki ckbwiki ckbwiktionary cnwikimedia commonswiki cowiki cowikibooks cowikimedia cowikiquote cowiktionary crhwiki crwiki crwikiquote crwiktionary csbwiki csbwiktionary cswiki cswikibooks cswikinews cswikiquote cswikisource cswikiversity cswiktionary cuwiki cvwiki cvwikibooks cywiki cywikibooks cywikiquote cywikisource cywiktionary dagwiki dawiki dawikibooks dawikiquote dawikisource dawiktionary dewiki dewikibooks dewikinews dewikiquote dewikisource dewikiversity dewikivoyage dewiktionary dinwiki diqwiki diqwiktionary dkwikimedia donatewiki dsbwiki dtywiki dvwiki dvwiktionary dzwiki dzwiktionary eewiki elwiki elwikibooks elwikinews elwikiquote elwikisource elwikiversity elwikivoyage elwiktionary emlwiki enwiki enwikibooks enwikinews enwikiquote enwikisource enwikiversity enwikivoyage enwiktionary eowiki eowikibooks eowikinews eowikiquote eowikisource eowikivoyage eowiktionary eswiki eswikibooks eswikinews eswikiquote eswikisource eswikiversity eswikivoyage eswiktionary etwiki etwikibooks etwikimedia etwikiquote etwikisource etwiktionary euwiki euwikibooks euwikiquote euwikisource euwiktionary extwiki fatwiki fawiki fawikibooks fawikinews fawikiquote fawikisource fawikivoyage fawiktionary ffwiki fiu_vrowiki fiwiki fiwikibooks fiwikimedia fiwikinews fiwikiquote fiwikisource fiwikiversity fiwikivoyage fiwiktionary fjwiki fjwiktionary foundationwiki fowiki fowikisource fowiktionary frpwiki frrwiki frwiki frwikibooks frwikinews frwikiquote frwikisource frwikiversity frwikivoyage frwiktionary furwiki fywiki fywikibooks fywiktionary gagwiki ganwiki gawiki gawikibooks gawikiquote gawiktionary gcrwiki gdwiki gdwiktionary gewikimedia glkwiki glwiki glwikibooks glwikiquote glwikisource glwiktionary gnwiki gnwikibooks gnwiktionary gomwiki gomwiktionary gorwiki gorwiktionary gotwiki gotwikibooks grwikimedia gucwiki gurwiki guwiki guwikibooks guwikiquote guwikisource guwiktionary guwwiki guwwikinews guwwikiquote guwwiktionary gvwiki gvwiktionary hakwiki hawiki hawiktionary hawwiki hewiki hewikibooks hewikinews hewikiquote hewikisource hewikivoyage hewiktionary hifwiki hifwiktionary hiwiki hiwikibooks hiwikimedia hiwikiquote hiwikisource hiwikiversity hiwikivoyage hiwiktionary howiki hrwiki hrwikibooks hrwikiquote hrwikisource hrwiktionary hsbwiki hsbwiktionary htwiki htwikisource huwiki huwikibooks huwikinews huwikiquote huwikisource huwiktionary hywiki hywikibooks hywikiquote hywikisource hywiktionary hywwiki hzwiki iawiki iawikibooks iawiktionary idwiki idwikibooks idwikimedia idwikiquote idwikisource idwiktionary iewiki iewikibooks iewiktionary igwiki igwikiquote igwiktionary iiwiki ikwiki ikwiktionary ilowiki incubatorwiki inhwiki iowiki iowiktionary iswiki iswikibooks iswikiquote iswikisource iswiktionary itwiki itwikibooks itwikinews itwikiquote itwikisource itwikiversity itwikivoyage itwiktionary iuwiki iuwiktionary jamwiki jawiki jawikibooks jawikinews jawikiquote jawikisource jawikiversity jawikivoyage jawiktionary jbowiki jbowiktionary jvwiki jvwikisource jvwiktionary kaawiki kabwiki kawiki kawikibooks kawikiquote kawiktionary kbdwiki kbdwiktionary kbpwiki kcgwiki kcgwiktionary kgwiki kiwiki kjwiki kkwiki kkwikibooks kkwikiquote kkwiktionary klwiki klwiktionary kmwiki kmwikibooks kmwiktionary knwiki knwikibooks knwikiquote knwikisource knwiktionary koiwiki kowiki kowikibooks kowikinews kowikiquote kowikisource kowikiversity kowiktionary krcwiki krwiki krwikiquote kshwiki kswiki kswikibooks kswikiquote kswiktionary kuwiki kuwikibooks kuwikiquote kuwiktionary kvwiki kwwiki kwwikiquote kwwiktionary kywiki kywikibooks kywikiquote kywiktionary labswiki ladwiki lawiki lawikibooks lawikiquote lawikisource lawiktionary lbewiki lbwiki lbwikibooks lbwikiquote lbwiktionary lezwiki lfnwiki lgwiki lijwiki lijwikisource liwiki liwikibooks liwikinews liwikiquote liwikisource liwiktionary lldwiki lmowiki lmowiktionary lnwiki lnwikibooks lnwiktionary loginwiki lowiki lowiktionary lrcwiki ltgwiki ltwiki ltwikibooks ltwikiquote ltwikisource ltwiktionary lvwiki lvwikibooks lvwiktionary madwiki maiwiki maiwikimedia map_bmswiki mdfwiki mediawikiwiki metawiki mgwiki mgwikibooks mgwiktionary mhrwiki mhwiki mhwiktionary minwiki minwiktionary miwiki miwikibooks miwiktionary mkwiki mkwikibooks mkwikimedia mkwikisource mkwiktionary mlwiki mlwikibooks mlwikiquote mlwikisource mlwiktionary mniwiki mniwiktionary mnwiki mnwikibooks mnwiktionary mnwwiki mnwwiktionary mrjwiki mrwiki mrwikibooks mrwikiquote mrwikisource mrwiktionary mswiki mswikibooks mswiktionary mtwiki mtwiktionary muswiki mwlwiki mxwikimedia myvwiki mywiki mywikibooks mywiktionary mznwiki nahwiki nahwikibooks nahwiktionary napwiki napwikisource nawiki nawikibooks nawikiquote nawiktionary ndswiki ndswikibooks ndswikiquote ndswiktionary nds_nlwiki newiki newikibooks newiktionary newwiki ngwiki ngwikimedia niawiki niawiktionary nlwiki nlwikibooks nlwikimedia nlwikinews nlwikiquote nlwikisource nlwikivoyage nlwiktionary nnwiki nnwikiquote nnwiktionary nostalgiawiki novwiki nowiki nowikibooks nowikimedia nowikinews nowikiquote nowikisource nowiktionary nqowiki nrmwiki nsowiki nvwiki nycwikimedia nywiki nzwikimedia ocwiki ocwikibooks ocwiktionary olowiki omwiki omwiktionary orwiki orwikisource orwiktionary oswiki outreachwiki pagwiki pamwiki papwiki pawiki pawikibooks pawikisource pawiktionary pa_uswikimedia pcdwiki pcmwiki pdcwiki pflwiki pihwiki piwiki piwiktionary plwiki plwikibooks plwikimedia plwikinews plwikiquote plwikisource plwikivoyage plwiktionary pmswiki pmswikisource pnbwiki pnbwiktionary pntwiki pswiki pswikibooks pswikivoyage pswiktionary ptwiki ptwikibooks ptwikimedia ptwikinews ptwikiquote ptwikisource ptwikiversity ptwikivoyage ptwiktionary punjabiwikimedia pwnwiki qualitywiki quwiki quwikibooks quwikiquote quwiktionary rmwiki rmwikibooks rmwiktionary rmywiki rnwiki rnwiktionary roa_rupwiki roa_rupwiktionary roa_tarawiki romdwikimedia rowiki rowikibooks rowikinews rowikiquote rowikisource rowikivoyage rowiktionary rswikimedia ruewiki ruwiki ruwikibooks ruwikimedia ruwikinews ruwikiquote ruwikisource ruwikiversity ruwikivoyage ruwiktionary rwwiki rwwiktionary sahwiki sahwikiquote sahwikisource satwiki sawiki sawikibooks sawikiquote sawikisource sawiktionary scnwiki scnwiktionary scowiki scwiki scwiktionary sdwiki sdwikinews sdwiktionary sewiki sewikibooks sewikimedia sgwiki sgwiktionary shiwiki shnwiki shnwikibooks shnwikivoyage shnwiktionary shwiki shwiktionary shywiktionary simplewiki simplewikibooks simplewikiquote simplewiktionary siwiki siwikibooks siwiktionary skrwiki skrwiktionary skwiki skwikibooks skwikiquote skwikisource skwiktionary slwiki slwikibooks slwikiquote slwikisource slwikiversity slwiktionary smnwiki smwiki smwiktionary snwiki snwiktionary sourceswiki sowiki sowiktionary specieswiki sqwiki sqwikibooks sqwikinews sqwikiquote sqwiktionary srnwiki srwiki srwikibooks srwikinews srwikiquote srwikisource srwiktionary sswiki sswiktionary stqwiki strategywiki stwiki stwiktionary suwiki suwikibooks suwikiquote suwiktionary svwiki svwikibooks svwikinews svwikiquote svwikisource svwikiversity svwikivoyage svwiktionary swwiki swwikibooks swwiktionary szlwiki szywiki tawiki tawikibooks tawikinews tawikiquote tawikisource tawiktionary taywiki tcywiki tenwiki test2wiki testcommonswiki testwiki testwikidatawiki tetwiki tewiki tewikibooks tewikiquote tewikisource tewiktionary tgwiki tgwikibooks tgwiktionary thankyouwiki thwiki thwikibooks thwikinews thwikiquote thwikisource thwiktionary tiwiki tiwiktionary tkwiki tkwikibooks tkwikiquote tkwiktionary tlwiki tlwikibooks tlwikiquote tlwiktionary tnwiki tnwiktionary towiki towiktionary tpiwiki tpiwiktionary trvwiki trwiki trwikibooks trwikimedia trwikinews trwikiquote trwikisource trwikivoyage trwiktionary tswiki tswiktionary ttwiki ttwikibooks ttwikiquote ttwiktionary tumwiki twwiki twwiktionary tyvwiki tywiki uawikimedia udmwiki ugwiki ugwikibooks ugwikiquote ugwiktionary ukwiki ukwikibooks ukwikinews ukwikiquote ukwikisource ukwikivoyage ukwiktionary urwiki urwikibooks urwikiquote urwiktionary usabilitywiki uzwiki uzwikibooks uzwikiquote uzwiktionary vecwiki vecwikisource vecwiktionary vepwiki vewiki vewikimedia viwiki viwikibooks viwikiquote viwikisource viwikivoyage viwiktionary vlswiki votewiki vowiki vowikibooks vowikiquote vowiktionary warwiki wawiki wawikibooks wawikisource wawiktionary wbwikimedia wikidatawiki wikimania2005wiki wikimania2006wiki wikimania2007wiki wikimania2008wiki wikimania2009wiki wikimania2010wiki wikimania2011wiki wikimania2012wiki wikimania2013wiki wikimania2014wiki wikimania2015wiki wikimania2016wiki wikimania2017wiki wikimania2018wiki wikimaniawiki wowiki wowikiquote wowiktionary wuuwiki xalwiki xhwiki xhwikibooks xhwiktionary xmfwiki yiwiki yiwikisource yiwiktionary yowiki yowikibooks yowiktionary yuewiktionary zawiki zawikibooks zawikiquote zawiktionary zeawiki zhwiki zhwikibooks zhwikinews zhwikiquote zhwikisource zhwikiversity zhwikivoyage zhwiktionary zh_classicalwiki zh_min_nanwiki zh_min_nanwikibooks zh_min_nanwikiquote zh_min_nanwikisource zh_min_nanwiktionary zh_yuewiki zuwiki zuwikibooks zuwiktionary