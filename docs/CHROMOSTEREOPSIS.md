# Chromostereopsis Specification — GameMaster

## Purpose

GameMaster uses chromostereopsis as a brand language, not as an anaglyph filter, RGB-split effect or retro 3D-glasses gimmick. The goal is a site that can feel spatial through color while remaining readable, comfortable and commercially credible.

This document translates the owner's research into an **artistic-depth implementation** for a public website. It does not claim laboratory-level reproducibility or identical depth perception for every observer.

## First principle: one image, one geometry

Chromostereopsis is not produced by making two displaced copies of the same object. A traditional anaglyph uses two offset image channels intended to be separated by colored filters. The chromostereoscopic phenomenon discussed in the supplied research can occur in a single 2D composition because red and blue regions are processed differently by the binocular visual system.

Therefore GameMaster must preserve a **single-geometry invariant**:

- one heading shape, not red/blue copies of the same heading;
- one button body, not two offset button shells;
- one logo, not red/blue ghost logos;
- one card body, not chromatically duplicated outlines;
- one visual object per semantic object.

Color depth comes from the relationship between **different red, blue and neutral regions**, not cloned contours.

## What the research supports strongly enough for art direction

The supplied research repeatedly treats chromostereopsis as:

- binocular;
- strongly associated with large spectral separation, especially red vs blue;
- sensitive to luminance and adaptation;
- affected by pupil position and observer-specific ocular optics;
- dependent on display characteristics;
- variable across observers, including possible inversion or weak/no effect;
- easier to isolate when chromatic regions are crisp and not muddied by gradients or color mixing.

Operational consequences for the website:

- use strongly separated red and blue regions;
- keep boundaries crisp where the effect matters;
- keep substantial black/neutral negative space;
- avoid mixing red and blue into purple in the primary depth cues;
- avoid blur and soft glow on the main chromatic structures;
- never rely on the illusion as the only communication channel;
- expect some users to perceive a different depth direction.

## Important nuance from the research set

The research documents are not uniform on every secondary parameter. Earlier material strongly favors a black background, high saturation and hard contrast. Later auditing is more cautious and treats absolute claims such as “black is always optimal”, “maximum saturation always maximizes depth” and exact spatial-frequency rules as insufficiently demonstrated.

Therefore GameMaster uses a dark brand base and vivid red/blue as a practical starting system, not as a claim of universal optical optimality.

## GameMaster implementation profile

### Palette

Use CSS variables so the exact values can be tuned globally.

Initial digital palette:

- `--gm-black: #050505`
- `--gm-surface: #0b0b0d`
- `--gm-red: #ff1a1a`
- `--gm-blue: #1616ff`
- `--gm-white: #f4f4ef`
- `--gm-muted: #a6a6ad`

These are implementation values, not scientific claims that a specific hex pair is physically optimal. Actual output depends on gamut, spectral power distribution, luminance, calibration and viewing conditions.

### Three-plane grammar

Use three conceptual planes:

1. **Front/focal plane — red**
   - primary focal motifs;
   - selected accents;
   - price/CTA emphasis when appropriate;
   - sparse foreground bars, symbols or masses.

2. **Neutral plane — black / near-black / off-white**
   - body copy;
   - card surfaces;
   - reading areas;
   - spacing and visual rest.

3. **Rear/structural plane — blue**
   - grids;
   - topographic lines;
   - circuit/network structures;
   - modular patterns;
   - secondary spatial fields.

These planes must be **different shapes or regions with different compositional roles**. Do not make red and blue copies of the same plane.

## Forbidden implementation patterns

Do not use the following to represent chromostereopsis:

```css
/* anaglyph-like: forbidden */
.title {
  text-shadow: -2px 0 red, 2px 0 blue;
}
```

```css
/* anaglyph-like: forbidden */
.card {
  box-shadow: -3px 0 red, 3px 0 blue;
}
```

Also forbidden:

- duplicate DOM elements offset in red/blue;
- pseudo-elements cloning the same shape in opposing colors;
- red/cyan ghost contours;
- RGB channel splitting;
- chromatic-aberration filters;
- blur halos as the main depth cue;
- repeated left/right copies of logos, typography, posters or icons.

These mechanisms visually read as anaglyph/glitch rather than the intended chromostereoscopic design system.

## Preferred chromatic relationships

### Figure vs structural field

A red independent foreground object can sit against a blue structural field on black. The red and blue areas are different geometry.

### Alternating regions

Use bars, cells, tessellations, glyphs or panels where red and blue occupy different adjacent regions. Crisp boundaries are useful.

### Sparse focal red

Several supplied references demonstrate that a small red foreground element can dominate against a larger blue field. GameMaster should not assume red and blue need equal area.

### Blue rear system + red editorial mass

Technical diagrams, grids, topographic contours and repeated glyphs work well as blue rear structures, while red is reserved for one focal figurative or abstract mass.

### Posterized / halftone segmentation

Figurative artwork may use red/black or blue/black posterization, with the other chromatic plane introduced as a separate pattern, frame or object. Avoid red and blue tracing the exact same silhouette at offsets.

## Typography

Primary body copy remains neutral for legibility.

