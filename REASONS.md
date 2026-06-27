# REASONS Canvas — Runder Tisch zur gemeinsamen Problemlösung

> Erstellt: 2026-06-27
> Status: In Umsetzung — Stufe A (Playbook und Lernschleife) gebaut, Trockenlauf (Operation 7) und Stufe B offen

---

## R — Requirements (Anforderungen)

**Problemdefinition:**
Es fehlt ein moderierter runder Tisch, an dem der Nutzer gemeinsam mit zwei Experten ein Problem kritisch-dialektisch, freimütig und wohlwollend bearbeitet. Das Ziel ist nicht ein Artikel, sondern ein disziplinierter Diskurs. Zuerst wird der Problemraum gemeinsam durchdrungen, und der Moderator gibt den Lösungsraum erst frei, wenn alle drei das Problem tragend verstanden haben. Im Lösungsraum wird entlang des Tetralemmas gearbeitet, damit der Raum nicht ins Entweder-oder kippt. Die Experten erden ihre Beiträge an den wissenschaftlichen Grundlagen des Nutzers. Das Ergebnis soll eine anschlussfähige Lösung im Luhmann'schen Sinn sein. Über die einzelne Session hinaus soll das Gesamtsystem selbständig lernen, also nach jeder Session eine Retrospektive machen und Verbesserungen für die nächste Session planen.

**Akzeptanzkriterien (Gherkin):**

    Szenario: Problemraum vor Lösungsraum
      Gegeben ein eingebrachtes Problem
      Wenn der Problemraum noch nicht tragend verstanden ist
      Dann hält der Moderator den Lösungsraum geschlossen
      Und treibt das gemeinsame Verständnis weiter

    Szenario: Freigabe des Lösungsraums mit benanntem Kriterium
      Gegeben die lebende Karte des Moderators
      Wenn der harte Stand das geteilte Verständnis trägt und keine blockierenden Widersprüche oder offenen Fragen bestehen
      Dann gibt der Moderator den Lösungsraum frei
      Und benennt das Kriterium, an dem er das festmacht

    Szenario: Geerdeter Expertenbeitrag
      Gegeben ein Beitrag eines Experten
      Wenn er eine fachliche Aussage macht
      Dann ist sie an einer benennbaren Quelle aus 02 Ressourcen geerdet
      Und ich erkenne die Quellnotiz im Verlauf wieder

    Szenario: Bewegung im Lösungsraum nach dem Tetralemma
      Gegeben die Freigabe des Lösungsraums
      Wenn wir an der Lösung arbeiten
      Dann bewegen wir uns sichtbar entlang der fünf Positionen
      Und kippen nicht vorschnell ins Entweder-oder

    Szenario: Kritik bleibt freimütig und wohlwollend
      Gegeben eine Kritik eines Experten
      Wenn er eine Position des anderen oder von mir angreift
      Dann tut er das mit fairer Stärken- und Schwächendarstellung
      Und nicht als Strohmann

    Szenario: Anschlussfähigkeit vor Abschluss
      Gegeben eine erarbeitete Lösung
      Wenn wir abschließen wollen
      Dann prüfen wir ausdrücklich, ob die Lösung in meiner Praxis andocken kann

    Szenario: Retrospektive nach jeder Session
      Gegeben eine abgeschlossene Session
      Wenn die Session endet
      Dann läuft eine Retrospektive an
      Und sie prüft jedes Akzeptanzkriterium dieser Session
      Und sie hält Reibung und Erkenntnisse im Lerntagebuch fest

    Szenario: Verbesserung wird vorgeschlagen, nicht stillschweigend angewandt
      Gegeben Verbesserungsvorschläge aus der Retrospektive
      Wenn sie das Playbook verändern würden
      Dann legt der Lern-Agent sie mir zur Freigabe vor
      Und ändert das Playbook erst nach meiner Bestätigung

    Szenario: Verbesserung wird gemessen, nicht behauptet
      Gegeben eine freigegebene Verbesserung aus der Vorwoche
      Wenn die nächste Session läuft
      Dann prüft die Retrospektive, ob sich die betroffenen Akzeptanzkriterien verbessert haben
      Und rollt die Änderung zurück, wenn sie verschlechtert hat

**Out of Scope:**
- Das knowledge-storm-Programm von der Stange, also Artikelgenerator, automatische Mindmap, unbeaufsichtigter Vielrundenlauf
- Indexierung des gesamten Vaults, indiziert wird nur 02 Ressourcen, ohne `PDS/` und `99_Personen/`
- Vertrauliches Stakeholder-Material
- Stillschweigendes Selbst-Umschreiben des Playbooks ohne Freigabe und ohne Rückrollmöglichkeit

---

## E — Entities (Domänenmodell)

