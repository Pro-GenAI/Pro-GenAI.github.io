# Praneeth Vadlapati — GitHub Pages resource directory

A standalone, indexable, static directory at **https://pro-genai.github.io/** linking to public Pro-GenAI GitHub projects and documentation pages. The previous redirect to a personal website has been removed. This site serves resource discovery and attribution rather than copying or republishing project content.

## Scope (snapshot 2026-11-20)

- **23** public repository links from the [main showcase data](https://github.com/Pro-GenAI/pro-genai.com/blob/main/projects.js).
- **177** unique website URLs from four upstream XML sitemaps: Agent-RT (**29**), Agent Action Guard (**9**), ReaTerm (**1**), and Awesome Checklists (**138**). The latter includes one repeated `AGENTS.html` URL; it is listed once.
- **200** distinct external destinations in total. All appear in semantic HTML lists on `index.html`, beneath each project name and short description. Links use ordinary `<a href="...">` elements without `nofollow`.
- `data/link-inventory.json` stores the exact source snapshots and the project list; each sitemap has a source path, source blob SHA, and ordered de-duplicated URLs.

## SEO and AEO implementation

- **Indexable HTML:** no JavaScript redirect, no meta refresh, self-referencing canonical, robots index/follow, descriptive HTML headings/anchors, and text accessible without JavaScript.
- **Crawler discovery:** `robots.txt` allows access and references the local `sitemap.xml`. The local sitemap lists **only the page hosted here**. External URLs are not inserted into this site's sitemap because this site does not host them.
- **Structured data:** JSON-LD Organization, WebSite, CollectionPage, and ItemList with 23 repository records; all entries correspond to visible content.
- **Social previews:** Open Graph and Twitter summary metadata, plus a responsive and keyboard-accessible page.
- **LLM-oriented retrieval:** `llms.txt` contains a concise project index; `llms-full.txt` includes all 200 external resource URLs and descriptions, matching the HTML.
- **Editorial quality:** factual descriptions from the main curated catalog, visible source references, a short FAQ, and explicit caveats for research prototypes. Avoid keyword stuffing, synthetic links, guaranteed ranking claims, or ungrounded FAQ rich-result claims.

The `llms.txt` convention is optional and **does not guarantee AI answer inclusion, search ranking, crawling, or backlink value**. Followable HTML links allow crawlers to discover destinations; search engines decide whether any signals are counted.

## Run and verify

No runtime dependencies. To preview: `python3 -m http.server 8000`, then visit `http://localhost:8000`.

Run dependency-free tests:

```bash
python3 -m unittest discover -s tests -v
```

Also inspect the published site, check responsive layout, follow links, and validate the deployed GitHub Pages URL. The tests verify snapshot coverage and formatting but do not prove that every external destination currently returns HTTP 200.

## Source sitemap files

- [Agent-RT](https://github.com/Pro-GenAI/Agent-RT/blob/main/docs/website/sitemap.xml) — 29 distinct URLs (source blob `e737005a37ec18be020976875f5f816f9eb5f802`).
- [Agent-Action-Guard](https://github.com/Pro-GenAI/Agent-Action-Guard/blob/main/docs/website/sitemap.xml) — 9 distinct URLs (source blob `e10fbfa3fd15515951705fd5f30efba5ac4edae3`).
- [ReaTerm](https://github.com/Pro-GenAI/ReaTerm/blob/main/docs/website/sitemap.xml) — 1 distinct URLs (source blob `8103687dc1b79087f3e626d644a0409212c76c4f`).
- [awesome-checklists](https://github.com/Pro-GenAI/awesome-checklists/blob/main/docs/website/sitemap.xml) — 138 distinct URLs (source blob `4fa5f886b234191c4fc0072e62d71fd338f5479b`).

## Updating the inventory

1. Fetch the public project records from `Pro-GenAI/pro-genai.com/projects.js` and the four upstream XML sitemaps above.
2. Update `data/link-inventory.json`, then regenerate the corresponding project cards and links in `index.html` and `llms-full.txt`; keep `llms.txt` concise.
3. Deduplicate only exact repeat URLs, preserve path case/trailing slashes, and never invent missing destinations.
4. Run the tests and inspect the page. Refresh the snapshot date only when the links have been rechecked.
5. After deployment, verify indexability and optionally submit `https://pro-genai.github.io/sitemap.xml` through your own verified Google Search Console or Bing Webmaster Tools property. These external console steps require site ownership verification; no such verification is assumed here.

The repository is intentionally static: no client-side GitHub API, external analytics, third-party assets, generated doorway pages, or secret configuration.
