# myhangar_parser
I put together a very simple Python script to parse saved Roberts Space Industries (Star Citizen) My Hangar pages (.html) for pledge and items data and store it into tables (.tsv), offline, without the security or privacy concerns of linking some app to your account or browser.

I just wanted a simple table of the ships I owned, without BS.

The data fields the script extracts include:

For each pledge / package:
* pledge id - (8 digit ID)
* pledge name - (e.g. Digital Goodies Pack - CitizenCon 2949 Digital Goodies Pack)
* pledge value - (e.g. $##.## USD)
* pledge configuration value - (e.g. modded 300 series - $##.## USD)

For each item:
* item title - (e.g. CitizenCon 2949 In-Game Carrack Plushie)
* item kind - (e.g. Hangar decoration)
* item liner - (e.g. Anvil Aerospace (ANVL) )

Usage: Use your web browser to save each page from your "My Hangar" as 'p1.html', 'p2.html', ... 'pN.html' in the working directory, run the script, input the 'N' pages you downloaded, open the .tsv files in Excel. Easy!
