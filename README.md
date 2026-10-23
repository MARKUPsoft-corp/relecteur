# 🤖 Relecteur Git Automatique (Git-Watch)

> **Revue de code IA autonome et collaborative pour équipes de développement.**  
> *GitHub Copilot CLI · cron · Telegram · Architecture Zero Trust*  
> Présenté aux **GitHub Dev Days** par **Emmanuel YAKAM TCHAMEGNI** *(Cryptographe · Co-fondateur de FYS)*.

[![GitHub](https://img.shields.io/badge/GitHub-MARKUPsoft--corp%2Frelecteur-blue?logo=github)](https://github.com/MARKUPsoft-corp/relecteur)
[![Linux](https://img.shields.io/badge/OS-Linux%20%7C%20WSL2-orange?logo=linux)](https://ubuntu.com)
[![Copilot](https://img.shields.io/badge/AI-GitHub%20Copilot%20CLI-success?logo=githubcopilot)](https://github.com/features/copilot)
[![Telegram](https://img.shields.io/badge/Alerts-Telegram%20Bot-blue?logo=telegram)](https://telegram.org)
[![Security](https://img.shields.io/badge/Security-Zero%20Trust%20%7C%20Client--side%20DLP-red)](https://github.com)

---

## 📌 Qu'est-ce que ce projet ?

**Git-Watch** est un agent de revue de code autonome qui surveille les commits poussés sur un dépôt Git (local ou distant sur GitHub). Dès qu'un collaborateur pousse du code :

1. Il intercepte le nouveau commit en quelques millisecondes.
2. Il applique un **caviardage local des secrets** (`redact.sh`) avant toute émission vers le réseau.
3. Il confie le diff à **GitHub Copilot CLI**, confiné dans un **bac à sable vide et privé de tout outil système** (`--deny-tool='shell' --deny-tool='write'`).
4. Il génère un rapport technique senior (explication détaillée, cas limites, failles de sécurité, cohérence du commit, message conventionnel suggéré).
5. Il notifie instantanément l'ensemble de l'équipe sur leur **groupe Telegram** avec l'identité de l'auteur, la branche, les fichiers touchés et l'analyse complète.

---

## ⚡ Installation Express en 1 ligne (Recommandé)

Sur votre machine de travail ou sur un serveur Linux (Ubuntu 22.04+, Debian ou WSL2) :

```bash
curl -fsSL https://raw.githubusercontent.com/MARKUPsoft-corp/relecteur/main/install.sh | bash
```

L'assistant interactif coloré se charge de tout : vérification des paquets, configuration sécurisée, détection de vos groupes Telegram et planification cron.

---

## 📖 Guide de A à Z : Préparer vos accès avant l'installation

Pour qu'une équipe puisse déployer le relecteur sur son groupe Telegram et son dépôt Git, voici comment obtenir chacune des informations demandées.

---

### 1. Accès GitHub Copilot

Le relecteur a besoin d'interroger le moteur GitHub Copilot. Deux options s'offrent à vous :

* **Option 1 (Le plus simple sur PC de dev) : Connexion Web existante**  
  Si vous avez déjà installé Copilot CLI (`npm install -g @github/copilot`), tapez simplement `copilot` dans votre terminal et suivez la validation dans votre navigateur. L'installateur détectera automatiquement votre session.
* **Option 2 (Idéal pour serveur / machine d'équipe) : Fine-grained PAT**  
  1. Rendez-vous sur votre profil GitHub : **Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** $\rightarrow$ **Fine-grained tokens**.
  2. Cliquez sur **Generate new token**.
  3. Nom : `git-watch`. Expiration : 30 jours (recommandé).
  4. Dans **Permissions**, cochez uniquement **Copilot Requests** (aucun droit sur vos dépôts n'est nécessaire !).
  5. Copiez la valeur générée (`github_pat_...`).

---

### 2. Créer son Bot Telegram (en 1 minute)

Chaque équipe peut créer son propre bot Telegram gratuitement via le bot officiel de Telegram :

1. Ouvrez Telegram sur votre téléphone ou ordinateur et cherchez **`@BotFather`** (le compte officiel avec la coche bleue).
2. Envoyez la commande :
   ```text
   /newbot
   ```
3. **Nom d'affichage du bot :** Entrez par exemple `Relecteur Équipe Dev`.
4. **Nom d'utilisateur unique :** Entrez un identifiant finissant obligatoirement par `bot` (ex: `mon_equipe_gitwatch_bot`).
5. **BotFather vous donne immédiatement votre Jeton d'API (Token) :**
   ```text
   Use this token to access the HTTP API:
   8832084068:AAEcjeCUuzVbsaHt51WeXcyYBW89OY3lxYo
   ```
   👉 *Conservez ce jeton secret, c'est ce que l'installateur vous demandera.*

---

### 3. Créer le Groupe Telegram de l'Équipe & y ajouter le Bot

1. Dans Telegram, créez un nouveau groupe (ex: **« Équipe Dev — Alertes Commits »**) et invitez vos collègues.
2. Ajoutez votre bot (`@mon_equipe_gitwatch_bot`) comme membre du groupe, exactement comme s'il s'agissait d'un contact humain.
3. **Autoriser le bot dans le groupe :**
   * Donnez les droits d'administration au bot dans le groupe (ou assurez-vous qu'il peut lire les messages).
   * Envoyez un premier message dans le groupe (par exemple tapez `/start` ou `bonjour`).  
   *(Cette étape est indispensable : elle crée la file d'attente permettant à l'installateur de détecter le groupe).*

---

### 4. Comment obtenir l'ID du Groupe Telegram (`chat_id`) ?

Deux méthodes au choix :

#### Méthode 1 : Automatique via notre installateur (Magique 🪄)
Notre script `install.sh` interroge directement l'API Telegram. Dès que vous avez envoyé un message dans votre groupe, l'installateur affiche automatiquement :
```text
Conversations & Groupes Telegram récents détectés :
  [1] 👥 Équipe Dev — Alertes Commits (supergroup) — ID : -1002345678901
  [2] 👤 Emmanuel (private) — ID : 5940820241
Choisissez le numéro du groupe à notifier : 1
```
Vous tapez juste **`1`** et c'est configuré !

#### Méthode 2 : Manuelle (si besoin)
* Invitez le bot d'aide **`@RawDataBot`** ou **`@userinfobot`** dans votre groupe : il affichera instantanément un pavé JSON contenant `"chat": { "id": -100xxxxxxxxxx }`.
* Copiez ce nombre (avec le tiret `-`) puis retirez le bot d'aide.
* *Note : Les identifiants de groupes Telegram commencent toujours par un nombre négatif (ex: `-100...`).*

---

### 5. L'URL du Dépôt Git à surveiller

* L'URL HTTPS ou SSH de votre dépôt GitHub (ex: `https://github.com/MARKUPsoft-corp/relecteur.git`).
* L'installateur le clonera automatiquement dans `~/lab/` et suivra la branche de votre choix (par défaut `main`).

---

## 🏗️ Architecture et Fonctionnement sous le capot

```
 ┌──────────────────────┐
 │ Dépôt GitHub distant │
 └──────────┬───────────┘
            │ git fetch origin (chaque minute par cron)
 ┌──────────▼───────────┐
 │     git-watch.sh     │ ──> Verrou flock anti-collision
 └──────────┬───────────┘ ──> Détection de nouveaux commits
            │
 ┌──────────▼───────────┐
 │      redact.sh       │ ──> Caviardage local des clés AWS, tokens, SSH
 └──────────┬───────────┘
            │ Données assainies entre balises <diff>
 ┌──────────▼───────────┐
 │  GitHub Copilot CLI  │ ──> Exécution dans sandbox/ vide
 └──────────┬───────────┘ ──> --deny-tool='shell' --deny-tool='write'
            │ Rapport Markdown produit
 ┌──────────▼───────────┐
 │    Groupe Telegram   │ ──> Notification d'équipe instantanée sur smartphone !
 └──────────────────────┘
```

---

## 🔒 Principes de Sécurité fondamentaux (Zero Trust)

1. **L'IA n'a aucun pouvoir :** Copilot CLI est invoqué avec `--deny-tool='shell' --deny-tool='write' --deny-tool='url'`. Même en cas d'injection de prompt hostile dans le commit, l'IA ne peut ni exécuter de commande, ni altérer de fichier.
2. **Exécution en bac à sable :** L'appel est confiné dans `~/lab/sandbox/` (un dossier vide), empêchant l'accès au code environnant.
3. **Caviardage côté client (Client-side DLP) :** Le script `redact.sh` masque les clés sensibles **avant** qu'elles ne soient envoyées à l'API.
4. **Secret sans trace :** Le jeton Telegram est injecté via l'entrée standard de `curl` (`curl -K -`), masquant ainsi le token dans la table des processus (`ps aux` / `/proc`).

---

## 🛠️ Commandes Utiles au Quotidien

* **Consulter les rapports générés :**
  ```bash
  ls -la ~/lab/reports/
  cat ~/lab/reports/commit-xxxx.md
  ```
* **Voir le journal d'activité de cron :**
  ```bash
  tail -f ~/lab/reports/cron.log
  ```
* **Forcer une vérification immédiate sans attendre cron :**
  ```bash
  ~/lab/bin/git-watch.sh
  ```
* **Modifier la configuration (Token, Chat ID) :**
  ```bash
  nano ~/.config/ai-report/env
  ```
* **Arrêter temporairement la surveillance :**
  ```bash
  crontab -e   # commentez la ligne avec un '#'
  ```

---

## 👥 Auteur & Remerciements

* **Emmanuel YAKAM TCHAMEGNI** — Cryptographe, Co-fondateur de **FYS** *(Find Your Security)*.
* Projet développé pour les **GitHub Dev Days**.
* Licence : MIT.
