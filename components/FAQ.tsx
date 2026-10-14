const questions = [
  ['¿Qué plataformas de Gaming ofrece GameMaster?', 'La oferta comercial visible actual se limita a juegos digitales para Nintendo Switch y Nintendo Switch 2. No presentamos otras plataformas sin una fuente canónica.'],
  ['¿Cuánto cuesta cada juego?', 'El precio y la disponibilidad se confirman al momento para cada título. La web no publica importes exactos cuando no existe un valor canónico vigente.'],
  ['¿Qué diferencia hay entre Principal y Secundaria?', 'La Principal permite jugar desde cualquier usuario y puede abrirse sin conexión. La Secundaria se usa desde el perfil proporcionado y necesita una verificación breve por internet al abrir.'],
  ['¿Puedo jugar en línea?', 'Depende del título y de la modalidad. Esa condición se revisa antes de confirmar para no prometer una función que no aplique.'],
  ['¿Qué herramientas de IA ofrece GameMaster?', 'La oferta actual de IA incluye ChatGPT y Claude. Abacus no forma parte de la oferta. Precio, modalidad y disponibilidad se confirman directamente.'],
  ['¿Dónde aparece Proton VPN?', 'Proton VPN pertenece a Privacidad / servicios digitales; no se clasifica como IA ni como streaming. Su precio, duración y disponibilidad se consultan al momento.'],
  ['¿GameMaster está afiliado con las marcas mostradas?', 'No. GameMaster es un negocio independiente. Las marcas y artes pertenecen a sus respectivos titulares y se muestran como referencia.'],
];

export function FAQ() {
  return (
    <section className="faqSection sectionShell" id="preguntas" aria-labelledby="faq-title">
      <div className="sectionHeading faqHeading">
        <p className="pixelLabel">✢ Capítulo 05 · Respuestas claras</p>
        <h2 id="faq-title">Preguntas <em>frecuentes.</em></h2>
      </div>
      <div className="faqList">
        {questions.map(([question, answer], index) => (
          <details key={question}>
            <summary><span className="pixelLabel">{String(index + 1).padStart(2, '0')}</span><strong>{question}</strong><i aria-hidden="true" /></summary>
            <p>{answer}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
