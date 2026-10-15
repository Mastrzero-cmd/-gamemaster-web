import { ArrowUpRight } from 'lucide-react';
import { FACEBOOK_URL, GENERAL_CONTACT_URL } from '@/lib/contact';
import { Sprite } from './art/Sprite';

export function Footer() {
  return (
    <footer className="siteFooter">
      <div className="footerField depthPlane" aria-hidden="true" />
      <Sprite name="gamepad" className="footerSpriteGamepad" />
      <Sprite name="headset" className="footerSpriteHeadset" />
      <Sprite name="cartridge" className="footerSpriteCartridge" />
      <div className="sectionShell footerTop">
        <p className="pixelLabel">✢ GameMaster · Entretenimiento digital · México ✢</p>
        <p className="footerLede">Gaming Nintendo digital, streaming, IA y privacidad, con atención directa de una persona.</p>
        <div className="footerContact">
          <a className="buttonBlack" href={GENERAL_CONTACT_URL} target="_blank" rel="noreferrer">WhatsApp <ArrowUpRight aria-hidden="true" /></a>
          <a className="buttonBlack" href={FACEBOOK_URL} target="_blank" rel="noreferrer">Facebook <ArrowUpRight aria-hidden="true" /></a>
        </div>
      </div>
      <p className="footerWordmark" aria-hidden="true">GameMaster</p>
      <div className="sectionShell footerBottom">
        <span className="pixelLabel">© {new Date().getFullYear()} GameMaster</span>
        <p>Negocio independiente. Las marcas y artes mostradas pertenecen a sus respectivos titulares; no implican afiliación ni patrocinio.</p>
      </div>
    </footer>
  );
}
