# Diagrammes swimlane — flux métier agentique bâtiment

## Statut

**Proposition UX / produit à intégrer aux flux métier de l'app.**

Ces diagrammes servent à visualiser les responsabilités entre l'utilisateur, l'interface, l'IA, le backend, la base de données et les rôles de validation.

---

## 1. Swimlane générique — voix → action métier → confirmation → DB

```mermaid
flowchart LR
  subgraph U[Utilisateur métier]
    U1[Parle / dicte une demande]
    U2[Relit la proposition]
    U3{Confirme ?}
    U4[Demande correction / clarification]
  end

  subgraph UI[Interface app]
    UI1[Capture voix / texte / photo]
    UI2[Affiche transcription]
    UI3[Affiche action proposée]
    UI4[Affiche succès / erreur réelle]
  end

  subgraph AI[IA agentique]
    AI1[Transcrit / comprend l'intention]
    AI2[Résout entités: client, chantier, tâche]
    AI3[Prépare action structurée]
    AI4[Demande clarification si doute]
  end

  subgraph API[Backend / policy engine]
    API1[Vérifie identité + rôle]
    API2[Vérifie organisation / tenant]
    API3[Vérifie champs autorisés]
    API4[Exécute mutation si confirmé]
    API5[Journalise audit trail]
  end

  subgraph DB[Base de données]
    DB1[(Clients / Contacts / Projets)]
    DB2[(Tâches / Notes / Documents)]
    DB3[(Audit logs)]
  end

  U1 --> UI1 --> AI1 --> AI2 --> AI3 --> API1 --> API2 --> API3 --> UI3 --> U2 --> U3
  U3 -- Non --> U4 --> AI4 --> UI3
  U3 -- Oui --> API4 --> DB1
  API4 --> DB2
  API4 --> API5 --> DB3
  DB1 --> UI4
  DB2 --> UI4
```

### Règle produit associée

- L'IA propose, mais n'exécute pas une action sensible sans confirmation.
- Le backend vérifie toujours identité, rôle, organisation et champs autorisés.
- L'UI n'affiche jamais un succès si la DB n'a pas réellement été modifiée.

---

## 2. Swimlane — réunion / discussion chantier enregistrée → transcription → compte-rendu validé

```mermaid
flowchart LR
  subgraph P[Participants réunion / chantier]
    P1[Participants informés]
    P2[Consentement donné]
    P3[Discussion chantier]
  end

  subgraph U[Utilisateur app]
    U1[Clique: démarrer enregistrement]
    U2[Arrête l'enregistrement]
    U3[Relit transcription + résumé]
    U4{Valide le compte-rendu ?}
    U5[Corrige / supprime passages]
  end

  subgraph UI[Interface app]
    UI1[Affiche écran consentement]
    UI2[Badge: enregistrement en cours]
    UI3[Affiche transcription]
    UI4[Affiche tâches / décisions proposées]
  end

  subgraph VOICE[Voix / transcription]
    V1[Capture audio temporaire]
    V2[Transcription Deepgram / fallback]
    V3[Suppression audio temporaire selon politique]
  end

  subgraph AI[IA métier]
    AI1[Résumé]
    AI2[Décisions]
    AI3[Tâches / réserves / points bloquants]
    AI4[Clarification si ambigu]
  end

  subgraph API[Backend / droits]
    API1[Vérifie rôle utilisateur]
    API2[Vérifie projet / organisation]
    API3[Stocke transcription validée]
    API4[Crée tâches seulement après validation]
    API5[Audit: qui a enregistré, validé, modifié]
  end

  subgraph DB[Stockage]
    DB1[(Transcriptions)]
    DB2[(Comptes-rendus)]
    DB3[(Tâches / réserves)]
    DB4[(Audit logs)]
  end

  U1 --> UI1 --> P1 --> P2 --> UI2 --> V1 --> P3 --> U2 --> V2 --> UI3 --> U3
  UI3 --> AI1 --> AI2 --> AI3 --> UI4 --> U4
  U4 -- Non --> U5 --> AI4 --> UI3
  U4 -- Oui --> API1 --> API2 --> API3 --> DB1
  API3 --> DB2
  API4 --> DB3
  API5 --> DB4
  V2 --> V3
```

### Règle produit associée

- L'enregistrement doit être visible et annoncé.
- La transcription peut être automatique.
- Les tâches, décisions et réserves ne deviennent officielles qu'après validation humaine.
- L'audio ne doit pas être conservé durablement sans décision explicite.

---

## 3. Swimlane — annulation / restauration avec droits officiels V1

```mermaid
flowchart LR
  subgraph U[Utilisateur]
    U1[Demande annulation / suppression]
    U2[Confirme action sensible]
    U3[Demande restauration]
  end

  subgraph UI[Interface]
    UI1[Affiche impact de l'annulation]
    UI2[Demande confirmation]
    UI3[Affiche statut annulé / restauré]
  end

  subgraph AUTH[Droits officiels V1]
    A1[Vérifie rôle: platform_admin / owner / org_admin / manager / finance]
    A2[Vérifie périmètre: org / projet / objet propre]
    A3{Autorisé ?}
  end

  subgraph API[Backend]
    API1[Soft-delete: deleted_at / cancelled / archived]
    API2[Journalise annulation]
    API3[Restore si rôle autorisé]
    API4[Journalise restauration]
  end

  subgraph DB[DB]
    DB1[(Objet métier)]
    DB2[(Audit logs)]
  end

  U1 --> UI1 --> UI2 --> U2 --> A1 --> A2 --> A3
  A3 -- Non --> UI3
  A3 -- Oui --> API1 --> DB1
  API1 --> API2 --> DB2 --> UI3
  U3 --> A1 --> A2 --> A3
  A3 -- Oui restauration --> API3 --> DB1
  API3 --> API4 --> DB2 --> UI3
```

### Règle produit associée

- Par défaut, on ne détruit pas définitivement: on applique un soft-delete.
- Toute annulation/restauration est journalisée.
- La restauration dépend du domaine: projet, terrain, documents, finance.
