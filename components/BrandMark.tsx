import Image from 'next/image';

export function BrandMark() {
  return (
    <span className="brandMark" aria-label="GameMaster">
      <Image className="brandEmblem" src="/brand/logos/gamemaster-emblema.png" alt="" width={560} height={560} unoptimized aria-hidden="true" />
      <span className="brandWordmark" aria-hidden="true">Game<span>Master</span></span>
    </span>
  );
}
