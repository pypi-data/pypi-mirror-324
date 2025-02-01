import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# URLs to download
DOCS_URLS = [
    "https://docs.astral.sh/uv/guides/projects/#running-commands",
    "https://docs.astral.sh/uv/guides/publish/"
]

def create_output_directory():
    """Create the output directory if it doesn't exist."""
    output_dir = Path("./references/uv")
    print(f"Creating directory: {output_dir.absolute()}")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def clean_text(text):
    """Clean up the text by removing extra whitespace and empty lines."""
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line and not line.startswith('Table of contents')]
    return '\n\n'.join(lines)

def download_and_convert(url, output_dir):
    """Download the documentation page and convert it to text."""
    print(f"\nProcessing URL: {url}")
    try:
        print("Downloading content...")
        response = requests.get(url)
        response.raise_for_status()
        
        print("Parsing HTML...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove navigation and table of contents
        for nav in soup.find_all(['nav', 'aside']):
            nav.decompose()
        
        print("Extracting main content...")
        # Try to find the most specific content container
        content = (
            soup.find('article', class_='md-content__inner') or  # Main content in MkDocs
            soup.find('div', class_='md-content') or            # Content wrapper in MkDocs
            soup.find('main') or                                # Generic main content
            soup.find('article') or                             # Generic article
            soup.find('body')                                   # Fallback to body
        )
        
        if content:
            print("Content found, processing text...")
            # Remove code blocks temporarily to preserve their formatting
            code_blocks = []
            for pre in content.find_all('pre'):
                code_blocks.append(pre.get_text())
                pre.replace_with('CODE_BLOCK_PLACEHOLDER')
            
            text = content.get_text(separator='\n', strip=True)
            text = clean_text(text)
            
            # Restore code blocks
            for code_block in code_blocks:
                text = text.replace('CODE_BLOCK_PLACEHOLDER', f'\n\n```\n{code_block}\n```\n\n', 1)
            
            filename = url.split('/')[-1].replace('#', '_').replace('-', '_') + '.txt'
            if filename == '.txt':
                filename = url.split('/')[-2] + '.txt'
            
            output_file = output_dir / filename
            print(f"Saving to: {output_file}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n\n")
                f.write(text)
            
            print(f"Successfully saved: {output_file}")
        else:
            print(f"ERROR: Could not find main content in: {url}")
            
    except Exception as e:
        print(f"ERROR processing {url}: {str(e)}")
        raise  # Re-raise the exception for debugging

def main():
    print("Starting documentation download...")
    output_dir = create_output_directory()
    for url in DOCS_URLS:
        download_and_convert(url, output_dir)
    print("\nProcess completed!")

if __name__ == "__main__":
    main() 