**Kernentitäten:**
| Entität | Beschreibung | Beziehungen |
|---------|-------------|-------------|
| Moderator | Führt den Prozess, rahmt die zwei Experten je Problem, hält die Schwelle, pflegt die lebende Karte, löst nicht selbst | steuert Experten und Phasen |
| Experte A / Experte B | Zwei Perspektiven, vom Moderator je Problem frisch gerahmt, problem- und lösungsraumfähig | erden sich am Korpus |
| Nutzer | Dritte Stimme am Tisch, bringt Problem und Praxis ein | gleichberechtigt im Diskurs |
| Lebende Karte | Inhaltlicher Arbeitszustand im Kartograf-Schema, liefert das Schwellenkriterium | gehört zum Problem |
| Lern-Agent (Retrospektive) | Reflektiert nach jeder Session den Prozess, misst gegen die Szenarien, schlägt Verbesserungen vor, pflegt das Lerntagebuch | verbessert das Playbook |
| Lerntagebuch | Dauerhaftes Lern-Artefakt im PDS-Lerntagebuch-Format, ein Eintrag je Session | Quelle für die nächste Session |
| Playbook (versioniert) | Die Beschreibung der Moderation, über Git versioniert, damit Verbesserungen rückrollbar sind | wird vom Lern-Agenten verbessert |
| Korpus 02 Ressourcen | 281 Notizen, wissenschaftliche Grundlagen | Erdungsquelle der Experten |

**Bestehende Entitäten (aus Vault und Konfiguration):**
- PDS-Agenten (Orchestrator, Rahmensetzer, Annahmen-Archäologe, Gegenmodell, Strategieprüfer, Schauseite, Kartograf): Vorlagen für Haltung und Rollen
- Kartograf-Schema und PDS-Lerntagebuch: Vorlagen für die lebende Karte und das Lerntagebuch
- `## Bezug` plus WikiLinks: bestehender Kopplungsmechanismus

---

## A — Approach (Lösungsansatz)

**Gewählte Strategie:**
Der runde Tisch wird als Moderation innerhalb unserer Sitzung gebaut, das Sprachmodell bin ich als Claude Code, nicht das knowledge-storm-Programm. Haltungen und Rollen kommen als Vorlage aus dem PDS-Stapel. Die zwei Experten sind nicht fest, der Moderator rahmt ihre Perspektiven je Problem frisch. Gestaffelt in zwei Stufen. Stufe A ist der Diskurs-Harness mit Lernschleife, zunächst geerdet über mein direktes Lesen. Stufe B legt einen lokalen Vektorindex über 02 Ressourcen darunter und hebt die Erdung auf semantische Suche.

Die Lernschleife folgt deiner Harness-Logik, also test- und szenariengetrieben mit zwei Sensortypen. Der berechnende, verlässliche Sensor ist die Prüfung jedes Akzeptanzkriteriums nach der Session. Der KI-Sensor ist die qualitative Einschätzung des Lern-Agenten, also ein Hinweis, kein Beweis. Verbesserungen sind Vorschläge, die du freigibst, das Playbook ist versioniert, und eine Änderung gilt erst als gut, wenn die nächste Session sie an den Szenarien bestätigt. So bleibt die Initiative beim System und das Urteil bei dir.

**Alternativen (verworfen):**
- Stock Co-STORM: baut einen Artikel, externalisiert das Verstehen, over-engineered
- Reine Canvas-Variante ohne Vektor: schwächere Erdung, deshalb der Vektor in Stufe B
- Externer Pipeline-LLM: unnötige Vertraulichkeitsfläche, das Modell ist diese Sitzung
- Autonomes Selbst-Umschreiben des Playbooks: Driftgefahr ohne Anker, deshalb Freigabe, Versionierung und Messung gegen die Szenarien

**Abhängigkeiten:**
- Stufe A: keine neuen, nur Lesezugriff auf den Korpus und Git für die Playbook-Versionierung
- Stufe B: lokales Einbettungsmodell und lokaler Vektorspeicher (Vorschlag sentence-transformers plus Chroma, lokal)

---

## S — Structure (Systemstruktur)

**Betroffene Komponenten:**
- PDS-Prompts als Vorlage (nur lesen)
- Korpus `/Users/d0e02236/Documents/Notes/Work/02 Ressourcen` als Erdungsquelle

**Neue Dateien:**
- `~/agent-sandbox/runder-tisch/`: Projektordner unter Git, Geschwister zu szenarien-pruefer
- `REASONS.md`, `szenarien.md`: dieses Blueprint und die Szenarien
- `playbook.md`: die Moderation, skill-fähig strukturiert, damit ein Skill `/runder-tisch` später leicht nachgezogen werden kann, über Git versioniert
- `retrospektive.md`: Vorlage und Ablauf der Retrospektive
- Lerntagebuch als Notiz im PDS-Lerntagebuch-Format
- Lebende Karte als Arbeitsnotiz im Vault im Kartograf-Format (Ablageort im jeweiligen Themenkreis)
- Stufe B: `index_bauen` und eine Such-Schnittstelle, der Index liegt außerhalb des Vaults

