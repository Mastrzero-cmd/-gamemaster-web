export const genreOrder = [
  'Acción',
  'Aventura',
  'RPG/JRPG',
  'Shooter',
  'Plataformas',
  'Estrategia y táctica',
  'Pelea',
  'Carreras',
  'Deportes',
  'Fiesta',
  'Terror y supervivencia',
  'Puzzle',
  'Simulación',
  'Ritmo',
  'Sigilo',
  'Roguelike',
] as const;

export const worldOrder = [
  'Mario',
  'Zelda',
  'Pokémon',
  'Metroid',
  'Minecraft',
  'Resident Evil',
  'Fire Emblem',
  'Xenoblade Chronicles',
  'Nintendo',
  'Donkey Kong',
  'Kirby',
  'Pikmin',
  'Sonic',
  'Dragon Ball',
  'Diablo',
  'Bayonetta',
  'Ori',
  'Little Nightmares',
  'SteamWorld',
  'BioShock',
  'Borderlands',
  'DOOM',
  'Plants vs. Zombies',
  'Splatoon',
  'Rabbids',
  'Shovel Knight',
  'Super Smash Bros.',
  'WarioWare',
  'Yoshi',
  'Advance Wars',
  'Animal Crossing',
  'Crash Bandicoot',
  'Metal Gear',
  'Monster Hunter',
  'Mortal Kombat',
  'Ninja Gaiden',
  'Portal',
  'The Elder Scrolls',
] as const;

export const collectionOrder = [
  'Destacados GameMaster',
  'Nintendo Switch 2',
  'Indies esenciales',
  'Familiar',
  'Multijugador',
  'Cooperativo',
  'Mundo abierto',
  'Sandbox y creatividad',
  'Clásicos, colecciones y remasters',
  'Aventuras largas',
  'Difíciles y desafiantes',
] as const;

export const featureOrder = [
  'Exploración',
  'Multijugador',
  'Cooperativo',
  'Familiar',
  'Mundo abierto',
  'Sandbox',
  'Colección',
  'Remaster',
  'Remake',
  'Aventura larga',
  'Desafiante',
] as const;

export type Genre = (typeof genreOrder)[number];
export type World = (typeof worldOrder)[number];
export type Collection = (typeof collectionOrder)[number];
export type GameFeature = (typeof featureOrder)[number];
export type TaxonomyConfidence = 'alta' | 'media' | 'baja';

export type GameTaxonomySeed = {
  genres: Genre[];
  worlds?: World[];
  collections?: Collection[];
  features?: GameFeature[];
  featured?: boolean;
  confidence?: TaxonomyConfidence;
  reviewNote?: string;
  manualReview?: boolean;
};

