const screens = [
  "Change Radar",
  "Claim CI",
  "Investigation",
  "VerityDecision Console",
  "Evidence Trace"
];

export default function Page() {
  return (
    <main>
      <h1>BioVerity</h1>
      <p>Continuously tested ecological claims with provenance-aware decisions.</p>
      <section>
        {screens.map((screen) => (
          <article key={screen}>
            <h2>{screen}</h2>
          </article>
        ))}
      </section>
    </main>
  );
}

