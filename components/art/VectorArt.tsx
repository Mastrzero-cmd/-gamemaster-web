import type { ReactNode } from 'react';

/**
 * Arte vectorial (SVG) de GameMaster — objetos rojos del plano frontal.
 * Cada objeto es una sola figura con una sombra interna en rojo profundo y
 * detalles negros: nunca hay copias rojo/azul desplazadas.
 * Autor: Claude (bot de Fernando) · 5ª pasada del rediseño.
 */
const R = '#e8392f';
const RD = '#a3201a';
const RL = '#f5736a';
const K = '#0b0b10';
const W = '#f4f4ef';
const SW = 7;

type Draw = (props: { id: string }) => ReactNode;

const cartridge: Draw = () => (
  <>
    <path d="M40 30h316a20 20 0 0 1 20 20v330l-34 34v32H54v-32l-34-34V50a20 20 0 0 1 20-20z" fill={R} stroke={K} strokeWidth={SW} strokeLinejoin="round" />
    <path d="M20 380l34 34v32h38V60H40a20 20 0 0 0-20 20z" fill={RD} opacity=".55" />
    <rect x="86" y="74" width="224" height="170" rx="12" fill={K} />
    <rect x="104" y="92" width="188" height="134" rx="6" fill={W} opacity=".92" />
    <path d="M122 200l46-60 36 40 30-26 38 46z" fill={RD} />
    <circle cx="256" cy="124" r="14" fill={R} />
    <rect x="120" y="282" width="156" height="14" rx="4" fill={K} />
    <rect x="120" y="310" width="156" height="14" rx="4" fill={K} opacity=".6" />
    <rect x="104" y="440" width="188" height="20" fill={K} />
    {Array.from({ length: 9 }, (_, i) => <rect key={i} x={110 + i * 20} y="420" width="10" height="22" fill={K} />)}
  </>
);

const gamepad: Draw = () => (
  <>
    <path d="M150 60h288c70 0 100 40 120 150l20 100c10 50-20 80-60 80-36 0-56-26-84-70-12-16-26-24-48-24H202c-22 0-36 8-48 24-28 44-48 70-84 70-40 0-70-30-60-80l20-100C50 100 80 60 150 60z" fill={R} stroke={K} strokeWidth={SW} strokeLinejoin="round" />
    <path d="M150 60h288c30 0 52 8 68 26-14-6-30-8-48-8H160c-48 0-80 20-100 80L40 310c-6 34 8 56 32 66-28-6-46-38-40-66l20-100C70 100 80 60 150 60z" fill={RL} opacity=".45" />
    <path d="M128 140h34v34h34v34h-34v34h-34v-34H94v-34h34z" fill={K} />
    <circle cx="432" cy="144" r="22" fill={K} /><circle cx="486" cy="190" r="22" fill={K} />
    <circle cx="378" cy="190" r="22" fill={K} /><circle cx="432" cy="236" r="22" fill={K} />
    <circle cx="432" cy="144" r="10" fill={R} />
    <circle cx="238" cy="266" r="34" fill={K} /><circle cx="238" cy="266" r="18" fill={RD} />
    <circle cx="352" cy="266" r="34" fill={K} /><circle cx="352" cy="266" r="18" fill={RD} />
    <rect x="262" y="120" width="66" height="22" rx="11" fill={K} />
  </>
);

const joystick: Draw = () => (
  <>
    <path d="M30 400h310l-18 66H48z" fill={K} />
    <path d="M60 330h250a24 24 0 0 1 24 24v46H36v-46a24 24 0 0 1 24-24z" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="166" y="150" width="38" height="190" fill={K} />
    <circle cx="185" cy="96" r="74" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M130 76a56 56 0 0 1 56-36" fill="none" stroke={RL} strokeWidth="12" strokeLinecap="round" />
    <circle cx="90" cy="372" r="14" fill={K} /><circle cx="140" cy="372" r="14" fill={K} opacity=".6" />
  </>
);

