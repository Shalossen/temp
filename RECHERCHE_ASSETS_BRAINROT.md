# Recherche d'assets : map Fortnite (UEFN) style « brainrot »

> Rapport de recherche basé sur tes 5 captures (Go Up For Brainrots, Steal the Brainrot) et sur des sources web consultées le 9 octobre 2026.
> Objectif : trouver/produire des assets « addictifs » (brainrots voxel, mutations glitchy, effets) pour construire ta propre map UEFN.

---

## TL;DR

1. **Les brainrots ne sont pas « à personne », mais leur statut n'est pas tranché.** Les mèmes d'origine ont été générés par IA, et aux États-Unis une image 100 % IA n'est pas protégeable par le droit d'auteur. Mais une agence (Mementum) revendique 23 personnages, des marques sont déposées, et **Epic a lui-même pris une licence** pour vendre les skins Tung Tung Tung Sahur et Ballerina Cappuccina (avril 2026). Beaucoup de brainrots de tes captures ont en plus été créés par les studios eux-mêmes. Détail des risques par niveau en section 2.
2. **Crée tes propres brainrots** en suivant la même formule : *objet du quotidien + animal + nom pseudo-italien*, en style voxel/blocky. Pars de bases **CC0** (Kenney *Cube Pets*, *Voxel Creature Pack* d'OpenGameArt, Quaternius) et retouche-les dans **MagicaVoxel / Blockbench / Blender**.
3. **Le côté « glitchy / addictif » vient surtout des matériaux.** Un seul modèle × 6 mutations (Neon, Crystal, Void, Party, Dreamy, Black&White…) = 6 variantes pour presque rien. Tu fais un *master material* dans UEFN et une *material instance* par mutation.
4. **Ajoute les boucles de jeu** visibles sur tes captures : raretés, timers « garanti », events tournants, rebirths, cash hors-ligne, leaderboard, annonces de spawn rare.

---

## 1. Ce que montrent tes captures (ce qui rend ces maps addictives)

| Élément | Ce qu'on voit | Pourquoi ça accroche |
|---|---|---|
| **Personnages** | Créatures voxel géantes : gorille étoilé, requin-glace, flamant-croissant arc-en-ciel, T-rex-tracteur, éléphant-fraise, pingouin-armure, Godzilla-maïs | Absurde + lisible de loin + couleurs saturées |
| **Raretés** | `Divine`, `Secret`, `Ascended` ; panneaux « GUARANTEED DIVINE : 3d 0h 40m », « ASCENDED SPAWN FOR EVERYONE in 2d » | Rareté = désir. Les timers « garanti » donnent un rendez-vous et font revenir les joueurs |
| **Mutations** | `Black&White`, `Summer`, `Dreamy`, `Party`, `Void`, `Neon`, `Crystal` au-dessus du nom | Chaque mutation est un skin matériau sur le même mesh, donc beaucoup de contenu à collectionner pour peu de travail |
| **Économie** | `$/s` par brainrot, nombres énormes (`B`, `T`, `Qa`, `Qi`, `Sx`), pads verts « Collect », *Offline Cash* | Les chiffres qui explosent donnent une sensation de progression permanente |
| **Méta-progression** | Rebirths, Jump (Go Up), Steals, Cash/s dans le leaderboard | Prestige, et une raison de recommencer |
| **Machines / lieux** | Mutation Machine, Brainrot Machine, SELL, Upgrade Shop, Trading Center, VIP, cadeau « FREE », Wall of Fame, clavier à codes | Plusieurs « verbes » de jeu : collecter, muter, vendre, échanger, améliorer |
| **Events tournants** | Party (16 min restantes), Summer (1h51), Dreamy (51 min), Halloween (21 min) | Il y a toujours un event dans moins d'une heure, donc on reste |
| **Objectif communautaire** | Barre « 52 751 / 75 000 » | Engagement collectif |
| **Feedback** | Bannière « Divine Brainrot Spawned », confettis, paillettes, néons | Récompense visuelle immédiate |

---

## 2. ⚠️ Droits d'auteur : à lire avant de choisir tes assets

*(Ceci n'est pas un avis juridique, juste ce que disent les sources.)*

### 2.1 « Ce sont des mèmes du web, ils n'appartiennent à personne » : vrai en partie seulement

- **L'argument « IA = domaine public » existe, mais il n'est pas tranché.** Aux États-Unis, une œuvre générée entièrement par IA n'est pas protégeable par le droit d'auteur ([Thaler v. Perlmutter](https://www.loeb.com/en/insights/publications/2025/03/thaler-v-perlmutter), mars 2025). C'est exactement ce que plaide Spyder Games (studio de *Steal a Brainrot*). D'après eux, Tung Tung Tung Sahur est né de 7 prompts en 15 minutes. → [Dexerto](https://www.dexerto.com/roblox/tung-tung-sahur-is-at-the-center-of-a-bizarre-federal-custody-battle-over-brainrot-characters-3381733/)
- **Mais quelqu'un revendique ces personnages.** L'agence française Mementum Labs dit représenter les créateurs (Noxa, Breno). Elle revendique Tung Tung Tung Sahur **et 22 autres brainrots**, à la fois par le droit d'auteur (noms, histoires, voix…) et par le droit des marques. Le procès est en cours aux États-Unis, sans décision à ce jour. → [GamesBeat](https://gamesbeat.com/the-battle-over-tung-tung-tung-sahur-is-testing-the-limits-of-copyright-and-trademark-law/), [Law Society Journal](https://lsj.com.au/articles/who-owns-brainrot/)
- **Des marques sont déposées.** Aux États-Unis, une société a déposé « TUNG TUNG TUNG SAHUR » et « TRALALERO TRALALA » (jouets, mai 2025). Une autre entité a enregistré Tung Tung Tung Sahur comme marque dans l'UE. → [Trademarkia](https://www.trademarkia.com/news/intellectual-property-news/tung-tung-sahur-trademark), [USPTO 99171194](https://uspto.report/TM/99171194)
- **Epic a pris une licence.** Les skins Tung Tung Tung Sahur et Ballerina Cappuccina vendus dans la boutique Fortnite (avril 2026) sont présentés comme un partenariat officiel avec Mementum. Concrètement, Epic traite Mementum comme l'ayant droit. → [GamesBeat](https://gamesbeat.com/the-battle-over-tung-tung-tung-sahur-is-testing-the-limits-of-copyright-and-trademark-law/), [Beebom](https://beebom.com/fortnite-tung-tung-tung-sahur-ballerina-cappuccina-skin/amp/)
- **Beaucoup de brainrots de tes captures ne sont pas des mèmes du web.** Ils ont été inventés par les studios. Exemples : Strawberry Elephant (ajouté par les devs de *Steal a Brainrot* le 30 août 2025) et Chicleteira Bicicleteira (brainrot « Secret » du jeu Roblox). Ceux-là appartiennent clairement à leurs créateurs. → [Deltia's Gaming](https://deltiasgaming.com/how-to-get-og-strawberry-elephant-in-steal-a-brainrot-roblox), [The Backdash](https://thebackdash.com/gaming/chicleteira-bicicleteira-in-steal-a-brainrot-how-to-get-income-rate-and-more/)
- **Les modèles 3D sont toujours protégés.** Même si le mème était libre, les modèles 3D faits par l'équipe de Ferins ou par Spyder sont leur travail. Les extraire ou les copier, c'est copier leur œuvre.

### 2.2 Ce qui s'est déjà passé sur Fortnite

- **Ferins (Steal the Brainrot) a une licence** pour le *jeu* Steal a Brainrot, accordée par Spyder Games/DoBig. Il dit aussi collaborer avec eux pour faire retirer les maps contrefaisantes. → [Pocket Tactics](https://www.pockettactics.com/fortnite/steal-the-brainrot-lawsuit)
- **Octobre 2025 : procès contre une copie Fortnite.** Spyder Games a attaqué le créateur de *Stealing Brainrots* pour « copie en gros » (artwork, assets, design), en demandant le retrait, des dommages et une part des revenus. → [Gamewave (FR)](https://gamewave.fr/roblox/steal-a-brainrot-le-phenomene-roblox-attaque-fortnite-pour-plagiat/), [Aftermath](https://aftermath.site/brainrot-roblox-court/)
- **Règles Epic.** Pas de contenu qui viole des droits tiers. Le propriétaire de l'équipe est responsable, et les sanctions vont du retrait de l'île jusqu'au ban du compte. → [Island Creator Rules](https://www.epicgames.com/help/en-US/c-Category_CreatorPrograms/c-Trending_0/fortnite-island-creator-rules-a000094823), [Guide IP/DMCA](https://www.fortnite.com/news/intellectual-property-ip-and-dmca-guidelines-for-fortnite-island-creators)

### 2.3 Niveau de risque par type d'asset

| Risque | Quoi | Pourquoi |
|---|---|---|
| 🔴 Élevé | Modèles extraits des maps de Ferins/Spyder ; brainrots inventés par les studios (Strawberry Elephant, Chicleteira…) ; copie 1:1 d'un jeu | Œuvres humaines clairement protégées, et précédent judiciaire sur Fortnite |
| 🟠 Moyen | Tung Tung Tung Sahur, Ballerina Cappuccina, Tralalero Tralala et les autres « mèmes d'origine », **refaits par toi en 3D** | Statut juridique non tranché, Mementum et des déposants de marques actifs, Epic licencié |
| 🟢 Faible | Tes propres brainrots dans le même style (section 7) | Le style et le genre ne sont pas protégeables en tant que tels |

**Si tu veux quand même les mèmes d'origine :** fais tes propres modèles (ne les extrais jamais), et sache qu'une plainte peut faire retirer ton île. La voie propre est de demander une licence à Mementum, qui a déjà licencié Fortnite, Plants vs Brainrots, Pudgy Party et Brainrot Fight. → [Dexerto](https://www.dexerto.com/roblox/tung-tung-sahur-is-at-the-center-of-a-bizarre-federal-custody-battle-over-brainrot-characters-3381733/)

---

## 3. Où trouver les assets

### 3.A Bases 3D libres (CC0) à transformer en brainrots

| Pack | Style | Licence | Formats | Pourquoi c'est utile |
|---|---|---|---|---|
| [Kenney – Cube Pets](https://opengameart.org/node/185352) ([kenney.nl](https://kenney.nl)) | Animaux **cubiques**, animés | CC0 | FBX, OBJ, glTF | La base la plus proche du look « Go Up » : tu ajoutes l'objet (frigo, toast, cactus…) dessus |
| [OpenGameArt – Voxel Creature Pack 1](https://opengameart.org/content/voxel-creature-pack1) | Voxel (canard vampire, poulet-requin gobelin, piranha à pieds…) | CC0 | `.vox` MagicaVoxel + modèles texturés | Déjà très « brainrot », et éditable directement dans MagicaVoxel |
| [Quaternius – LowPoly Animated Animals](https://quaternius.itch.io/lowpoly-animated-animals) | Low-poly animé | CC0 | FBX, OBJ, Blend | Squelettes et anims (Idle/Walk/Run…) ; un commentaire signale que certaines anims manquent, à vérifier dans le zip |
| [Quaternius – Ultimate Monsters](https://sketchfab.com/3d-models/ultimate-monsters-pack-fd72e114d119488da71fe3a16f216c4f) | 50 monstres animés | Annoncé CC0, mais Sketchfab affiche CC-BY : **vérifie sur quaternius.com** | Blend, FBX, OBJ, glTF | Bases pour les raretés « Secret » et « Ascended » |
| [Vox-Fox – Voxel Tiny Animals](https://vox-fox.itch.io/voxel-tiny-animals) | Voxel | Payant (dès 1 $) | VOX, OBJ, PNG | 21 animaux voxel propres |
| [3D Voxel Park Pack](https://mariaisme.itch.io/3d-voxel-park) | Voxel (chiens, oiseaux, écureuils + décor) | Prix libre, usage commercial OK, revente interdite | — | Animaux + décor de parc |

### 3.B Fab (directement dans UEFN)

- **La fenêtre Fab dans UEFN n'affiche que les produits utilisables dans UEFN.** Elle a des filtres *Free*, licence (CC-BY 4.0, Fab standard), style et tags, et une option « 3D compatible formats » (GLB, glTF, FBX, USDZ). → [Doc Epic](https://dev.epicgames.com/documentation/fortnite/fab-user-interface-reference-in-unreal-editor-for-fortnite?lang=en-US)
- Epic indique que les assets Fab pour UEFN sont prêts côté collision et budget mémoire, et à l'échelle Fortnite. → [Spotlight Fab/UEFN](https://www.fortnite.com/news/spotlight-fab-content-added-to-uefn-in-august-2023)
- Depuis le 15 octobre, Fab vend aussi des **source assets UEFN** (systèmes Verse/Scene Graph : IA, UI, véhicules…). Utile pour ne pas recoder un tycoon de zéro. → [Forum Epic](https://forums.unrealengine.com/t/uefn-source-assets-are-coming-to-fab-upload-yours-today/2833019)
- **Je n'ai trouvé aucun pack « brainrot » officiel sur Fab.** Les recherches utiles dans la fenêtre Fab de UEFN : `voxel`, `stylized`, `toon`, `crystal`, `neon`, `party`, `balloon`, `gift box`, `pedestal`, `conveyor`, `arcade`, `candy`.
- Le filtre « AI-created » existe, et Epic impose de déclarer les assets générés par IA sur Fab. → [80.lv](https://80.lv/articles/epic-games-adresses-ai-generated-content-plaguing-fab)

Packs Unreal pas confirmés compatibles UEFN (à tester, ou à prendre comme modèles à recréer) :
- [Glitch Material Pack](https://www.fab.com/listings/22721291-ad36-43e3-a351-8ee723f9761e) : glitch par *World Position Offset*, donc il faut des meshes assez denses en vertices.
- [Post Process Volume Materials Bundle](https://fab.com/s/1801889829fd) (gratuit) : contient une aberration chromatique custom.
- [Niagara Examples Pack](https://www.unrealengine.com/en-US/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7) (gratuit, Epic, UE 5.7) : plus de 50 systèmes (étincelles, buffs, traînées…). UEFN ne supporte qu'une partie de Niagara, donc certains effets devront être simplifiés.
- [Voxel Hero Duo Pack](https://forums.unrealengine.com/t/new-asset-pack-released-on-fab-voxel-hero-duo-pack-explore-guima-games/2739269) : personnages voxel animés pour UE5.

### 3.C Outils pour fabriquer tes propres brainrots

| Outil | Usage | Note |
|---|---|---|
| **MagicaVoxel** (gratuit) | Modéliser ou retoucher en voxel (`.vox`) | Workflow UE : export OBJ → Blender → FBX. Si UE signale « missing smoothing groups » : *Mark Sharp* puis export avec *Smoothing: Face*. → [Forum UE](https://forums.unrealengine.com/t/voxel-editor/22002) |
| **Blockbench** (gratuit) | Modèles blocky **et animation** | Exporte FBX (ASCII) compatible Unreal ; Blender n'importe pas le FBX ASCII, passe par glTF dans ce cas. → [Wiki Blockbench](https://www.blockbench.net/wiki/guides/export-formats) |
| **Blender** (gratuit) | Rig, anims, et **voxeliser n'importe quel modèle** (modificateur *Remesh* en mode *Blocks*) | Voxelise **avant** de rigger. Le manuel déconseille le remesh sur un mesh déjà destiné à être déformé. → [BlenderNation](https://www.blendernation.com/2022/12/23/how-to-use-the-remesh-modifier-to-make-voxel-art/) |
| IA texte/image → 3D (Meshy, Tripo, Asset Forge de UEFN Central…) | Prototyper vite une créature, puis la voxeliser dans Blender | Aucune règle Epic trouvée qui interdit l'IA dans les îles, mais tu restes responsable des droits. Lis les conditions de l'outil. → [UEFN terms](https://legal.epicgames.com/epicgames/uefn) |

### 3.D Systèmes / templates (côté gameplay)

- Tutoriel communautaire Epic : [« Steal the Brainrot » stat table en Verse](https://forums.unrealengine.com/t/community-tutorial-how-to-make-a-steal-the-brainrot-stat-table-in-uefn-verse-tutorial/2611064).
- Exemple d'UI (shop, compteur d'argent, rebirth) en UMG + Verse UI : [post d'Eason](https://x.com/itsEasonn/status/1941222632818606544).
- Projet UEFN complet payant (157,50 $, licence restrictive) : [UEFN Academy sur Patreon](https://www.patreon.com/posts/steal-brainrot-144805173). ⚠️ Vérifie qu'il ne contient pas de personnages protégés avant de publier.
- Méfie-toi des templates « steal brainrot » sur Fiverr : beaucoup réutilisent les personnages connus.

### 3.E Modèles des mèmes d'origine (risque 🟠, voir section 2.3)

Packs « Tralalero / Tung Sahur / Bombardiro » sur itch.io ([exemple](https://crtss.itch.io/brainrot-ai-meme-3d-model-pack-tralalero-tralala-bombardiro-crocodiro-tung-sahur)), RenderHub ou Sketchfab. La licence d'un modèle couvre le travail 3D de son auteur, **pas les droits sur le personnage**. Certaines annonces précisent d'ailleurs « usage éditorial uniquement ».

---

## 4. Recettes « glitchy » dans UEFN

UEFN utilise l'éditeur de matériaux d'Unreal, donc les techniques UE classiques s'appliquent. **Limite connue : pas de *Custom node*** (HLSL) dans UEFN. Les post-process matériaux custom ne sont pas confirmés non plus. → [Doc nœuds matériaux UEFN](https://dev.epicgames.com/documentation/fortnite/material-nodes-and-settings-in-unreal-editor-for-fortnite), [forum CustomNode](https://forums.unrealengine.com/t/uefn-customnode/1159025)

### 4.1 Architecture conseillée

```
M_Brainrot_Master           ← un seul matériau maître
 ├─ Params : BaseTint, PaletteTexture, EmissiveColor, EmissiveStrength,
 │           PatternTexture, PatternScale, PanSpeed, FresnelColor, FresnelPower,
 │           HueCycleSpeed, GlitchAmount, SparkleAmount
 ├─ MI_Mut_Normal
 ├─ MI_Mut_Neon
 ├─ MI_Mut_Crystal
 ├─ MI_Mut_Void
 ├─ MI_Mut_Party (arc-en-ciel)
 ├─ MI_Mut_Dreamy
 ├─ MI_Mut_BlackWhite
 └─ MI_Mut_Glitch
```

Astuce voxel : texture **palette** (style MagicaVoxel, ex. 256×1 px). Une mutation peut alors n'être qu'un *swap* de palette, ce qui coûte quasi zéro en mémoire.

### 4.2 Recette par mutation

| Mutation | Recette matériau (nœuds UE) |
|---|---|
| **Neon** | Emissive fort + *scanlines* : texture de lignes dont les UV passent par un `Panner`, multipliée sur la base ; contour `Fresnel` coloré |
| **Crystal** | Couleur claire + `Fresnel` lumineux + normal facettée ; paillettes (voir Sparkle) |
| **Void** | Base quasi noire + `Fresnel` violet + champ d'étoiles qui défile (texture étoiles + `Panner`) |
| **Party / Rainbow** | Hue cycling : `Time` × vitesse + coordonnée UV ou world position, passés dans des sinus déphasés de 0, ⅓ et ⅔ pour R, G et B |
| **Dreamy** | Dégradé pastel vertical (world Z) + motifs lunes/étoiles + glow doux |
| **Black&White** | `Desaturation` à 1 + motif étoiles blanches en emissive |
| **Glitch** | 1) UV décalés par un bruit en escalier (`Floor(Time×N)` dans un noise) ; 2) **split RGB** : 3 lectures de la texture avec petits offsets, une par canal ; 3) jitter par *World Position Offset*. ⚠️ Les meshes voxel ont peu de vertices, préfère les techniques 1 et 2 |
| **Sparkle** (overlay) | Bruit/cellules → `Power` élevé pour ne garder que les points brillants → × pulsation `Time` |

### 4.3 VFX et feedback

- **Niagara** est supporté dans UEFN (sous-ensemble) et utilisable via les devices (VFX Spawner, etc.) → [Doc Niagara UEFN](https://dev.epicgames.com/documentation/fortnite/effects-and-particle-systems-in-unreal-editor-for-fortnite)
  - Une **aura par rareté** (Divine : rayons dorés ; Secret : fumée noire et rouge ; Ascended : anneaux arc-en-ciel)
  - Confettis lors d'un spawn rare, paillettes sur les pads « Collect »
- **Post Process Device** : `BlendIn` / `BlendInForAll` en Verse pour un flash plein écran quand un « Divine » apparaît (source tierce : [UEFN Central](https://uefncentral.com/ar/verse/post-process-device)).
- **Changer de matériau en Verse sur un prop** : je n'ai pas trouvé de doc officielle fiable. L'approche sûre est de préparer **un asset par variante** (mesh + material instance) et de spawner la bonne variante. Vérifie dans la référence API Verse de `creative_prop` avant de coder autrement.

---

## 5. Pipeline d'import dans UEFN

1. **Statique** (brainrot posé sur son piédestal) : FBX importé via le Content Browser. Mêmes règles FBX que dans Unreal standard. → [Doc import UEFN](https://dev.epicgames.com/documentation/en-us/uefn/importing-assets-in-unreal-editor-for-fortnite)
2. **Animé** (idle qui respire ou danse, très efficace pour l'attrait) : UEFN n'a **aucun squelette ni anim préchargés**. Exporte un *skeletal mesh* FBX et coche *Skeletal Mesh* à l'import. → [Doc anims UEFN](https://dev.epicgames.com/documentation/en-us/uefn/import-and-play-mesh-animations-in-unreal-editor-for-fortnite)
   - Blender : une seule armature, un root bone, unités en mètres avec échelle 0.01
   - Anims supplémentaires : importées sur le **même** squelette (même hiérarchie et même nombre d'os)
3. **Textures** en puissances de 2 (sinon faces blanches possibles).
4. Organisation : `Content/Brainrots/<Nom>/` avec `SM_`, `SK_`, `A_`, `MI_`, `NS_`.

---

## 6. Checklist des mécaniques « addictives »

Tirée de tes captures et de conseils de créateurs UEFN. Ce sont des avis de praticiens, pas des règles officielles d'Epic. → [UEFN Central](https://uefncentral.com/pt/blog/uefn-island-monetization-strategies-2026), [StraySpark](https://www.strayspark.studio/blog/uefn-revenue-stream-indie-studios-2026)

- [ ] **Hook immédiat** : cadeau « FREE » et premier brainrot offert dès le spawn
- [ ] **4 à 6 raretés** (Common → Rare → Epic → Legendary → Divine → Secret/Ascended) avec un `$/s` exponentiel
- [ ] **Mutations** avec multiplicateurs (×2, ×3, ×5…), obtenues via une *Mutation Machine* ou pendant les events
- [ ] **Timers « garanti »** (Divine garanti dans X jours) et **spawn global** (« Ascended pour tout le monde dans 2 jours »)
- [ ] **Events tournants** toutes les 30–60 min (thèmes = mutations : Party, Summer, Dreamy, Halloween…)
- [ ] **Rebirth** (reset contre multiplicateur permanent)
- [ ] **Persistance** Verse (`persistable`) + **cash hors-ligne**
- [ ] **Leaderboard** (Rebirths, Cash/s, Steals/Jump) + Wall of Fame
- [ ] **Annonces serveur** « Divine Brainrot Spawned ! » + flash VFX
- [ ] **Nombres géants** formatés avec suffixes (K, M, B, T, Qa, Qi, Sx…)
- [ ] **Codes** (clavier) + **objectif communautaire** (barre de progression)
- [ ] ⚠️ Epic pénalise l'engagement de faible qualité (AFK farming). Le jeu doit demander des actions actives, pas seulement de l'idle

---

## 7. Idées de brainrots originaux (formule objet + animal + nom pseudo-italien)

À vérifier sur le web avant usage, pour être sûr qu'ils n'existent pas déjà :

| Nom | Concept | Rareté suggérée |
|---|---|---|
| Lampadino Pinguino | Pingouin avec une ampoule pour tête, qui clignote (parfait en Neon) | Common |
| Tostapane Tartarugone | Tortue dont la carapace est un grille-pain qui éjecte des toasts | Rare |
| Ventilatore Gufone | Hibou dont les ailes sont des pales de ventilateur qui tournent | Rare |
| Cactusso Lamatino | Lama-cactus qui crache des épines | Epic |
| Lavatricino Polpo | Pieuvre dans une machine à laver, le hublot qui tourne | Epic |
| Gelatino Rinocerone | Rhinocéros en cornet de glace qui fond | Legendary |
| Telefonino Fenicottero | Flamant rose dont le cou est un fil de téléphone | Legendary |
| Ananasso Koalino | Koala-ananas avec couronne de feuilles | Divine |
| Microondino Riccio | Hérisson micro-ondes, piquants en néon | Divine |
| Frigoriferro Elefantone | Éléphant-frigo géant, la porte s'ouvre sur une galaxie (Void) | Secret |

---

## 8. Plan d'action proposé

1. **Direction artistique** : fixer la palette, la taille (gros, lisibles de loin) et le style voxel.
2. **Roster** : 10–15 brainrots originaux (section 7), 5–6 raretés, 6–8 mutations.
3. **Modélisation** : partir de *Kenney Cube Pets* et du *Voxel Creature Pack*, kitbash dans MagicaVoxel/Blockbench, puis Blender pour les idle.
4. **Matériaux** : `M_Brainrot_Master` + material instances de mutations (section 4).
5. **VFX** : auras de rareté + confettis + flash post-process.
6. **Gameplay** : Verse (économie, persistance, rebirth, events), en s'aidant des tutos et source assets Fab (section 3.D).
7. **Test et itération** sur la rétention (retour J+1), puis publication.

---

## Sources

- Go Up For Brainrots / Ferins : [ProGameGuides](https://progameguides.com/codes/fortnite-go-up-for-brainrots-codes/), [Destructoid](https://www.destructoid.com/go-up-for-brainrots-fortnite-codes/), [UEFN Community Awards 2026](https://esports.gg/news/fortnite/uefn-community-awards-2026-results/)
- Steal the Brainrot : [Fortnite.GG](https://fortnite.gg/island/3225-0366-8885), [Wikipedia – Steal a Brainrot](https://en.wikipedia.org/wiki/Steal_a_Brainrot)
- Droits : [Pocket Tactics](https://www.pockettactics.com/fortnite/steal-the-brainrot-lawsuit), [Aftermath](https://aftermath.site/brainrot-roblox-court/), [Gamewave](https://gamewave.fr/roblox/steal-a-brainrot-le-phenomene-roblox-attaque-fortnite-pour-plagiat/), [Law Society Journal](https://lsj.com.au/articles/who-owns-brainrot/), [Island Creator Rules](https://www.epicgames.com/help/en-US/c-Category_CreatorPrograms/c-Trending_0/fortnite-island-creator-rules-a000094823), [IP & DMCA Guidelines](https://www.fortnite.com/news/intellectual-property-ip-and-dmca-guidelines-for-fortnite-island-creators), [UEFN Terms](https://legal.epicgames.com/epicgames/uefn)
- Fab / UEFN : [Fab UI dans UEFN](https://dev.epicgames.com/documentation/fortnite/fab-user-interface-reference-in-unreal-editor-for-fortnite?lang=en-US), [Spotlight Fab](https://www.fortnite.com/news/spotlight-fab-content-added-to-uefn-in-august-2023), [Source assets](https://forums.unrealengine.com/t/uefn-source-assets-are-coming-to-fab-upload-yours-today/2833019), [IA sur Fab](https://80.lv/articles/epic-games-adresses-ai-generated-content-plaguing-fab)
- Assets : [Kenney Cube Pets](https://opengameart.org/node/185352), [Voxel Creature Pack 1](https://opengameart.org/content/voxel-creature-pack1), [Quaternius Animals](https://quaternius.itch.io/lowpoly-animated-animals), [Quaternius Monsters](https://sketchfab.com/3d-models/ultimate-monsters-pack-fd72e114d119488da71fe3a16f216c4f), [Voxel Tiny Animals](https://vox-fox.itch.io/voxel-tiny-animals), [3D Voxel Park](https://mariaisme.itch.io/3d-voxel-park), [Glitch Material Pack](https://www.fab.com/listings/22721291-ad36-43e3-a351-8ee723f9761e), [PP Materials Bundle](https://fab.com/s/1801889829fd), [Niagara Examples Pack](https://www.unrealengine.com/en-US/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7), [Voxel Hero Duo](https://forums.unrealengine.com/t/new-asset-pack-released-on-fab-voxel-hero-duo-pack-explore-guima-games/2739269)
- Outils / pipeline : [Blockbench export](https://www.blockbench.net/wiki/guides/export-formats), [Blender Remesh voxel](https://www.blendernation.com/2022/12/23/how-to-use-the-remesh-modifier-to-make-voxel-art/), [MagicaVoxel → UE](https://forums.unrealengine.com/t/voxel-editor/22002), [Import UEFN](https://dev.epicgames.com/documentation/en-us/uefn/importing-assets-in-unreal-editor-for-fortnite), [Anims UEFN](https://dev.epicgames.com/documentation/en-us/uefn/import-and-play-mesh-animations-in-unreal-editor-for-fortnite)
- Matériaux / VFX : [Nœuds matériaux UEFN](https://dev.epicgames.com/documentation/fortnite/material-nodes-and-settings-in-unreal-editor-for-fortnite), [Niagara UEFN](https://dev.epicgames.com/documentation/fortnite/effects-and-particle-systems-in-unreal-editor-for-fortnite), [Forum CustomNode](https://forums.unrealengine.com/t/uefn-customnode/1159025), [Post Process Device (tiers)](https://uefncentral.com/ar/verse/post-process-device)
- Gameplay / rétention : [Tuto stat table](https://forums.unrealengine.com/t/community-tutorial-how-to-make-a-steal-the-brainrot-stat-table-in-uefn-verse-tutorial/2611064), [UI Eason](https://x.com/itsEasonn/status/1941222632818606544), [Patreon UEFN Academy](https://www.patreon.com/posts/steal-brainrot-144805173), [UEFN Central – monétisation](https://uefncentral.com/pt/blog/uefn-island-monetization-strategies-2026), [StraySpark](https://www.strayspark.studio/blog/uefn-revenue-stream-indie-studios-2026)
