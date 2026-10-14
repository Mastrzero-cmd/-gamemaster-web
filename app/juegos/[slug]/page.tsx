import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft, ArrowRight, ArrowUpRight, MessageCircle, UserRound, Wifi } from 'lucide-react';
import { catalog, getGameBySlug, getRelatedGames } from '@/app/data/catalog';
import { DepthPlanes } from '@/components/art/DepthPlanes';
import { Footer } from '@/components/Footer';
import { Header } from '@/components/Header';
import { gameQuoteMessage, toWhatsApp } from '@/lib/contact';
import { getSiteUrl } from '@/lib/site';

type GamePageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return catalog.map((game) => ({ slug: game.slug }));
}

export async function generateMetadata({ params }: GamePageProps): Promise<Metadata> {
  const { slug } = await params;
  const game = getGameBySlug(slug);
  if (!game) return { title: 'Juego no encontrado' };

  const siteUrl = getSiteUrl();
  const title = `${game.title} | GameMaster`;
  const description = `Consulta precio y disponibilidad de ${game.title} para ${game.platform}. Ficha de catálogo GameMaster.`;
  const socialImage = siteUrl ? new URL(game.image, siteUrl).toString() : undefined;

  return {
    title: game.title,
    description,
    alternates: siteUrl ? { canonical: new URL(`/juegos/${game.slug}`, siteUrl).toString() } : undefined,
    openGraph: {
      type: 'website',
      title,
      description,
      url: siteUrl ? new URL(`/juegos/${game.slug}`, siteUrl).toString() : undefined,
      images: socialImage ? [{ url: socialImage, alt: `Portada de ${game.title}` }] : [],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: socialImage ? [socialImage] : [],
    },
  };
}

export default async function GamePage({ params }: GamePageProps) {
  const { slug } = await params;
  const game = getGameBySlug(slug);
  if (!game) notFound();

  const relatedGames = getRelatedGames(game, 8);
  const quoteUrl = toWhatsApp(gameQuoteMessage(game.title, game.platform));
  const metadataTags = [...game.genres, ...game.worlds, ...game.features];

  return (
    <>
      <DepthPlanes />
      <Header homePath="/" />
      <main className="gameDetailPage" id="inicio">
        <section className="gameDetailHero" aria-labelledby="game-title">
          <div className="gameDetailField depthPlane" aria-hidden="true" />
          <div className="gameDetailInner sectionShell">
            <div className="gameDetailArt">
              <div className="gameDetailBlade depthPlane" aria-hidden="true" />
              <div className="gameDetailCover">
                <Image src={game.image} alt={`Portada de ${game.title}`} fill sizes="(max-width: 760px) 78vw, 430px" priority />
              </div>
            </div>

            <div className="gameDetailCopy">
              <Link className="backLink" href="/#catalogo"><ArrowLeft aria-hidden="true" /> Volver al catálogo</Link>
              <p className="pixelLabel gameDetailKicker">{game.platform} · Categoría fuente: {game.sourceCategory}</p>
              <h1 id="game-title">{game.title}</h1>
              {metadataTags.length > 0 && <div className="gameDetailTags">{metadataTags.map((tag) => <span key={tag}>{tag}</span>)}</div>}
              <p className="gameDetailDescription">Título digital registrado en el catálogo de GameMaster para {game.platform}. La ficha usa únicamente metadatos disponibles; precio, modalidad y disponibilidad se verifican contigo.</p>
              <dl className="gameDetailStatus">
                <div><dt>Precio</dt><dd>Consultar precio</dd></div>
                <div><dt>Estado</dt><dd>Consultar disponibilidad</dd></div>
              </dl>
              <a className="buttonRed" href={quoteUrl} target="_blank" rel="noreferrer"><MessageCircle aria-hidden="true" /> Cotizar este juego <ArrowUpRight aria-hidden="true" /></a>
              <small>GameMaster es un negocio independiente. La portada pertenece a su respectivo titular y se muestra como referencia.</small>
            </div>
          </div>
        </section>

        <section className="detailModes" aria-labelledby="detail-modes-title">
          <div className="sectionShell">
            <div className="sectionHeading">
              <p className="pixelLabel">✢ Modalidades de acceso</p>
              <h2 id="detail-modes-title">Principal o <em>Secundaria</em></h2>
              <p>La opción aplicable se confirma antes de comprar.</p>
            </div>
            <div className="modeGrid">
              <article className="modeCard modePrincipal">
                <header><span className="pixelLabel">Opción 01</span><h3>Cuenta Principal</h3></header>
                <ul><li><UserRound aria-hidden="true" /><span>Permite jugar con cualquier perfil de la consola y puede abrirse sin conexión a internet.</span></li></ul>
              </article>
              <article className="modeCard modeSecondary">
                <header><span className="pixelLabel">Opción 02</span><h3>Cuenta Secundaria</h3></header>
                <ul><li><Wifi aria-hidden="true" /><span>Se usa desde el perfil proporcionado y necesita una conexión breve para verificar al abrir.</span></li></ul>
              </article>
            </div>
          </div>
        </section>

        <section className="relatedSection sectionShell" aria-labelledby="related-title">
          <div className="relatedHeading"><div><p className="pixelLabel">✢ Sigue explorando</p><h2 id="related-title">Juegos relacionados</h2></div><Link href="/#catalogo">Ver catálogo completo <ArrowRight aria-hidden="true" /></Link></div>
          <div className="relatedRail" tabIndex={0} role="region" aria-label="Juegos relacionados. Desplázate horizontalmente para ver más.">
            {relatedGames.map((related) => (
              <Link className="relatedCard" href={`/juegos/${related.slug}`} key={related.id}>
                <span><Image src={related.image} alt={`Portada de ${related.title}`} fill sizes="(max-width: 720px) 64vw, 210px" /></span>
                <small>{related.platform === 'Nintendo Switch 2' ? 'SWITCH 2' : 'SWITCH'} · {related.sourceCategory}</small>
                <strong>{related.title}</strong>
                <em>Consultar precio <ArrowRight aria-hidden="true" /></em>
              </Link>
            ))}
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