const handheld: Draw = () => (
  <>
    <rect x="30" y="30" width="414" height="416" rx="44" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M30 380v22a44 44 0 0 0 44 44h326a44 44 0 0 0 44-44v-22z" fill={RD} opacity=".55" />
    <rect x="86" y="72" width="302" height="200" rx="14" fill={K} />
    <rect x="104" y="90" width="266" height="164" rx="6" fill="#1b2a6b" />
    <path d="M104 230l60-70 50 44 40-34 76 60v24H104z" fill="#3f55b8" />
    <path d="M118 322h30v26h26v30h-26v26h-30v-26H92v-30h26z" fill={K} />
    <circle cx="352" cy="334" r="18" fill={K} /><circle cx="394" cy="366" r="18" fill={K} />
    <circle cx="310" cy="366" r="18" fill={K} /><circle cx="352" cy="398" r="18" fill={K} />
    <rect x="196" y="372" width="82" height="16" rx="8" fill={K} />
  </>
);

const sideController: Draw = () => (
  <>
    <rect x="26" y="26" width="150" height="476" rx="75" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M26 380v47a75 75 0 0 0 75 75 75 75 0 0 0 75-75v-47z" fill={RD} opacity=".5" />
    <circle cx="101" cy="130" r="42" fill={K} /><circle cx="101" cy="130" r="22" fill={RD} />
    <rect x="76" y="62" width="50" height="12" rx="6" fill={K} />
    <circle cx="101" cy="270" r="15" fill={K} /><circle cx="101" cy="318" r="15" fill={K} />
    <circle cx="68" cy="294" r="15" fill={K} /><circle cx="134" cy="294" r="15" fill={K} />
  </>
);

const headset: Draw = () => (
  <>
    <path d="M70 300V230a163 163 0 0 1 326 0v70" fill="none" stroke={K} strokeWidth="46" strokeLinecap="round" />
    <path d="M70 300V230a163 163 0 0 1 326 0v70" fill="none" stroke={R} strokeWidth="30" strokeLinecap="round" />
    <rect x="30" y="270" width="96" height="190" rx="40" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="340" y="270" width="96" height="190" rx="40" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="30" y="390" width="96" height="70" rx="30" fill={RD} opacity=".55" />
    <rect x="340" y="390" width="96" height="70" rx="30" fill={RD} opacity=".55" />
    <path d="M78 460q4 56 80 60h60" fill="none" stroke={K} strokeWidth="14" strokeLinecap="round" />
    <rect x="212" y="500" width="64" height="30" rx="15" fill={K} />
  </>
);

const mouse: Draw = () => (
  <>
    <path d="M195 30c100 0 165 60 165 160v110c0 90-60 138-165 138S30 390 30 300V190C30 90 95 30 195 30z" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M30 300c0 90 60 138 165 138s165-48 165-138v-30c-30 70-90 100-165 100S60 340 30 270z" fill={RD} opacity=".5" />
    <path d="M195 30v170M30 200h330" stroke={K} strokeWidth={SW} fill="none" />
    <rect x="176" y="96" width="38" height="70" rx="19" fill={K} />
  </>
);

const memoryCard: Draw = () => (
  <>
    <path d="M30 30h130l34 36v208a20 20 0 0 1-20 20H50a20 20 0 0 1-20-20z" fill={R} stroke={K} strokeWidth={SW} strokeLinejoin="round" />
    <path d="M30 200h164v74a20 20 0 0 1-20 20H50a20 20 0 0 1-20-20z" fill={RD} opacity=".5" />
    {Array.from({ length: 5 }, (_, i) => <rect key={i} x={52 + i * 26} y="44" width="14" height="46" fill={K} />)}
    <rect x="54" y="130" width="116" height="80" rx="8" fill={K} />
    <rect x="68" y="146" width="88" height="10" rx="4" fill={W} opacity=".85" />
    <rect x="68" y="170" width="60" height="10" rx="4" fill={W} opacity=".55" />
  </>
);

