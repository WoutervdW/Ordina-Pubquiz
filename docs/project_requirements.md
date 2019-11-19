Requirements Ordina pubquiz - MoSCoW
-------------------

M
-------------------
- Geschreven tekst herkenning
	- Tekst in vast formaat
(Het lijkt er op dat enkel 1 woord of max. 1 regel tegelijk ingegeven zal kunnen worden:)
	- pre-processing van image in losse regels en/of woorden.
	- pre-processing als correctie voor belichting.
	

- Goede antwoord uit digitale tekst kunnen halen.
	- digitale tekst representeert niet altijd perfect het geschreven antwoord.
	= Meerdere antwoordmogelijkheden moeten goed gekeurd kunnen worden.
	
- Scores uitrekenen.

- Scores displayen.


S
-------------------
- Handmatig antwoorden na kunnen kijken.
	- Aangeven wanneer antwoorden handmatig nagekeken moeten worden door e.g. te lage confidence of onbegrijpelijke tekst.
	- Voor bepaalde vragen in kunnen voeren of het antwoord goed of fout was en dit verwerken bij het aantal punten.

- GUI score display.


"""
some ideas for pre processing:
- The input will probably a pdf. So the first processing step is the conversion of pdf to png
    - preferable png will be used since in jpg there is a loss of detail.
- The answer sheet should be separated in separate lines. This can be done using the lines given in the template
- increase contract for small lines
- word segmentation
        https://medium.com/@arthurflor23/text-segmentation-b32503ef2613
- word deslanting:
        https://github.com/githubharald/DeslantImg
"""

C
-------------------
- Manier om goed beeld te maken van geschreven tekst.
	- Nadenken over camera, belichting en grootte en hoeveelheid tekst in één afbeelding.


W
-------------------
- 



