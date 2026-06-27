# Retrospektive und Lernschleife

> Stand 2026-06-27. Fester Bestandteil des runden Tisches.

## Wann

Nach jeder abgeschlossenen Session, als fester Schlussschritt, nicht optional.

## Zwei Sensoren

- Berechnender Sensor, verlässlich. Jedes Szenario aus szenarien.md wird geprüft, hält oder hält nicht, mit kurzer Begründung am Sessionverlauf.
- KI-Sensor, Hinweis. Die qualitative Einschätzung, wo es gehakt hat, wo die Erdung dünn war, wo die Schwelle zu früh oder zu spät kam. Ein Hinweis, kein Beweis.

## Lerntagebuch

Ein Eintrag je Session, im PDS-Lerntagebuch-Format. Festgehalten werden, welche Szenarien hielten und welche nicht, Reibung und Erkenntnisse, und ob die freigegebene Verbesserung der Vorsession gewirkt hat.

## Verbesserungsvorschläge

- konkret und an ein Szenario gebunden, nicht allgemein,
- als Vorschlag formuliert, nicht angewandt,
- mit der erwarteten Wirkung auf das betroffene Szenario.

## Freigabe und Anwendung

Der Lern-Agent legt die Vorschläge dem Nutzer vor. Erst nach Freigabe ändert er das Playbook, und zwar als eigener Git-Commit. Ohne Freigabe bleibt das Playbook unverändert. Autonomiegrad im Standard, Vorschlag mit Freigabe durch den Nutzer.

## Messung und Rollback

Die nächste Session liest die zuletzt freigegebenen Verbesserungen und wendet sie an. In ihrer Retrospektive wird geprüft, ob sich die betroffenen Szenarien verbessert haben. Hat eine Änderung verschlechtert, wird sie auf die letzte gute Playbook-Version zurückgerollt.

## Maß für „besser"

Die Szenarien halten, plus das Urteil des Nutzers zur Anschlussfähigkeit. Erweiterbar, zum Beispiel um die Häufigkeit, mit der die Schwelle zu früh geöffnet wurde.