const keycap: Draw = () => (
  <>
    <path d="M64 60h200l36 40v180l-36 40H64l-36-40V100z" fill={R} stroke={K} strokeWidth={SW} strokeLinejoin="round" />
    <rect x="76" y="86" width="176" height="150" rx="22" fill={RL} opacity=".5" />
    <path d="M28 280l36 40h200l36-40v-40l-36 36H64l-36-36z" fill={RD} opacity=".6" />
    <path d="M130 130v70M130 130h60M130 165h50" fill="none" stroke={K} strokeWidth="16" strokeLinecap="round" />
  </>
);

const remote: Draw = () => (
  <>
    <rect x="30" y="30" width="192" height="500" rx="46" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M30 430v54a46 46 0 0 0 46 46h100a46 46 0 0 0 46-46v-54z" fill={RD} opacity=".5" />
    <circle cx="126" cy="92" r="22" fill={K} /><circle cx="126" cy="92" r="9" fill={R} />
    <circle cx="126" cy="230" r="66" fill={K} /><circle cx="126" cy="230" r="26" fill={RD} />
    <circle cx="70" cy="354" r="20" fill={K} /><circle cx="126" cy="354" r="20" fill={K} /><circle cx="182" cy="354" r="20" fill={K} />
    <circle cx="70" cy="414" r="20" fill={K} opacity=".6" /><circle cx="126" cy="414" r="20" fill={K} opacity=".6" /><circle cx="182" cy="414" r="20" fill={K} opacity=".6" />
  </>
);

const tv: Draw = () => (
  <>
    <rect x="30" y="30" width="478" height="320" rx="30" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="62" y="62" width="414" height="256" rx="12" fill={K} />
    <path d="M232 130l108 60-108 60z" fill={R} />
    <path d="M180 350l-30 50h238l-30-50z" fill={K} />
  </>
);

const chip: Draw = () => (
  <>
    {Array.from({ length: 6 }, (_, i) => (
      <g key={i} fill={K}>
        <rect x={86 + i * 52} y="14" width="22" height="64" />
        <rect x={86 + i * 52} y="520" width="22" height="64" />
        <rect x="14" y={110 + i * 62} width="64" height="22" />
        <rect x="356" y={110 + i * 62} width="64" height="22" />
      </g>
    ))}
    <rect x="64" y="64" width="306" height="470" rx="30" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="64" y="440" width="306" height="94" rx="30" fill={RD} opacity=".5" />
    <rect x="120" y="140" width="194" height="194" rx="18" fill={K} />
    <path d="M217 170l16 48 48 16-48 16-16 48-16-48-48-16 48-16z" fill={R} />
    <circle cx="96" cy="96" r="10" fill={K} />
  </>
);

const headphones: Draw = () => (
  <>
    <path d="M70 340V260a172 172 0 0 1 344 0v80" fill="none" stroke={K} strokeWidth="44" strokeLinecap="round" />
    <path d="M70 340V260a172 172 0 0 1 344 0v80" fill="none" stroke={R} strokeWidth="28" strokeLinecap="round" />
    <rect x="30" y="300" width="110" height="270" rx="46" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="344" y="300" width="110" height="270" rx="46" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="30" y="470" width="110" height="100" rx="40" fill={RD} opacity=".55" />
    <rect x="344" y="470" width="110" height="100" rx="40" fill={RD} opacity=".55" />
  </>
);

const phone: Draw = () => (
  <>
    <rect x="30" y="30" width="220" height="434" rx="40" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="56" y="76" width="168" height="342" rx="14" fill={K} />
    <rect x="104" y="46" width="72" height="12" rx="6" fill={K} />
    <path d="M140 150l56 24v52c0 40-24 68-56 82-32-14-56-42-56-82v-52z" fill={R} />
    <path d="M140 150v158c-32-14-56-42-56-82v-52z" fill={RD} opacity=".6" />
    <circle cx="140" cy="440" r="8" fill={K} />
  </>
);

const clapperboard: Draw = () => (
  <>
    <rect x="30" y="170" width="396" height="268" rx="22" fill={R} stroke={K} strokeWidth={SW} />
    <rect x="30" y="360" width="396" height="78" rx="22" fill={RD} opacity=".5" />
    <path d="M30 170l24-110 396 78-18 32z" fill={K} />
    {[0, 1, 2, 3].map((i) => <path key={i} d={`M${70 + i * 90} 84l50 10-20 44-50-10z`} fill={W} opacity=".92" />)}
    <path d="M186 248l112 60-112 60z" fill={K} />
  </>
);

