# Szenarien — Runder Tisch zur gemeinsamen Problemlösung

> Diese Datei gehört dir. Du kannst Szenarien jederzeit ergänzen, ändern oder löschen.
> Stand: 2026-06-27, Entwurf, noch nicht bestätigt.

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

    Szenario: Ordner-Wahl ist Pflicht
      Gegeben ein Start von /runder-tisch, /frag oder /index-aktualisieren
      Wenn der Korpus-Ordner nicht eindeutig benannt ist
      Dann wird kein Standard-Ordner angenommen
      Und der Nutzer wird nach dem Ordner gefragt, bevor irgendetwas läuft

    Szenario: Runder Tisch auf beliebigem Ordner
      Gegeben ein Ordner mit Markdown-Notizen im Dateisystem
      Wenn ich /runder-tisch mit diesem Ordner starte
      Dann baut oder aktualisiert der Skill den Index für genau diesen Ordner
      Und die Erdung der Experten nutzt nur Quellen aus diesem Ordner

    Szenario: Bestehender Index bleibt erhalten
      Gegeben der vorhandene Index über den Arbeits-Vault
      Wenn ein Index für einen zweiten Ordner gebaut wird
      Dann bleibt der erste Index unverändert nutzbar

    Szenario: Vorführung startet ohne Wartezeit
      Gegeben der vorab gebaute Index über den Test-Vault
      Wenn die Vorführung beginnt
      Dann liefert die erste Suchanfrage sofort Treffer
