# 30 brainrots originaux pour ta map UEFN

![Les 30 brainrots](previews/roster_sheet.jpg)

Trente personnages créés pour ta map, dans le style voxel des jeux « brainrot ». La formule est la même : **objet du quotidien + animal + nom pseudo-italien**. Aucun ne reprend un personnage existant (Tung Tung, Tralalero, Strawberry Elephant…). Fais quand même une recherche rapide sur les noms avant de publier, l'univers brainrot est immense.

Chaque modèle est livré en :

| Fichier | Usage |
|---|---|
| `models/NN_nom/nom.fbx` | **À importer dans UEFN** (mesh statique, textures intégrées) |
| `models/NN_nom/nom.glb` | Aperçu rapide (Windows 3D Viewer, Blender, sites web) |
| `models/NN_nom/nom.vox` | Modifiable dans **MagicaVoxel** (gratuit) |
| `models/NN_nom/preview.png` | Rendu fond transparent (miniatures, UI, réseaux) |
| `previews/cards/NN_nom.jpg` | Carte « style jeu » (rareté, nom, revenu) |

Tous les modèles partagent **une seule palette** (`textures/`). Il suffit donc d'un seul matériau pour les 30, et une mutation se résume à changer de palette.

---

## Le roster

<!-- ROSTER_TABLE -->
<!-- /ROSTER_TABLE -->

Les revenus sont des suggestions d'équilibrage (environ ×1,5 entre deux brainrots, avec un saut à chaque rareté). Adapte-les à ton économie.

---

## Importer dans UEFN (pas à pas)

### 1. Les textures (une seule fois)

1. Dans le Content Browser, crée un dossier `Brainrots/Textures`.
2. Glisse dedans `textures/T_Brainrot_BaseColor.png`, `T_Brainrot_ORM.png` et `T_Brainrot_Emissive.png`.
3. Ouvre chaque texture et règle :
   - **Filter** : `Nearest` (sinon les couleurs bavent entre les voxels)
   - **Mip Gen Settings** : `NoMipmaps`
   - Pour `T_Brainrot_ORM` uniquement : **Compression Settings** = `Masks` et **sRGB** décoché

### 2. Le matériau maître `M_Brainrot`

Crée un matériau `M_Brainrot` avec ce graphe :

```
TextureSampleParameter2D "Palette"   (T_Brainrot_BaseColor) ── RGB ──► Base Color
TextureSampleParameter2D "ORM"       (T_Brainrot_ORM)       ── G ────► Roughness
                                                             └─ B ────► Metallic
TextureSampleParameter2D "Emissive"  (T_Brainrot_Emissive)  ── RGB ─┐
ScalarParameter "EmissiveStrength" (défaut 4) ──────────────── × ───┴──► Emissive Color
```

Toutes les UV d'un même voxel pointent au centre d'un seul pixel de la palette. Il n'y a donc **aucun dépliage UV** à faire.

### 3. Les modèles

1. Crée `Brainrots/Meshes` et glisse les 30 fichiers `.fbx` (sélection multiple possible).
2. Dans la fenêtre d'import :
   - **Skeletal Mesh** : décoché (ce sont des meshes statiques)
   - **Generate Missing Collision** : coché
   - **Material Import Method** : `Do Not Create Material`. Ensuite, assigne `M_Brainrot` à chaque mesh. Tu peux aussi laisser UEFN créer les matériaux, mais tu en auras 30 copies identiques.
3. **Pivot** : au sol, au centre du personnage, ce qui le pose directement sur un piédestal.
4. **Échelle** : 1 voxel = 7,5 cm. Les tailles vont de 2 m (communs) à 7 m (Secret), comme dans les jeux où les rares sont plus gros.
5. **Orientation** : dans Blender, chaque brainrot regarde vers −Y. Si l'un d'eux est de dos ou de profil dans UEFN, fais-lui une rotation de 90° ou 180° en Z.

### 4. Les mutations

Dans `textures/mutations/` il y a 7 palettes prêtes : **Gold, Diamond, Void, Lava, Neon, Candy, BlackWhite**.

![Mutations](previews/mutations_14_jukeboxino_pappagallo.jpg)

Pour chacune :

1. Clic droit sur `M_Brainrot` → *Create Material Instance* → `MI_Brainrot_Gold`.
2. Remplace les paramètres `Palette`, `ORM` et `Emissive` par les trois textures `_Gold`.
3. Applique l'instance sur le mesh. Si tu veux changer de mutation pendant la partie, prépare un prop par variante et fais apparaître la bonne.

Pour les mutations animées (arc-en-ciel *Party*, *Glitch*), voir la section 4 de `RECHERCHE_ASSETS_BRAINROT.md` à la racine du repo.

### 5. Donner vie aux brainrots

- **Flottement** : un petit va-et-vient vertical (prop mover ou `MoveTo` en Verse) et une rotation lente sur le piédestal suffisent à les rendre vivants.
- **Aura de rareté** : un système Niagara par rareté (étincelles dorées pour Divine, pixels magenta/cyan pour Secret).
- **Annonce** : bannière « Divine Brainrot Spawned ! » et flash post-process quand un Divine ou un Secret apparaît.

### Performances

Entre 2 500 et 15 000 triangles par modèle grâce au *greedy meshing* (fusion des faces de même couleur). La palette ne pèse que 32 × 32 pixels.

---

## Modifier ou en créer d'autres

Les modèles sont générés par du code, ce qui les rend faciles à retoucher :

```bash
pip install bpy numpy pillow        # bpy = Blender en module Python
cd brainrots/generator
python3 build.py                    # régénère les 30 (.vox, .glb, .fbx, rendus)
python3 build.py --only 7,12        # seulement certains modèles
python3 build.py --no-render        # sans rendus (rapide)
python3 cards.py --mutations 14     # cartes + planche + démo des mutations
```

- Chaque brainrot est une fonction dans `generator/roster.py`. Couleurs, tailles et accessoires se changent en quelques lignes.
- `generator/vox.py` est le moteur voxel : sphères, cylindres, tubes, peinture, décalques.
- Tu peux aussi ouvrir n'importe quel `.vox` dans MagicaVoxel pour le retoucher à la main.

La police des cartes, *Lilita One*, est sous licence SIL Open Font License (`generator/fonts/OFL.txt`). Elle ne sert qu'aux images d'aperçu.