Large typography may use:

- one red word against neutral text;
- one blue word as a rear label;
- a red bar crossing a neutral title;
- a separate blue geometric field near the title;
- different colored typographic modules with different content.

Do **not** use duplicated red/blue text shadows or pseudo-element copies to fake depth.

### Text colour on chromatic fields (hard rule)

**Nunca texto rojo sobre azul; el texto rojo siempre va sobre negro.** Never set red text on a blue field. Red text (`--gm-red`) is only allowed on black/near-black (`--gm-black` / `--gm-ink`). Red-on-blue text vibrates at the colour boundary and is hard to read.

Text on electric blue (`--gm-blue`, #2438ff):

- small text (body copy, labels, buttons, metadata — anything under 24px, or under 18.66px bold) uses off-white (`--gm-white`), about 6:1;
- black text on #2438ff is only about 3.1:1, so black is reserved for large display titles;
- if a small label needs a darker look, place it on `--gm-blue-deep` with off-white text, or on a black plate.

When a decorative blue band can pass behind small text (rails, step lists, card bodies), give that text block a solid black background so the rule holds at every width.

## Cards

Cards should feel layered through composition, not ghosting.

Recommended structure:

- one black/near-black card body;
- one independent blue rear motif inside or behind a defined region;
- one independent red foreground marker, strip or focal graphic;
- cover art/procedural art occupying a real region;
- strong focus/hover behavior without chromatic duplication.

Do not place a red clone and blue clone of the entire card shell behind the neutral card.

## Background visual languages

Allowed and encouraged when kept controlled:

- sparse grids;
- circuit/network lines;
- topographic contours;
- modular diagrams;
- halftone fields;
- tessellations;
- flow fields;
- technical/vector motifs;
- posterized engraving-inspired imagery.

These directions match the owner's research and supplied references better than a generic RGB glitch texture.

## Motion

Motion can reinforce independent planes through small translations or parallax, but it must never turn them into a stereo pair of duplicated objects.

Recommended:

- independent blue background structure moves slightly slower than red focal art;
- cards translate 2–4px as a whole on hover;
- red foreground marker may move independently from a blue background motif if they are different shapes;
- rails use normal inertial scrolling.

Forbidden:

- oscillating red/blue ghost copies;
- animated channel splitting;
- continuous chromatic jitter.

Always support `prefers-reduced-motion: reduce`.

## Comfort guardrails

The research notes possible visual fatigue from intense red/blue combinations and dense repetitive structures.

Therefore:

- reserve the strongest chromatic composition for hero, selected feature art and section transitions;
- keep reading surfaces mostly neutral;
- avoid high-density chromatic vibration behind text;
- use substantial black/neutral space;
- do not animate saturated patterns continuously;
- simplify art and reduce density on mobile.

## Responsive rules

### Desktop

- richer three-plane composition;
- larger fields of independent red and blue art;
- more visible structural backgrounds;
- several discovery rails visible at once.

### Mobile

- fewer simultaneous chromatic structures;
- larger simple color masses instead of thin doubled edges;
- simplified background ornament;
- full-width readability;
- no horizontal viewport overflow;
- no desktop composition merely scaled down.

## Reference-derived artistic directions

The supplied references repeatedly show combinations such as:

- red engraved/halftone figure + blue repeating geometric background;
- blue technical portrait + a single red foreground bar;
- red architectural/ornamental frame + blue/black inner scene;
- blue figurative field + one sparse red focal object;
- large black negative areas separating the chromatic planes.

These are excellent GameMaster directions because each color occupies a **different visual role**.

## What Codex should experiment with next

Test distinct modules rather than mixing everything at once:

1. topographic rear field + red focal mass;
2. technical/circuit blue system + red product marker;
3. modular tessellation with genuinely alternating cells;
4. halftone/engraving foreground + independent geometric background;
5. flow-field rear structure + sparse red foreground elements;
6. abstract typographic symbols using separate red/blue modules.

For each experiment evaluate:

- perceived depth;
- whether any element looks duplicated;
- readability;
- brand distinctiveness;
- fatigue after 30–60 seconds;
- mobile performance;
- whether the design still looks coherent in grayscale.

## Scientific humility

Never present the website as scientifically guaranteed to create identical depth for every viewer. The source research explicitly notes individual differences, possible inversion and display-dependent results.

The product goal is a **controlled chromostereoscopic art direction**, not an optical claim.

## 5ª pasada: parallax real, cortes y arte vectorial (Claude)

- Fondo fijo (`components/art/Backdrop.tsx`): azul suave sobre negro, casi inmóvil; las piezas rojas viajan más que el contenido (variables `--gm-depth-*`).
- Cada sección tiene su propia placa con corte diagonal (`clip-path`) y se solapa con la anterior.
- Objetos rojos y láminas en SVG (`components/art/VectorArt.tsx`); logos en PNG sin fondo en `public/brand/logos/`.
- Colores grandes suaves (`--gm-blue` #3447aa); rojo vivo solo en piezas y botones; texto sobre azul siempre blanco; el acento rojo de títulos va en placa negra.
- Con `prefers-reduced-motion` no hay parallax ni deriva del fondo.
