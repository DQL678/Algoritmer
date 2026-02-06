# Algoritmer
## Projektformulering
### Idébeskrivelse
Vi har i gruppen tænkt os at lave et spil, der hedder "Protect at All Costs", som er et strategi og defense spil, der omhandler algoritmer. Måden, det her spil fungerer på, er, at man som spiller skal forsvare sit flag fra fjenden, hvis mål er at pathfinde så effektivt som muligt hen mod det. Så noget, der minder om Capture the Flag. Dette foregår på et stort map med en masse grids, hvor du vinder over fjenden ved at få dem til at bruge mere end de designeret antal steps, de har adgang til. Eksempelvis kan fjenden have 30 steps til at nå dit flag, og hvis den bruger mere end det, har du vundet. Hvis den bruger under antal steps og når dit flag, så har du tabt. Måden du kan forsvare dit flag på, er ved at placere flaget et bestemt sted på mappen og bruge vægge til at blokere for fjenden og tvinge dem til at pathfinde en anden vej hen til dit flag, hvilket tvinger dem til at bruge flere steps. Dette inddrager et labyrint-princip, så du skaber blokeringer, som skal sørge for, at fjenden tager længere tid for at nå dit flag. Fjenden har et bestemt spawn-location på mappet, hvilket gør, at man som spiller skal arbejde rundt om det, eftersom dette spawn er tilfældigt. De blocks eller vægge, man bruger til at forsvare sit flag, mister man hvert level, så derfor indgår der også noget strategi i spillet, eftersom man skal vide præcis, hvor mange blocks man skal bruge, uden at man bruger for mange og uden man bruger for få. Efter hver level tjener spilleren et bestemt antal mønter, hvor spilleren så skal kunne bruge disse mønter på at købe flere vægge, upgrades og måske senere hen i spillet et større map. Efter hver runde får fjenden flere og flere steps at arbejde med, hvilket gør spillet sværere og sværere. En good to have eller nice to have kan være, at fjenden/maps har en sværhedsgrad, hvor den nemmeste sværhedsgrad er en fjende, som ikke er så effektiv til at pathfinde, hvor den sværeste sværhedsgrad kan være en fjende, som  nemt kan pathfinde, som for eksempel A*.

### Programstruktur
Programmet er designet som et strategispil med ture og niveauer. I hver runde gennemløbes en fast struktur, hvor spilleren først opstiller sit forsvar, hvorefter algoritmen benytter pathfinding til at forsøge at nå spillerens flag.

**Overordnet flow:**
1. Spillet starter og mappet genereres som et grid
2. Algoritmens spawn-position placeres (foruddefineret/random)
3. Spilleren placerer sit flag på mappet
4. Spilleren placerer vægge (begrænset antal)
5. Algoritmen forsøger at finde den mest effektive vej til flaget
6. Antallet af steps tælles undervejs
7. Spillet evaluerer:
   - Hvis algoritmen bruger flere end det tilladte antal steps --> spilleren vinder
   - Hvis algoritmen når flaget inden for step-grænsen --> spilleren taber
8. Spilleren modtager penge
9. Næste level starter med øget sværhedsgrad

**Klassestruktur**

Programmet kan struktureres med følgende klasser/moduler (vi er ikke helt sikker endnu):

Game
   - Styrer spillets flow, levels og regler

Grid / Map
   - Repræsenterer spillebanen og håndterer placering af vægge, flag og algoritme

AIPathfinder
   - Indeholder pathfinding-algoritmen og step-tælling

Player
   - Håndterer spillerens ressourcer (penge, vægge, flag-placering)

LevelManager
   - Justerer sværhedsgrad, step-limit og belønninger mellem levels

### Liste af features
- Pathfinding af fjende (fra start til slutpunkt).

- Gridmap.

- Placering af flag og vægge/blocks i grids fra spiller.

- Shop med Upgrades/Powerups (flere vægge/Forskellige slags vægge, større map og andre positives for spilleren eller negatives for fjenden).

- Sværhedsgrader til fjende/maps.

### Kilder/inspiration
Capture the flag, Bloons Tower Defense (defense spil generelt).

### Infrastruktur
Github: https://github.com/DQL678/Algoritmer

Trello: https://trello.com/b/Eyzfs3td/algoritmer