const consoleTower: Draw = () => (
  <>
    <path d="M60 30h174c20 0 30 10 30 30v396c0 20-14 30-30 30H60c-16 0-30-10-30-30V60c0-20 10-30 30-30z" fill={K} />
    <path d="M70 30h70c52 0 80 30 80 80v300c0 52-28 80-80 80H70c-20 0-30-10-30-30V60c0-20 10-30 30-30z" fill={R} stroke={K} strokeWidth={SW} />
    <path d="M160 40h70c20 0 30 10 30 30v360c0 20-10 30-30 30h-70c40-30 50-60 50-100V140c0-40-10-70-50-100z" fill={RD} opacity=".5" />
    <rect x="96" y="120" width="26" height="250" rx="13" fill={K} />
    <circle cx="136" cy="428" r="10" fill={K} /><rect x="60" y="480" width="170" height="14" rx="7" fill={K} />
  </>
);

const heart: Draw = () => (
  <>
    <path d="M228 390C80 290 34 220 34 140 34 80 80 40 134 40c40 0 74 22 94 58 20-36 54-58 94-58 54 0 100 40 100 100 0 80-46 150-194 250z" fill={R} stroke={K} strokeWidth={SW} strokeLinejoin="round" />
    <path d="M70 120c10-40 40-56 70-50" fill="none" stroke={RL} strokeWidth="16" strokeLinecap="round" />
  </>
);

export const SPRITES = {
  cartridge: [396, 486, cartridge],
  gamepad: [588, 400, gamepad],
  joystick: [370, 490, joystick],
  handheld: [474, 476, handheld],
  'side-controller': [202, 528, sideController],
  headset: [466, 534, headset],
  mouse: [390, 468, mouse],
  'memory-card': [224, 304, memoryCard],
  keycap: [328, 334, keycap],
  remote: [252, 560, remote],
  tv: [538, 430, tv],
  chip: [434, 598, chip],
  headphones: [484, 602, headphones],
  phone: [280, 494, phone],
  clapperboard: [456, 468, clapperboard],
  'console-tower': [294, 516, consoleTower],
  heart: [456, 410, heart],
} as const;

export type SpriteName = keyof typeof SPRITES;

export function VectorSprite({ name }: { name: SpriteName }) {
  const [width, height, draw] = SPRITES[name];
  return (
    <svg viewBox={`0 0 ${width} ${height}`} width={width} height={height} focusable="false" aria-hidden="true">
      {draw({ id: name })}
    </svg>
  );
}

/** Lámina de consola + TV + mando (hero). Plano trasero: azul suave; frontal: rojo. */
export function HeroRear() {
  return (
    <svg viewBox="0 0 864 1152" focusable="false" aria-hidden="true">
      <defs>
        <pattern id="hxHex" width="64" height="56" patternUnits="userSpaceOnUse" patternTransform="scale(1.1)">
          <path d="M16 0h32l16 28-16 28H16L0 28z" fill="none" stroke="#9fb0ff" strokeOpacity=".28" strokeWidth="2" />
        </pattern>
      </defs>
      <rect x="40" y="90" width="784" height="960" rx="40" fill="#2a3a8a" />
      <rect x="40" y="90" width="784" height="960" rx="40" fill="url(#hxHex)" />
      <rect x="110" y="170" width="644" height="420" rx="26" fill={K} stroke="#8aa0ff" strokeOpacity=".5" strokeWidth="6" />
      <rect x="140" y="200" width="584" height="360" rx="12" fill="#1a2766" />
      <path d="M140 500l110-150 90 90 80-70 160 150 144-90v130H140z" fill="#3a50b5" />
      <circle cx="590" cy="290" r="46" fill="#9fb0ff" opacity=".55" />
      <rect x="380" y="590" width="104" height="60" fill={K} />
      <rect x="260" y="650" width="344" height="26" rx="13" fill={K} />
      <path d="M90 880h684M90 940h684M90 1000h684" stroke="#9fb0ff" strokeOpacity=".25" strokeWidth="3" />
    </svg>
  );
}

