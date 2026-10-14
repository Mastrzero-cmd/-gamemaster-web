import { DepthPlanes } from '@/components/art/DepthPlanes';
import { Catalog } from '@/components/catalog/Catalog';
import { FAQ } from '@/components/FAQ';
import { Footer } from '@/components/Footer';
import { Header } from '@/components/Header';
import { Hero } from '@/components/Hero';
import { MobileQuoteBar } from '@/components/MobileQuoteBar';
import { ProductPreviewModal } from '@/components/ProductPreviewModal';
import { PurchaseModes } from '@/components/PurchaseModes';
import { QuoteBuilder } from '@/components/QuoteBuilder';
import { Universes } from '@/components/Universes';

export default function HomePage() {
  return (
    <>
      <DepthPlanes />
      <Header />
      <main>
        <Hero />
        <Catalog />
        <Universes />
        <PurchaseModes />
        <QuoteBuilder />
        <FAQ />
      </main>
      <Footer />
      <MobileQuoteBar />
      <ProductPreviewModal />
    </>
  );
}
