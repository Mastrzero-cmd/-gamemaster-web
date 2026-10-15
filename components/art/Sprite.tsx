import Image from 'next/image';

const SPRITES = {
  cartridge: [396, 486],
  gamepad: [588, 400],
  joystick: [370, 490],
  handheld: [474, 476],
  'side-controller': [202, 528],
  headset: [466, 534],
  mouse: [390, 468],
  'memory-card': [224, 304],
  keycap: [328, 334],
  remote: [252, 560],
  tv: [538, 430],
  chip: [434, 598],
  headphones: [484, 602],
  phone: [280, 494],
  clapperboard: [456, 468],
  'console-tower': [294, 516],
  heart: [456, 410],
} as const;

export type SpriteName = keyof typeof SPRITES;

/**
 * A red foreground object on its own plane. Placement, size and depth live in
 * the stylesheet (`className`), so art direction never touches business content.
 */
export function Sprite({ name, className, moving = true }: { name: SpriteName; className: string; moving?: boolean }) {
  const [width, height] = SPRITES[name];
  return (
    <span className={`sprite ${moving ? 'depthPlane' : ''} ${className}`} aria-hidden="true">
      <Image src={`/art/cromo/sprite-${name}.webp`} alt="" width={width} height={height} unoptimized />
    </span>
  );
}

/** Oversized tonal lettering for the rear plane; decorative only. */
export function GiantType({ children, className }: { children: string; className: string }) {
  return <span className={`giantType depthPlane ${className}`} aria-hidden="true">{children}</span>;
}