export function HeroFront() {
  return (
    <svg viewBox="0 0 864 1152" focusable="false" aria-hidden="true">
      {/* consola híbrida */}
      <rect x="140" y="520" width="584" height="300" rx="44" fill={K} stroke={K} strokeWidth="6" />
      <rect x="220" y="548" width="424" height="244" rx="16" fill="#1a2766" />
      <path d="M220 740l80-100 70 60 60-50 110 90v52H220z" fill="#3a50b5" />
      <path d="M144 540a62 62 0 0 1 62-62h22v400h-22a62 62 0 0 1-62-62z" fill={R} stroke={K} strokeWidth="7" />
      <path d="M720 540a62 62 0 0 0-62-62h-22v400h22a62 62 0 0 0 62-62z" fill={R} stroke={K} strokeWidth="7" />
      <circle cx="186" cy="620" r="26" fill={K} /><circle cx="186" cy="620" r="12" fill={RD} />
      <circle cx="678" cy="740" r="26" fill={K} /><circle cx="678" cy="740" r="12" fill={RD} />
      <circle cx="660" cy="590" r="12" fill={K} /><circle cx="700" cy="620" r="12" fill={K} />
      <circle cx="620" cy="620" r="12" fill={K} /><circle cx="660" cy="650" r="12" fill={K} />
      {/* mando */}
      <g transform="translate(250 740) scale(.9)">
        {gamepad({ id: 'h' })}
      </g>
    </svg>
  );
}

/** Placa de circuito (IA): trasera. */
export function ChipRear() {
  const traces = [140, 230, 320, 410, 500, 590, 680, 770];
  return (
    <svg viewBox="0 0 864 1152" focusable="false" aria-hidden="true">
      <rect x="30" y="80" width="804" height="990" rx="44" fill="#2a3a8a" />
      <g fill="none" stroke="#9fb0ff" strokeOpacity=".5" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round">
        {traces.map((x, i) => (
          <g key={x}>
            <path d={`M${x} 90V${200 + (i % 3) * 40}l${i % 2 ? 40 : -40} 40v${120 + (i % 4) * 20}`} />
            <path d={`M${x} 1060V${940 - (i % 3) * 40}l${i % 2 ? -40 : 40} -40v${-100 - (i % 4) * 20}`} />
            <circle cx={x} cy="96" r="10" fill="#9fb0ff" fillOpacity=".5" />
            <circle cx={x} cy="1054" r="10" fill="#9fb0ff" fillOpacity=".5" />
          </g>
        ))}
        {traces.slice(0, 5).map((y, i) => (
          <g key={`h${y}`}>
            <path d={`M40 ${y + 120}H${120 + (i % 2) * 40}l30 30h${90}`} />
            <path d={`M824 ${y + 120}H${744 - (i % 2) * 40}l-30 30h-90`} />
          </g>
        ))}
      </g>
    </svg>
  );
}

/** Núcleo de IA: frontal rojo. */
export function ChipFront() {
  return (
    <svg viewBox="0 0 864 1152" focusable="false" aria-hidden="true">
      <g>
        {Array.from({ length: 6 }, (_, i) => (
          <g key={i} fill={K}>
            <rect x={286 + i * 50} y="300" width="24" height="56" />
            <rect x={286 + i * 50} y="676" width="24" height="56" />
            <rect x="244" y={364 + i * 50} width="56" height="24" />
            <rect x="564" y={364 + i * 50} width="56" height="24" />
          </g>
        ))}
        <rect x="296" y="346" width="272" height="334" rx="30" fill={R} stroke={K} strokeWidth="8" />
        <rect x="296" y="590" width="272" height="90" rx="30" fill={RD} opacity=".5" />
        <rect x="346" y="396" width="172" height="172" rx="16" fill={K} />
        <path d="M432 418l14 44 44 14-44 14-14 44-14-44-44-14 44-14z" fill={R} />
      </g>
    </svg>
  );
}
