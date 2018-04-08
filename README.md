# Backend-dej-uran-dom
Repozitář týmu dej/uran/dom na soutěži UnIT Brno 2018

Aplikace pro příkazovou řádku pro rozpoznávání kruhových částic v předaném obrázku typu TIFF.
Pro detekci hran je použita hranová funkce. Ve spolupráci s **Houghovou transformací kružnice** jsou poté odhlasovány kandidátní kružnice pro všechny částice (komponenty). Ty rozděleny na **hlavní komponenty a subkomponenty**, které jsou následně shlukovány. Výstupem jsou poté změřené částice obsažené v **rozšířených AABB boxes** (určených ze subkomponent).

# Výsledky
Obrázek vpravo je vždy originál, vlevo jsou vizualizované výsledky - přerušované **červené obdelníky** jsou rozšířené AABB **boxy**, kružnice přerušovanou čarou jsou **hlavní komponenty** částic, kružnice plnou čarou pak **subkomponenty částic**.

![results/1_0.tif.png](/results/1_0.tif.png)
![results/0.tif.png](/results/0.tif.png)
![results/2.tif.png](/results/2.tif.png)
![results/3.tif.png](/results/3.tif.png)
![results/6_0.tif.png](/results/6_0.tif.png)
![results/8_0.tif.png](/results/8_0.tif.png)
![results/1.tif.png](/results/1.tif.png)
![results/3_0.tif.png](/results/3_0.tif.png)
![results/7_0.tif.png](/results/7_0.tif.png)

### Ty méně povedené
![results/2_0.tif.png](/results/2_0.tif.png)
![results/5_0.tif.png](/results/5_0.tif.png)
![results/9_0.tif.png](/results/9_0.tif.png)
![results/4.tif.png](/results/4.tif.png)
![results/11_0.tif.png](/results/11_0.tif.png)
