# GeoDesk — Frontend (SIH26013)

Frontend dashboard for **SIH26013: Automated Integration and Intelligent
Harmonization of Multi-source Geospatial Data for Urban Land Record
Management**.

This is your (Bavadharani's) part of the team project: the web dashboard
that will eventually sit on top of the backend + GIS harmonization
pipeline your teammates are building.

## What's in here

- **React 18 + Vite** — fast dev server, simple build
- **React Router** — page navigation
- **Tailwind CSS** — styling, using a custom "surveyor's ledger" theme
  (navy ink, brass/gold "seal" accents for verified data, teal for
  harmonized status, contour-line texture)
- **react-leaflet** — interactive map showing land parcels
- **recharts** — charts on the overview dashboard

## Pages

| Route         | What it shows                                              |
|---------------|-------------------------------------------------------------|
| `/`           | Overview — key stats, map preview, conflict chart, activity feed |
| `/map`        | Full map explorer with status filters                      |
| `/sources`    | Connected data sources table + a drag-and-drop upload zone  |
| `/records`    | Searchable table of harmonized land parcels                 |
| `/conflicts`  | List of parcels where sources disagree, with review actions |

## Running it locally

```bash
npm install
npm run dev
```

Then open the URL Vite prints (usually `http://localhost:5173`).

To build for production:

```bash
npm run build
npm run preview
```

## Important: this currently uses MOCK DATA

All the data on these pages comes from `src/data/mockData.js`. There is
no backend connected yet. When your teammates' API is ready:

1. Open `src/data/mockData.js`.
2. Replace the exported constants with `fetch()` calls to the real API
   (or create a small `src/api/` folder with functions like
   `getDataSources()`, `getLandRecords()`, etc., and call those from the
   pages instead of importing the mock arrays directly).
3. The component code in `src/pages/` and `src/components/` shouldn't
   need to change much — they just expect the same shape of data
   (see the objects in `mockData.js` for the exact fields each page
   expects, e.g. a parcel needs `id`, `village`, `surveyNo`, `owner`,
   `status`, `lat`, `lng`, etc.).

## Pushing this to your team's repository

Since you're extracting this from a zip:

```bash
# from inside the extracted folder
git init                                   # only if this repo isn't already a git repo
git remote add origin <your-team-repo-url> # skip if remote already exists
git add .
git commit -m "Add frontend dashboard for SIH26013"
git branch -M main                         # or whatever branch your team uses
git push -u origin main
```

If your team already has a repo with other people's code in it, it's
usually safer to:

```bash
git clone <your-team-repo-url>
# copy the contents of this extracted folder into the cloned repo
# (merge carefully if there's already a frontend folder)
cd <cloned-repo-folder>
git checkout -b frontend-dashboard
git add .
git commit -m "Add frontend dashboard for SIH26013"
git push -u origin frontend-dashboard
# then open a pull request into main
```

Ask your teammates which of these two flows matches how your repo is
set up before pushing.

## Project structure

```
src/
  components/     Reusable UI pieces (Sidebar, Topbar, ParcelMap, StatCard, StatusBadge)
  pages/          One file per route (Overview, MapExplorer, DataSources, LandRecords, Conflicts)
  data/           mockData.js — swap this for real API calls later
  App.jsx         Routes
  main.jsx        App entry point
  index.css       Tailwind + global styles
```
