'use client';

import { Fragment, useMemo, useState } from 'react';
import { ArrowRight, ChevronDown, Compass, MessageCircle, Search } from 'lucide-react';
import { catalog, exploreCatalogShelves, homepageCatalogShelves } from '@/app/data/catalog';
import { toWhatsApp } from '@/lib/contact';
import { CatalogShelf } from './CatalogShelf';
import { Filters, type CatalogFilterState } from './Filters';
import { GameCard } from './GameCard';

function normalizeSearch(value: string) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('es');
}

const initialFilters: CatalogFilterState = {
  platform: 'Todas',
  genres: [],
  worlds: [],
  collections: [],
};

const INTERLUDE_AFTER = 2;

const missingGameUrl = toWhatsApp('Hola, busco un juego de Nintendo Switch que no aparece en el catálogo. ¿Me ayudan a revisarlo?');

function CatalogInterlude() {
  return (
    <aside className="catalogInterlude" aria-labelledby="interlude-title">
      <div className="interludeField depthPlane" aria-hidden="true" />
      <div className="interludeBlade depthPlane" aria-hidden="true" />
      <div className="interludeCopy">
        <p className="pixelLabel">✢ Pedido especial</p>
        <h3 id="interlude-title">¿No ves tu juego?</h3>
        <p>El catálogo crece con lo que nos piden. Escríbenos el título y revisamos precio y disponibilidad contigo.</p>
        <a className="buttonBlack" href={missingGameUrl} target="_blank" rel="noreferrer"><MessageCircle aria-hidden="true" /> Preguntar por un título</a>
      </div>
    </aside>
  );
}

export function Catalog() {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<CatalogFilterState>(initialFilters);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [showExploreMore, setShowExploreMore] = useState(false);

  const results = useMemo(() => {
    const normalizedQuery = normalizeSearch(query.trim());
    return catalog.filter((game) => {
      const queryMatch = !normalizedQuery || normalizeSearch(game.title).includes(normalizedQuery);
      const platformMatch = filters.platform === 'Todas' || game.platform === filters.platform;
      const genresMatch = !filters.genres.length || game.genres.some((genre) => filters.genres.includes(genre));
      const worldsMatch = !filters.worlds.length || game.worlds.some((world) => filters.worlds.includes(world));
      const collectionMatch = !filters.collections.length || game.collections.some((collection) => filters.collections.includes(collection));
      return queryMatch && platformMatch && genresMatch && worldsMatch && collectionMatch;
    }).sort((a, b) => a.title.localeCompare(b.title, 'es'));
  }, [filters, query]);

  const isExploring = Boolean(query.trim())
    || filters.platform !== 'Todas'
    || filters.genres.length > 0
    || filters.worlds.length > 0
    || filters.collections.length > 0;

  const toggleFacet = (facet: 'genres' | 'worlds' | 'collections', value: string) => {
    setFilters((current) => ({
      ...current,
      [facet]: current[facet].includes(value)
        ? current[facet].filter((item) => item !== value)
        : [...current[facet], value],
    }));
  };

  const clearFilters = () => {
    setQuery('');
    setFilters(initialFilters);
  };

  const freeSearchUrl = query.trim()
    ? toWhatsApp(`Hola, busco ${query.trim()} para Nintendo Switch. ¿Me ayudan a revisar precio y disponibilidad?`)
    : missingGameUrl;

  return (
    <section className="catalogSection" id="catalogo" aria-labelledby="catalog-title" data-quote-bar-avoid>
      <div className="catalogHeading sectionShell">
        <p className="pixelLabel">✢ Capítulo 01 · Gaming</p>
        <h2 id="catalog-title">Encuentra tu <em>próxima partida.</em></h2>
        <p>Busca por título o combina plataforma, género, franquicia y colección. Agrega con <strong>+</strong> los juegos que quieras y cotízalos juntos.</p>
      </div>

      <div className="sectionShell">
        <Filters
          query={query}
          filters={filters}
          resultsCount={results.length}
          filtersOpen={filtersOpen}
          onQueryChange={setQuery}
          onPlatformChange={(platform) => setFilters((current) => ({ ...current, platform }))}
          onFacetToggle={toggleFacet}
          onFiltersOpenChange={setFiltersOpen}
          onClear={clearFilters}
        />
      </div>

      {isExploring ? (
        results.length ? (
          <div className="catalogResults sectionShell">
            <div className="resultsHeading"><strong>{results.length} {results.length === 1 ? 'resultado' : 'resultados'}</strong><button type="button" onClick={clearFilters}>Limpiar filtros</button></div>
            <div className="gameGrid">
              {results.map((game, index) => <GameCard game={game} index={index} key={game.id} />)}
            </div>
          </div>
        ) : (
          <div className="emptyResults sectionShell" role="status">
            <Search aria-hidden="true" />
            <p className="pixelLabel">Búsqueda sin coincidencias</p>
            <h3>No aparece en esta selección</h3>
            <p>Prueba otra combinación o pregúntanos por el título. Nada se presenta como disponible hasta confirmarlo.</p>
            <div>
              <button type="button" className="buttonGhost" onClick={clearFilters}>Limpiar filtros</button>
              <a className="buttonRed" href={freeSearchUrl} target="_blank" rel="noreferrer">Consultar por WhatsApp <ArrowRight aria-hidden="true" /></a>
            </div>
          </div>
        )
      ) : (
        <div className="catalogShelves">
          {homepageCatalogShelves.map((shelf, index) => (
            <Fragment key={shelf.id}>
              <CatalogShelf {...shelf} position={index} />
              {index === INTERLUDE_AFTER && <CatalogInterlude />}
            </Fragment>
          ))}
          <div className="exploreMoreControl sectionShell">
            <div><Compass aria-hidden="true" /><span><strong>Explorar más géneros</strong><small>Estrategia, pelea, carreras, terror, puzzle, mundo abierto y más.</small></span></div>
            <button type="button" className="buttonGhost" aria-expanded={showExploreMore} aria-controls="explore-more-shelves" onClick={() => setShowExploreMore((current) => !current)}>
              {showExploreMore ? 'Mostrar menos' : 'Abrir más carruseles'} <ChevronDown aria-hidden="true" />
            </button>
          </div>
          {showExploreMore && (
            <div className="exploreMoreShelves" id="explore-more-shelves">
              {exploreCatalogShelves.map((shelf, index) => <CatalogShelf {...shelf} position={homepageCatalogShelves.length + index} key={shelf.id} />)}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