// Taxonomía editorial explícita por ID. Nunca deriva géneros de sourceCategory.
export const gameTaxonomy: Record<string, GameTaxonomySeed> = {
  'castlestorm-ii': { genres: ['Acción', 'Estrategia y táctica'], confidence: 'media', reviewNote: 'Híbrido de combate lateral y defensa de torres; conviene validar qué faceta priorizar.', manualReview: true },
  'hellblade-senua-s-sacrifice': { genres: ['Acción', 'Aventura', 'Puzzle'], features: ['Exploración'] },
  'hotline-miami': { genres: ['Acción', 'Shooter'], collections: ['Indies esenciales'], features: ['Colección', 'Desafiante'] },
  'john-wick-hex': { genres: ['Acción', 'Estrategia y táctica'] },
  'katana-zero': { genres: ['Acción', 'Plataformas'], collections: ['Indies esenciales'], features: ['Desafiante'] },
  'little-nightmares': { genres: ['Aventura', 'Plataformas', 'Terror y supervivencia', 'Puzzle'], worlds: ['Little Nightmares'], features: ['Exploración'] },
  'little-nightmares-2': { genres: ['Aventura', 'Plataformas', 'Terror y supervivencia', 'Puzzle'], worlds: ['Little Nightmares'], features: ['Exploración'] },
  'my-friend-pedro': { genres: ['Acción', 'Shooter', 'Plataformas'], collections: ['Indies esenciales'], features: ['Desafiante'] },
  'ori-blind-forest': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Ori'], collections: ['Indies esenciales'], features: ['Exploración', 'Desafiante'] },
  'ori-wisps': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Ori'], collections: ['Indies esenciales'], features: ['Exploración', 'Desafiante'] },
  'shovel-knight-treasure-trove-con-expansion': { genres: ['Acción', 'Plataformas'], worlds: ['Shovel Knight'], collections: ['Indies esenciales'], features: ['Colección', 'Desafiante'] },
  'steamworld-dig-2': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['SteamWorld'], collections: ['Indies esenciales'], features: ['Exploración'] },
  'steamworld-heist': { genres: ['Estrategia y táctica'], worlds: ['SteamWorld'], collections: ['Indies esenciales'] },
  'void-bastards': { genres: ['Shooter', 'Estrategia y táctica', 'Roguelike'], collections: ['Indies esenciales'], features: ['Desafiante'], confidence: 'media', reviewNote: 'Combina shooter, gestión de recursos y estructura roguelike.' },
  bioshock: { genres: ['Acción', 'Aventura', 'Shooter'], worlds: ['BioShock'], features: ['Colección'] },
  borderlands: { genres: ['Acción', 'RPG/JRPG', 'Shooter'], worlds: ['Borderlands'], features: ['Colección', 'Multijugador', 'Cooperativo', 'Aventura larga'] },
  crysis: { genres: ['Acción', 'Shooter', 'Sigilo'], features: ['Remaster'] },
  'doom-2016': { genres: ['Acción', 'Shooter'], worlds: ['DOOM'], features: ['Desafiante'] },
  'dying-light-platinum-edition': { genres: ['Acción', 'Aventura', 'Terror y supervivencia'], features: ['Mundo abierto', 'Multijugador', 'Cooperativo', 'Aventura larga'] },
  'metroid-prime-remastered': { genres: ['Acción', 'Aventura', 'Shooter', 'Puzzle'], worlds: ['Metroid', 'Nintendo'], features: ['Exploración', 'Remaster'] },
  'plants-vs-zombies-battle-for-neighborville': { genres: ['Acción', 'Shooter'], worlds: ['Plants vs. Zombies'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'resident-evil-revelations-2': { genres: ['Acción', 'Shooter', 'Terror y supervivencia'], worlds: ['Resident Evil'], features: ['Cooperativo'] },
  'splatoon-3': { genres: ['Acción', 'Shooter'], worlds: ['Splatoon', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'wolfenstein-youngblood': { genres: ['Acción', 'Shooter'], features: ['Multijugador', 'Cooperativo'] },
  'xcom-2-collection': { genres: ['Estrategia y táctica'], features: ['Colección', 'Aventura larga', 'Desafiante'] },
  'donkey-kong-bananza': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Donkey Kong', 'Mario', 'Nintendo'], features: ['Exploración', 'Familiar'], featured: true },
  'mario-kart-world': { genres: ['Carreras', 'Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'], featured: true },
  'metroid-prime-4': { genres: ['Acción', 'Aventura', 'Shooter'], worlds: ['Metroid', 'Nintendo'], features: ['Exploración'], featured: true },
  'pokemon-pokopia': { genres: ['Aventura', 'Simulación'], worlds: ['Pokémon', 'Nintendo'], features: ['Sandbox', 'Familiar'], confidence: 'baja', reviewNote: 'La clasificación se basa en la propuesta pública del título y debe revisarse al consolidarse su ficha final.', manualReview: true },
  'resident-evil-9-requiem-8-7': { genres: ['Acción', 'Shooter', 'Terror y supervivencia'], worlds: ['Resident Evil'] },
  celeste: { genres: ['Acción', 'Plataformas'], collections: ['Indies esenciales'], features: ['Desafiante'], featured: true },
  'hollow-knight': { genres: ['Acción', 'Aventura', 'Plataformas'], collections: ['Indies esenciales'], features: ['Exploración', 'Desafiante'], featured: true },
  membrane: { genres: ['Plataformas', 'Puzzle'], collections: ['Indies esenciales'], confidence: 'media', reviewNote: 'Puzzle-plataformas experimental; revisar si se desea añadir Acción.' },
  'pixeljunk-monsters-2': { genres: ['Estrategia y táctica'], collections: ['Indies esenciales'], features: ['Cooperativo', 'Familiar'], confidence: 'media', reviewNote: 'Tower defense con cooperativo; Estrategia es la clasificación principal.' },
  'captain-toad': { genres: ['Aventura', 'Plataformas', 'Puzzle'], worlds: ['Mario', 'Nintendo'], features: ['Exploración', 'Familiar'] },
  'luigi-mansion-3': { genres: ['Acción', 'Aventura', 'Puzzle'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Cooperativo', 'Familiar', 'Exploración'] },
  'mario-and-sonic-at-the-olympic-games-tokyo-2020': { genres: ['Deportes', 'Fiesta'], worlds: ['Mario', 'Sonic', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'mario-rabbids': { genres: ['RPG/JRPG', 'Estrategia y táctica'], worlds: ['Mario', 'Rabbids', 'Nintendo'], features: ['Familiar', 'Aventura larga'] },
  'mario-kart-8': { genres: ['Carreras', 'Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'mario-party-jamboree': { genres: ['Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'mario-party-superstars': { genres: ['Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'mario-strikers': { genres: ['Deportes', 'Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'new-mario-u': { genres: ['Acción', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'mario-origami': { genres: ['Aventura', 'RPG/JRPG', 'Puzzle'], worlds: ['Mario', 'Nintendo'], features: ['Familiar', 'Aventura larga'] },
  'super-mario-3d-all-stars-coleccion-3-en-1': { genres: ['Aventura', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Colección', 'Familiar'] },
  'mario-3d-world': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'mario-wonder': { genres: ['Acción', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Cooperativo', 'Familiar'], featured: true },
  'super-mario-galaxy-2': { genres: ['Aventura', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Exploración', 'Familiar'] },
  'mario-maker-2': { genres: ['Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Sandbox', 'Multijugador', 'Familiar'] },
  'mario-odyssey': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Mario', 'Nintendo'], features: ['Exploración', 'Familiar'], featured: true },
  'super-mario-party': { genres: ['Fiesta'], worlds: ['Mario', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'mario-rpg': { genres: ['Aventura', 'RPG/JRPG'], worlds: ['Mario', 'Nintendo'], features: ['Remake', 'Familiar'] },
  'super-smash-bros-ultimate': { genres: ['Pelea', 'Fiesta'], worlds: ['Super Smash Bros.', 'Nintendo'], features: ['Multijugador', 'Familiar'] },
  'warioware-get-it-together': { genres: ['Fiesta'], worlds: ['WarioWare', 'Mario', 'Nintendo'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'yoshi-s-crafted-world': { genres: ['Aventura', 'Plataformas'], worlds: ['Yoshi', 'Mario', 'Nintendo'], features: ['Cooperativo', 'Familiar'] },
  'advance-wars-1-2-re-boot-camp': { genres: ['Estrategia y táctica'], worlds: ['Advance Wars', 'Nintendo'], features: ['Colección', 'Remake', 'Multijugador', 'Desafiante'] },
  'animal-crossing-new-horizons': { genres: ['Aventura', 'Simulación'], worlds: ['Animal Crossing', 'Nintendo'], features: ['Sandbox', 'Multijugador', 'Familiar'], featured: true },
  'batman-arkham-trilogy': { genres: ['Acción', 'Aventura', 'Sigilo'], features: ['Colección', 'Mundo abierto', 'Aventura larga'] },
  bayonetta: { genres: ['Acción', 'Aventura'], worlds: ['Bayonetta'], features: ['Desafiante'] },
  'bayonetta-3': { genres: ['Acción', 'Aventura'], worlds: ['Bayonetta'], features: ['Desafiante'] },
  cuphead: { genres: ['Acción', 'Shooter', 'Plataformas'], collections: ['Indies esenciales'], features: ['Cooperativo', 'Desafiante'] },
  'dragon-ball-fighterz-fighterz-edition': { genres: ['Pelea'], worlds: ['Dragon Ball'], features: ['Multijugador'] },
  'fall-guys': { genres: ['Fiesta', 'Plataformas'], features: ['Multijugador', 'Familiar'], confidence: 'media', reviewNote: 'Fiesta competitiva con obstáculos de plataformas; ambas facetas son relevantes.' },
  'fifa-20': { genres: ['Deportes'], features: ['Multijugador', 'Familiar'] },
  'fifa-21': { genres: ['Deportes'], features: ['Multijugador', 'Familiar'] },
  'grand-theft-auto-the-trilogy-the-definitive-edition': { genres: ['Acción', 'Aventura', 'Shooter'], features: ['Colección', 'Mundo abierto', 'Aventura larga'] },
  hades: { genres: ['Acción', 'RPG/JRPG', 'Roguelike'], collections: ['Indies esenciales'], features: ['Desafiante'], featured: true },
  'jump-force-deluxe-edition': { genres: ['Pelea'], features: ['Multijugador'] },
  'just-dance-2021': { genres: ['Fiesta', 'Ritmo'], features: ['Multijugador', 'Familiar'] },
  'kimetsu-no-yaiba-demon-slayer-the-hinokami-chronicles': { genres: ['Acción', 'Aventura', 'Pelea'], features: ['Multijugador'] },
  'kirby-and-the-forgotten-land': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Kirby', 'Nintendo'], features: ['Cooperativo', 'Familiar', 'Exploración'] },
  'metal-gear-solid-master-collection-vol-1': { genres: ['Acción', 'Aventura', 'Sigilo'], worlds: ['Metal Gear'], features: ['Colección', 'Aventura larga'] },
  'metroid-dread': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Metroid', 'Nintendo'], features: ['Exploración', 'Desafiante'], featured: true },
  minecraft: { genres: ['Aventura'], worlds: ['Minecraft'], features: ['Sandbox', 'Multijugador', 'Cooperativo', 'Familiar'], featured: true },
  'minecraft-dungeons': { genres: ['Acción', 'RPG/JRPG'], worlds: ['Minecraft'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'minecraft-legends': { genres: ['Acción', 'Estrategia y táctica'], worlds: ['Minecraft'], features: ['Multijugador', 'Cooperativo', 'Familiar'] },
  'mortal-kombat-11': { genres: ['Pelea'], worlds: ['Mortal Kombat'], features: ['Multijugador'] },
  'naruto-shippuden-ultimate-ninja-storm-4-road-to-boruto': { genres: ['Acción', 'Pelea'], features: ['Multijugador'] },
  'switch-sports': { genres: ['Deportes', 'Fiesta'], worlds: ['Nintendo'], features: ['Multijugador', 'Familiar'] },
  'pikmin-1-2': { genres: ['Aventura', 'Estrategia y táctica', 'Puzzle'], worlds: ['Pikmin', 'Nintendo'], features: ['Colección', 'Exploración', 'Familiar'] },
  'pikmin-3-deluxe': { genres: ['Aventura', 'Estrategia y táctica', 'Puzzle'], worlds: ['Pikmin', 'Nintendo'], features: ['Cooperativo', 'Exploración', 'Familiar'] },
  'pikmin-4': { genres: ['Aventura', 'Estrategia y táctica', 'Puzzle'], worlds: ['Pikmin', 'Nintendo'], features: ['Exploración', 'Familiar'] },
  portal: { genres: ['Aventura', 'Puzzle'], worlds: ['Portal'], features: ['Colección', 'Cooperativo', 'Desafiante'] },
  'red-dead': { genres: ['Acción', 'Aventura', 'Shooter'], features: ['Mundo abierto', 'Aventura larga'] },
  'civilization-vi': { genres: ['Estrategia y táctica', 'Simulación'], features: ['Aventura larga', 'Desafiante'] },
  'pokemon-detective': { genres: ['Aventura', 'Puzzle'], worlds: ['Pokémon', 'Nintendo'], features: ['Familiar'] },
  'pokemon-snap': { genres: ['Aventura'], worlds: ['Pokémon', 'Nintendo'], features: ['Exploración', 'Familiar'], confidence: 'media', reviewNote: 'Aventura fotográfica sobre raíles; se evita forzarla dentro de Shooter o Puzzle.' },
  'pokemon-diamante-brillante': { genres: ['Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Remake', 'Familiar', 'Aventura larga'] },
  'pokemon-arceus': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Exploración', 'Familiar', 'Aventura larga'], featured: true },
  'pokemon-za': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Exploración', 'Familiar'], featured: true },
  'pokemon-mystery': { genres: ['RPG/JRPG', 'Roguelike'], worlds: ['Pokémon', 'Nintendo'], features: ['Remake', 'Familiar', 'Desafiante'] },
  'pokemon-perla-reluciente': { genres: ['Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Remake', 'Familiar', 'Aventura larga'] },
  'pokemon-scarlet': { genres: ['Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Mundo abierto', 'Multijugador', 'Familiar', 'Aventura larga'] },
  'pokemon-violet': { genres: ['Aventura', 'RPG/JRPG'], worlds: ['Pokémon', 'Nintendo'], features: ['Mundo abierto', 'Multijugador', 'Familiar', 'Aventura larga'] },
  'assassin-s-creed-the-rebel-collection': { genres: ['Acción', 'Aventura', 'Sigilo'], features: ['Colección', 'Mundo abierto', 'Aventura larga'] },
  'bravely-default-ii': { genres: ['Aventura', 'RPG/JRPG'], features: ['Aventura larga'] },
  'crash-bandicoot-4-it-s-about-time': { genres: ['Acción', 'Plataformas'], worlds: ['Crash Bandicoot'], features: ['Familiar', 'Desafiante'] },
  'crash-bandicoot-n-sane-trilogy': { genres: ['Acción', 'Plataformas'], worlds: ['Crash Bandicoot'], features: ['Colección', 'Remaster', 'Familiar', 'Desafiante'] },
  'diablo-ii-resurrected': { genres: ['Acción', 'RPG/JRPG'], worlds: ['Diablo'], features: ['Remaster', 'Multijugador', 'Cooperativo', 'Aventura larga'] },
  'diablo-3': { genres: ['Acción', 'RPG/JRPG'], worlds: ['Diablo'], features: ['Multijugador', 'Cooperativo', 'Aventura larga'] },
  'divinity-2': { genres: ['RPG/JRPG', 'Estrategia y táctica'], features: ['Multijugador', 'Cooperativo', 'Aventura larga', 'Desafiante'] },
  'dragon-ball-z-kakarot-a-new-power-awakens-set': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Dragon Ball'], features: ['Aventura larga'], confidence: 'media', reviewNote: 'Usa zonas abiertas conectadas; no se marca como mundo abierto para evitar una afirmación excesiva.' },
  'dragon-quest-xi-s-echoes-of-an-elusive-age-definitive-edition': { genres: ['Aventura', 'RPG/JRPG'], features: ['Aventura larga'] },
  'fire-emblem-engage': { genres: ['RPG/JRPG', 'Estrategia y táctica'], worlds: ['Fire Emblem', 'Nintendo'], features: ['Aventura larga', 'Desafiante'] },
  'fire-emblem': { genres: ['RPG/JRPG', 'Estrategia y táctica'], worlds: ['Fire Emblem', 'Nintendo'], features: ['Aventura larga', 'Desafiante'] },
  'hogwarts-legacy': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'] },
  'immortals-fenyx-rising': { genres: ['Acción', 'Aventura', 'Puzzle'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'] },
  'marvel-ultimate-alliance-3-the-black-order': { genres: ['Acción', 'RPG/JRPG'], worlds: ['Nintendo'], features: ['Multijugador', 'Cooperativo'] },
  'monster-hunter-rise': { genres: ['Acción', 'RPG/JRPG'], worlds: ['Monster Hunter'], features: ['Multijugador', 'Cooperativo', 'Aventura larga', 'Desafiante'] },
  'ni-no-kuni-wrath-of-the-white-witch': { genres: ['Aventura', 'RPG/JRPG'], features: ['Aventura larga'] },
  nier: { genres: ['Acción', 'Aventura', 'RPG/JRPG'], features: ['Aventura larga', 'Desafiante'] },
  'ninja-gaiden-master-collection': { genres: ['Acción'], worlds: ['Ninja Gaiden'], features: ['Colección', 'Desafiante'] },
  'no-more-heroes-1-and-2': { genres: ['Acción', 'Aventura'], features: ['Colección'] },
  'octopath-traveler': { genres: ['Aventura', 'RPG/JRPG'], features: ['Aventura larga'] },
  'pillars-of-eternity-complete-edition': { genres: ['RPG/JRPG', 'Estrategia y táctica'], features: ['Aventura larga', 'Desafiante'] },
  'sonic-frontiers': { genres: ['Acción', 'Aventura', 'Plataformas'], worlds: ['Sonic'], features: ['Mundo abierto', 'Exploración'] },
  skyrim: { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['The Elder Scrolls'], features: ['Mundo abierto', 'Aventura larga'] },
  'the-outer-worlds': { genres: ['Aventura', 'RPG/JRPG', 'Shooter'], features: ['Aventura larga'] },
  'witcher-3': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], features: ['Mundo abierto', 'Aventura larga'], featured: true },
  'the-wonderful-101-remastered': { genres: ['Acción', 'Aventura'], worlds: ['Nintendo'], features: ['Remaster'], confidence: 'media', reviewNote: 'Acción es el género dominante; Aventura se conserva como faceta secundaria.' },
  'triangle-strategy': { genres: ['RPG/JRPG', 'Estrategia y táctica'], features: ['Aventura larga', 'Desafiante'] },
  'xenoblade-chronicles-2': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Xenoblade Chronicles', 'Nintendo'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'] },
  'xenoblade-chronicles-3': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Xenoblade Chronicles', 'Nintendo'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'] },
  'xenoblade-chronicles-definitive-edition': { genres: ['Acción', 'Aventura', 'RPG/JRPG'], worlds: ['Xenoblade Chronicles', 'Nintendo'], features: ['Remaster', 'Mundo abierto', 'Exploración', 'Aventura larga'] },
  'hyrule-warriors-age-of-calamity': { genres: ['Acción'], worlds: ['Zelda', 'Nintendo'], features: ['Cooperativo'] },
  'zelda-botw': { genres: ['Acción', 'Aventura'], worlds: ['Zelda', 'Nintendo'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'], featured: true },
  'zelda-echoes': { genres: ['Acción', 'Aventura', 'Puzzle'], worlds: ['Zelda', 'Nintendo'], features: ['Exploración', 'Familiar'] },
  'zelda-awakening': { genres: ['Acción', 'Aventura', 'Puzzle'], worlds: ['Zelda', 'Nintendo'], features: ['Remake', 'Exploración', 'Familiar'] },
  'zelda-skyward': { genres: ['Acción', 'Aventura', 'Puzzle'], worlds: ['Zelda', 'Nintendo'], features: ['Remaster', 'Exploración', 'Aventura larga'] },
  'zelda-totk': { genres: ['Acción', 'Aventura'], worlds: ['Zelda', 'Nintendo'], features: ['Mundo abierto', 'Exploración', 'Aventura larga'], featured: true },
};

const featureCollectionMap: Partial<Record<GameFeature, Collection>> = {
  Multijugador: 'Multijugador',
  Cooperativo: 'Cooperativo',
  Familiar: 'Familiar',
  'Mundo abierto': 'Mundo abierto',
  Sandbox: 'Sandbox y creatividad',
  Colección: 'Clásicos, colecciones y remasters',
  Remaster: 'Clásicos, colecciones y remasters',
  Remake: 'Clásicos, colecciones y remasters',
  'Aventura larga': 'Aventuras largas',
  Desafiante: 'Difíciles y desafiantes',
};

function unique<T>(values: Array<T | undefined>) {
  return [...new Set(values.filter((value): value is T => value !== undefined))];
}

export function resolveTaxonomy(id: string, platform: 'Nintendo Switch' | 'Nintendo Switch 2') {
  const seed = gameTaxonomy[id];
  if (!seed) {
    return {
      genres: [] as Genre[],
      worlds: [] as World[],
      collections: platform === 'Nintendo Switch 2' ? ['Nintendo Switch 2'] as Collection[] : [],
      features: [] as GameFeature[],
      featured: false,
      confidence: 'baja' as TaxonomyConfidence,
      reviewNote: 'Sin taxonomía editorial explícita.',
      manualReview: true,
    };
  }

  const features = [...(seed.features ?? [])];
  return {
    genres: [...seed.genres],
    worlds: [...(seed.worlds ?? [])],
    collections: unique<Collection>([
      ...(seed.collections ?? []),
      seed.featured ? 'Destacados GameMaster' : undefined,
      platform === 'Nintendo Switch 2' ? 'Nintendo Switch 2' : undefined,
      ...features.map((feature) => featureCollectionMap[feature]),
    ]),
    features,
    featured: Boolean(seed.featured),
    confidence: seed.confidence ?? 'alta',
    reviewNote: seed.reviewNote,
    manualReview: Boolean(seed.manualReview),
  };
}

export type RailMatch =
  | { field: 'featured'; value: true }
  | { field: 'platform'; value: 'Nintendo Switch 2' }
  | { field: 'genre' | 'world' | 'collection' | 'feature'; value: string };

export type CatalogRailDefinition = {
  id: string;
  title: string;
  description: string;
  homepage: boolean;
  mode?: 'all' | 'any';
  matches: RailMatch[];
};

export const catalogRailDefinitions: CatalogRailDefinition[] = [
  { id: 'destacados-gamemaster', title: 'Destacados GameMaster', description: 'Una selección editorial para entrar a la biblioteca.', homepage: true, matches: [{ field: 'featured', value: true }] },
  { id: 'nintendo-switch-2', title: 'Nintendo Switch 2', description: 'Títulos registrados para la nueva generación.', homepage: true, matches: [{ field: 'platform', value: 'Nintendo Switch 2' }] },
  { id: 'mundo-mario', title: 'Mundo Mario', description: 'Plataformas, carreras, fiesta, deporte y RPG.', homepage: true, matches: [{ field: 'world', value: 'Mario' }] },
  { id: 'universo-zelda', title: 'Universo Zelda', description: 'Acción, aventura, exploración y acertijos.', homepage: true, matches: [{ field: 'world', value: 'Zelda' }] },
  { id: 'universo-pokemon', title: 'Universo Pokémon', description: 'RPG, aventura, exploración y propuestas familiares.', homepage: true, matches: [{ field: 'world', value: 'Pokémon' }] },
  { id: 'accion-aventura', title: 'Acción y aventura', description: 'Combate, recorrido y exploración en una misma experiencia.', homepage: true, mode: 'all', matches: [{ field: 'genre', value: 'Acción' }, { field: 'genre', value: 'Aventura' }] },
  { id: 'rpg-jrpg', title: 'RPG y JRPG', description: 'Progresión, grupos, decisiones y aventuras extensas.', homepage: true, matches: [{ field: 'genre', value: 'RPG/JRPG' }] },
  { id: 'shooters', title: 'Shooters', description: 'Disparos, acción táctica y combate en primera o tercera persona.', homepage: true, matches: [{ field: 'genre', value: 'Shooter' }] },
  { id: 'plataformas', title: 'Plataformas', description: 'Movimiento preciso, saltos y mundos construidos para recorrer.', homepage: true, matches: [{ field: 'genre', value: 'Plataformas' }] },
  { id: 'indies-esenciales', title: 'Indies esenciales', description: 'Autores, estudios y propuestas independientes imprescindibles.', homepage: true, matches: [{ field: 'collection', value: 'Indies esenciales' }] },
  { id: 'estrategia-tactica', title: 'Estrategia y táctica', description: 'Planificación, gestión y decisiones de combate.', homepage: false, matches: [{ field: 'genre', value: 'Estrategia y táctica' }] },
  { id: 'pelea', title: 'Pelea', description: 'Duelo, arena y combate competitivo.', homepage: false, matches: [{ field: 'genre', value: 'Pelea' }] },
  { id: 'carreras', title: 'Carreras', description: 'Velocidad, circuitos y competencia.', homepage: false, matches: [{ field: 'genre', value: 'Carreras' }] },
  { id: 'deportes', title: 'Deportes', description: 'Competencia deportiva y juego local o conectado.', homepage: false, matches: [{ field: 'genre', value: 'Deportes' }] },
  { id: 'fiesta-multijugador', title: 'Fiesta y multijugador', description: 'Opciones para competir, cooperar o jugar en grupo.', homepage: false, mode: 'any', matches: [{ field: 'genre', value: 'Fiesta' }, { field: 'collection', value: 'Multijugador' }] },
  { id: 'terror-supervivencia', title: 'Terror y supervivencia', description: 'Tensión, recursos limitados y atmósferas inquietantes.', homepage: false, matches: [{ field: 'genre', value: 'Terror y supervivencia' }] },
  { id: 'puzzle-exploracion', title: 'Puzzle y exploración', description: 'Acertijos, observación y descubrimiento.', homepage: false, mode: 'any', matches: [{ field: 'genre', value: 'Puzzle' }, { field: 'feature', value: 'Exploración' }] },
  { id: 'mundo-abierto', title: 'Mundo abierto', description: 'Espacios amplios con libertad de recorrido.', homepage: false, matches: [{ field: 'collection', value: 'Mundo abierto' }] },
  { id: 'sandbox-creatividad', title: 'Sandbox y creatividad', description: 'Sistemas abiertos para construir, diseñar o experimentar.', homepage: false, matches: [{ field: 'collection', value: 'Sandbox y creatividad' }] },
  { id: 'clasicos-colecciones-remasters', title: 'Clásicos, colecciones y remasters', description: 'Recopilaciones, regresos y versiones renovadas.', homepage: false, matches: [{ field: 'collection', value: 'Clásicos, colecciones y remasters' }] },
];

export type TaxonomyComparableGame = {
  platform: string;
  genres: string[];
  worlds: string[];
  collections: string[];
  features: string[];
  featured: boolean;
};

export function matchesCatalogRail(game: TaxonomyComparableGame, rail: CatalogRailDefinition) {
  const results = rail.matches.map((match) => {
    if (match.field === 'featured') return game.featured;
    if (match.field === 'platform') return game.platform === match.value;
    if (match.field === 'genre') return game.genres.includes(match.value);
    if (match.field === 'world') return game.worlds.includes(match.value);
    if (match.field === 'collection') return game.collections.includes(match.value);
    return game.features.includes(match.value);
  });
  return rail.mode === 'all' ? results.every(Boolean) : results.some(Boolean);
}
