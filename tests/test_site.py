"""Dependency-free tests for the public directory. Run: python3 -m unittest discover -s tests -v"""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
INVENTORY = json.loads((ROOT / "data" / "link-inventory.json").read_text(encoding="utf-8"))
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
FULL = (ROOT / "llms-full.txt").read_text(encoding="utf-8")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.meta = []
        self.articles = 0
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "a":
            self.links.append(data)
        elif tag == "meta":
            self.meta.append(data)
        elif tag == "article":
            self.articles += 1

class DirectoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = LinkParser()
        cls.html.feed(HTML)
        cls.hrefs = [x["href"] for x in cls.html.links if "href" in x]

    def test_every_project_has_human_readable_html_and_source_link(self):
        self.assertEqual(len(INVENTORY["projects"]), 23)
        self.assertEqual(self.html.articles, 23)
        for project in INVENTORY["projects"]:
            self.assertIn('id="' + project["id"] + '"', HTML)
            self.assertIn(project["repository"], self.hrefs)
            self.assertIn(project["name"], HTML)

    def test_every_source_sitemap_url_is_present_in_html_and_full_index(self):
        links = [url for source in INVENTORY["sitemaps"] for url in source["urls"]]
        self.assertEqual(len(links), 177)
        self.assertEqual(len(set(links)), len(links))
        self.assertEqual(len({p["repository"] for p in INVENTORY["projects"]}), 23)
        for url in links:
            self.assertIn(url, self.hrefs, url)
            self.assertIn(url, FULL, url)
        for p in INVENTORY["projects"]:
            self.assertIn(p["repository"], FULL)
            self.assertIn(p["repository"], LLMS)
        self.assertEqual(len(set(links) | {p["repository"] for p in INVENTORY["projects"]}), 200)

    def test_followable_non_redirecting_index(self):
        self.assertNotIn('http-equiv="refresh"', HTML.lower())
        self.assertNotIn("window.location", HTML.lower())
        self.assertNotIn("nofollow", HTML.lower())
        self.assertIn('rel="canonical" href="https://pro-genai.github.io/"', HTML)
        self.assertTrue(any(m.get("name") == "robots" and "index,follow" in m.get("content", "") for m in self.html.meta))
        self.assertNotIn("prane-eth.github.io", HTML)

    def test_local_sitemap_is_not_external_url_directory(self):
        root = ElementTree.parse(ROOT / "sitemap.xml").getroot()
        locations = [n.text for n in root.iter() if n.tag.endswith("}loc")]
        self.assertEqual(locations, ["https://pro-genai.github.io/"])
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Allow: /", robots)
        self.assertIn("https://pro-genai.github.io/sitemap.xml", robots)

    def test_structured_data_is_parsable_and_matches_projects(self):
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)
        self.assertIsNotNone(m)
        schema = json.loads(m.group(1))
        listing = next(x for x in schema["@graph"] if x["@type"] == "ItemList")
        self.assertEqual(listing["numberOfItems"], 23)
        self.assertEqual([x["item"]["url"] for x in listing["itemListElement"]], [p["repository"] for p in INVENTORY["projects"]])

if __name__ == "__main__":
    unittest.main()
