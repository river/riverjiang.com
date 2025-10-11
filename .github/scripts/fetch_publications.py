import requests

def fetch_publications():
    """Fetch publications from PubMed and generate markdown"""
    
    # Search PubMed
    query = "River Jiang[Author]"
    esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&sort=pub+date"
    
    esearch_response = requests.get(esearch_url)
    esearch_response.raise_for_status()
    esearch_data = esearch_response.json()
    
    ids = esearch_data['esearchresult']['idlist']
    
    if not ids:
        print("No publications found.")
        return []
    
    # Fetch summaries
    summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
    summary_response = requests.get(summary_url)
    summary_response.raise_for_status()
    summary_data = summary_response.json()
    
    # Parse publications
    publications = []
    for item in summary_data['result'].values():
        if 'uid' not in item:
            continue
            
        title = item.get('title', 'No title available')
        authors = ', '.join([author['name'] for author in item.get('authors', [])])
        journal = item.get('source', 'N/A')
        pubdate = item.get('pubdate', 'N/A')
        year = pubdate[:4] if pubdate != 'N/A' else 'N/A'
        uid = item['uid']
        
        # Parse date for sorting
        sortdate = item.get('sortpubdate', item.get('pubdate', ''))
        
        publications.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year,
            'pubdate': pubdate,
            'sortdate': sortdate,
            'uid': uid,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{uid}"
        })
    
    # Sort by date (most recent first)
    publications.sort(key=lambda x: x['sortdate'], reverse=True)
    
    return publications

def generate_markdown(publications):
    """Generate markdown for publications page"""

    # Start with frontmatter
    md = """---
title: "Publications"
author_profile: true
---

"""

    if not publications:
        md += "\nNo publications found.\n"
        return md

    # Add publications as ordered list
    for i, pub in enumerate(publications, 1):
        # Bold "Jiang R" in author list
        authors = pub['authors'].replace('Jiang R', '**Jiang R**')

        md += f"{i}. {pub['title']} {authors}. *{pub['journal']}*. {pub['year']}. [PMID {pub['uid']}]({pub['url']})\n\n"

    return md

def main():
    print("Fetching publications from PubMed...")
    publications = fetch_publications()
    print(f"Found {len(publications)} publications")
    
    # Generate markdown
    markdown = generate_markdown(publications)
    
    # Save to file
    with open('_pages/publications.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print("Publications page updated successfully!")

if __name__ == "__main__":
    main()