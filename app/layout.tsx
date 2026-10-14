import type { Metadata, Viewport } from 'next';
import { Jersey_10, Outfit, Silkscreen } from 'next/font/google';
import { getSiteUrl } from '@/lib/site';
import './globals.css';

const display = Jersey_10({ variable: '--font-display', subsets: ['latin', 'latin-ext'], weight: '400' });
const pixel = Silkscreen({ variable: '--font-pixel', subsets: ['latin', 'latin-ext'], weight: ['400', '700'] });
const body = Outfit({ variable: '--font-body', subsets: ['latin', 'latin-ext'] });

const siteUrl = getSiteUrl();
const socialImage = siteUrl ? new URL('/og.png', siteUrl).toString() : undefined;

export const metadata: Metadata = {
  title: {
    default: 'GameMaster | Nintendo, streaming, IA y privacidad',
    template: '%s | GameMaster',
  },
  description: 'Explora 130 juegos digitales para Nintendo Switch y Switch 2, además de streaming, IA y privacidad bajo consulta directa.',
  metadataBase: siteUrl,
  alternates: siteUrl ? { canonical: siteUrl } : undefined,
  icons: {
    icon: '/brand/game-master-emblem-v4.png',
    shortcut: '/brand/game-master-emblem-v4.png',
    apple: '/brand/game-master-emblem-v4.png',
  },
  openGraph: {
    type: 'website',
    locale: 'es_MX',
    siteName: 'GameMaster',
    title: 'GameMaster | Nintendo, streaming, IA y privacidad',
    description: 'Gaming, streaming, IA y privacidad en una sola señal.',
    url: siteUrl,
    images: socialImage ? [{ url: socialImage, width: 1200, height: 630, alt: 'GameMaster — Gaming Nintendo, streaming, IA y privacidad' }] : [],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GameMaster | Nintendo, streaming, IA y privacidad',
    description: 'Gaming, streaming, IA y privacidad en una sola señal.',
    images: socialImage ? [socialImage] : [],
  },
};

export const viewport: Viewport = {
  colorScheme: 'dark',
  themeColor: '#050506',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es-MX"><body className={`${display.variable} ${pixel.variable} ${body.variable}`}>{children}</body></html>;
}
