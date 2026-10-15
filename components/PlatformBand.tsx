import Image from 'next/image';

/** Franja de plataformas: logos en PNG sin fondo, sobre una placa negra con corte diagonal. */
export function PlatformBand() {
  return (
    <section className="platformBand" aria-label="Ecosistema gaming" data-quote-bar-avoid>
      <div className="platformPlate sectionShell">
        <Image className="platformEmblem" src="/brand/logos/gamemaster-emblema.png" alt="GameMaster" width={560} height={560} unoptimized />
        <p className="pixelLabel platformCaption">✢ Universo gaming</p>
        <ul className="platformLogos">
          <li><Image src="/brand/logos/nintendo-switch.png" alt="Nintendo Switch" width={600} height={600} unoptimized /></li>
          <li><Image src="/brand/logos/playstation.png" alt="PlayStation" width={600} height={108} unoptimized /></li>
          <li><Image src="/brand/logos/steam.png" alt="Steam, para PC" width={600} height={600} unoptimized /></li>
        </ul>
      </div>
    </section>
  );
}
