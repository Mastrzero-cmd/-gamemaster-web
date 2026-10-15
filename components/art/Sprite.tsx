import { VectorSprite, type SpriteName } from './VectorArt';

export type { SpriteName };

/**
 * Objeto rojo (vectorial) en su propio plano. Posición, tamaño y profundidad
 * viven en la hoja de estilos (`className`), así el arte nunca toca el contenido comercial.
 */
export function Sprite({ name, className, moving = true }: { name: SpriteName; className: string; moving?: boolean }) {
  return (
    <span className={`sprite ${moving ? 'depthPlane' : ''} ${className}`} aria-hidden="true">
      <VectorSprite name={name} />
    </span>
  );
}

/** Letras gigantes tonales del plano trasero; solo decoración. */
export function GiantType({ children, className }: { children: string; className: string }) {
  return <span className={`giantType depthPlane ${className}`} aria-hidden="true">{children}</span>;
}