**Integration:**
Die Moderation übernimmt PDS-Haltungen, Karte und Lerntagebuch nutzen bestehende PDS-Formate, die Erdung verweist auf Vault-Notizen über deren Titel. Das Playbook ist so geschrieben, dass es ohne Umbau zu einem Skill wird.

---

## O — Operations (Konkrete Umsetzungsschritte)

### Stufe A — Diskurs-Harness mit Lernschleife (ohne Vektor)

1. **Projekt anlegen** — Ordner, REASONS.md, szenarien.md. Test: Dateien existieren. *(erledigt)*
2. **Moderator-Charta und Experten-Rahmung** — Moderator-Haltung aus der Orchestrator-Vorlage, Logik zum Rahmen der zwei Experten je Problem, Schwellen- und Freigabe-Logik. Test: Charta benennt, wann der Lösungsraum freigegeben wird.
3. **Problemraum-Phase** — Methoden der Experten (zirkuläres Fragen, Annahmen-Archäologie), Moderator pflegt die Karte, Schwellenkriterium aus der Karte. Test: Szenarien Problemraum und Freigabe.
4. **Lösungsraum-Phase** — Tetralemma als Struktur, Gegenmodell als Reibfläche, Diskursethik. Test: Szenarien Tetralemma und Kritik.
5. **Anschlussfähigkeits-Check** — Abschlusskriterium im Luhmann'schen Sinn. Test: Szenario Anschlussfähigkeit.
6. **Lernschleife** — Retrospektive-Ablauf, Lerntagebuch-Format, Prüfung jedes Szenarios, Verbesserungsvorschläge zur Freigabe, Versionierung des Playbooks über Git, Lese-Regel für die nächste Session. Test: Szenarien Retrospektive, Vorschlag-statt-Anwendung, Messung-statt-Behauptung.
7. **Trockenlauf an einem kleinen Testproblem** — ganzer Tisch inklusive Retrospektive, Erdung über direktes Lesen. Test: alle Szenarien laufen durch.

**Git-Checkpoint nach:** Operation 7 — Tisch und Lernschleife funktionieren ohne Vektor

### Stufe B — Semantische Erdung

8. **Index bauen** — lokales Einbettungsmodell und Speicher, Index über 02 Ressourcen, ohne `PDS/` und `99_Personen/`. Test: Testfrage liefert sinnvolle Treffer mit Quellpfad.
9. **Such-Schnittstelle** — lokale Suche, die ich im Tisch aufrufe. Test: Aufruf liefert Treffer und Quellnotiz.
10. **Erdung umstellen** — von direktem Lesen auf semantische Suche. Test: Szenario Geerdeter Beitrag über die Suche.
11. **Trockenlauf mit Vektor-Erdung** — gleicher Tisch, semantisch geerdet, Vergleich. Test: Erdung spürbar breiter.

**Git-Checkpoint nach:** Operation 11 — semantische Erdung steht

---

## N — Norms (Querschnittliche Standards)

- **Sprache:** Deutsch, Begriffe ausschreiben statt Kürzel
- **Karte und Lerntagebuch:** bestehende PDS-Formate, keine Sektion weglassen
- **Kopplung:** `## Bezug` plus WikiLinks wie in PDS
- **Erdung:** jeder fachliche Beitrag mit benennbarer Quelle
- **Git:** eine logische Änderung, ein Commit, deutsche Nachricht, Dateien einzeln stagen, das Playbook immer als eigener Commit, damit Verbesserungen rückrollbar sind
- **Wiederverwendung:** PDS-Muster übernehmen statt Paralleles bauen

---

## S — Safeguards (Nicht verhandelbare Grenzen)

**Invarianten:**
- Kein Lösungsraum vor der Freigabe durch die Schwelle
- Jeder Expertenbeitrag ist geerdet
- Keine Playbook-Änderung ohne deine Freigabe

**Lernschleife:**
- „Besser" wird an den Szenarien gemessen, nicht behauptet
- Das Playbook ist versioniert, jede Verbesserung ist einzeln rückrollbar
- Verschlechtert eine freigegebene Änderung die betroffenen Szenarien, wird sie zurückgerollt

**Vertraulichkeit:**
- Das Sprachmodell ist diese Sitzung, kein externer Pipeline-LLM
- Einbettung und Index laufen lokal, der Index liegt außerhalb des Vaults
- Korpus ist nur 02 Ressourcen, ohne `PDS/` und `99_Personen/`
- Der Vault wird nicht verändert

**Performance:**
- 281 Notizen, ein lokaler Index ist trivial

**Rollback-Kriterium:**
- Stufe B ist additiv, bei Problemen bleibt Stufe A mit direktem Lesen voll funktionsfähig
- Eine schädliche Playbook-Verbesserung wird auf die letzte gute Version zurückgesetzt

**Offene Entscheidung [?]:**
- Autonomiegrad des Lern-Agenten, Vorschlag mit Freigabe durch dich, alternativ selbst anwenden und nur melden
