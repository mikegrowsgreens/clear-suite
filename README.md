# Clear Suite - Recovery Trackers

Free, private, clinically-sourced recovery tracking PWAs. No accounts, no servers, no tracking. Everything stays on the user's device.

## Apps

| App | Substance | Health Categories | Live |
|-----|-----------|-------------------|------|
| **Clear Mind** | Cannabis | ECS Recovery, Cognitive, Sleep, Mood, Respiratory, Appetite | [clearmind.mikegrowsgreens.com](https://clearmind.mikegrowsgreens.com) |
| **Clear Air** | Nicotine/Vaping | Cardiovascular, Respiratory, Senses, Blood, Nicotine, Immune | [clearair.mikegrowsgreens.com](https://clearair.mikegrowsgreens.com) |
| **Clear Path** | Alcohol | Liver, Cognitive, Cardiovascular, Sleep, Digestive, Immune | [clearpath.mikegrowsgreens.com](https://clearpath.mikegrowsgreens.com) |

## Architecture

Each app is a single-file React PWA (~70KB) served by Caddy on Railway. Zero backend dependencies.

- **Single HTML file** with inline React, CSS, and all logic
- **Clinically weighted scoring** - milestones sourced from peer-reviewed research, weighted by clinical significance
- **Front-loaded recovery curves** - most progress visible in the first weeks when motivation matters most
- **Full PWA support** - installable, works offline, service worker caching
- **100% client-side** - localStorage only, no network requests after initial load
- **4-4-6 breathing exercise** - built-in craving intervention tool
- **Craving logging** with trigger categorization and outcome tracking

## Deployment

Each app deploys as an independent Railway service using the Caddy Docker image.

```
apps/
  clearpath/     -> clearpath.yourdomain.com
  clearmind/     -> clearmind.yourdomain.com
  clearair/      -> clearair.yourdomain.com
  landing/       -> clearsuite.yourdomain.com
```

### Deploy to Railway

1. Push this repo to GitHub
2. Create a new Railway project
3. Add a service for each app (connect GitHub repo, set root directory)
4. Generate domains or add custom domains
5. Each service auto-builds from its Dockerfile

### Environment

No environment variables needed. No secrets. No API keys. Each service is a static file server.

## Tech Stack

- React 19 (CDN, no build step)
- Caddy web server (Alpine Docker)
- Railway (deployment platform)
- localStorage (client-side persistence)

## Clinical Sources

- Cleveland Clinic, American Liver Foundation (alcohol/liver timelines)
- American Heart Association (cardiovascular recovery)
- Journal of Hepatology (liver regeneration research)
- NIDA (substance dependence and recovery milestones)
- Recovery Village (withdrawal and detox timelines)
- PMC/PubMed peer-reviewed studies (ECS, nicotine, cognitive recovery)

## License

MIT
