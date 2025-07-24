#!/usr/bin/env python3
"""
Repository File Concatenator
Recursively scans a repository and concatenates all files with metadata
for easy AI context sharing.
"""

import os
import argparse
from pathlib import Path
import mimetypes
from datetime import datetime

# File extensions to include (text-based files)
TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.sass',
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.md', '.txt', '.rst', '.tex', '.csv', '.sql', '.sh', '.bash', '.zsh',
    '.ps1', '.bat', '.cmd', '.dockerfile', '.gitignore', '.gitattributes',
    '.env', '.example', '.sample', '.template', '.makefile', '.cmake',
    '.c', '.cpp', '.h', '.hpp', '.cs', '.java', '.php', '.rb', '.go',
    '.rs', '.swift', '.kt', '.scala', '.clj', '.hs', '.ml', '.r', '.m',
    '.vim', '.lua', '.pl', '.tcl', '.awk', '.sed', '.grep'
}

# Directories to ignore
IGNORE_DIRS = {
    '.git', '.svn', '.hg', '__pycache__', 'node_modules', '.venv', 'venv',
    'env', '.env', 'dist', 'build', '.next', '.nuxt', 'target', 'bin',
    'obj', '.vs', '.vscode', '.idea', '*.egg-info', '.pytest_cache',
    '.coverage', '.nyc_output', 'coverage', '.DS_Store', 'Thumbs.db'
}

# Files to ignore
IGNORE_FILES = {
    '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.pyd', '*.class',
    '*.o', '*.so', '*.dylib', '*.dll', '*.exe', '*.log', '*.tmp',
    '*.temp', '*.bak', '*.backup', '*.swp', '*.swo', '*~'
}

def is_text_file(file_path):
    """Check if a file is likely a text file based on extension and mimetype."""
    # Check extension first
    if file_path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    
    # Check if it has no extension but might be a text file
    if not file_path.suffix:
        try:
            # Try to detect mimetype
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type and mime_type.startswith('text/'):
                return True
            
            # For files without extension, try reading first few bytes
            with open(file_path, 'rb') as f:
                sample = f.read(1024)
                # Check if it's mostly text (allow some binary chars)
                try:
                    sample.decode('utf-8')
                    return True
                except UnicodeDecodeError:
                    return False
        except:
            return False
    
    return False

def should_ignore_path(path, ignore_dirs, ignore_files):
    """Check if a path should be ignored."""
    path_name = path.name.lower()
    
    # Check if it's an ignored directory
    if path.is_dir() and path_name in ignore_dirs:
        return True
    
    # Check if it's an ignored file
    if path.is_file() and path_name in ignore_files:
        return True
    
    return False

def get_file_summary(file_path):
    """Generate a brief summary of the file based on its name and location."""
    relative_path = file_path
    parts = relative_path.parts
    
    # Extract meaningful information from path
    summary_parts = []
    
    # Add directory context
    if len(parts) > 1:
        dir_context = " / ".join(parts[:-1])
        summary_parts.append(f"Location: {dir_context}")
    
    # Add file type information
    if file_path.suffix:
        summary_parts.append(f"Type: {file_path.suffix[1:]} file")
    
    # Add special file recognition
    filename = file_path.name.lower()
    if filename in ['readme.md', 'readme.txt', 'readme']:
        summary_parts.append("Purpose: Documentation/README")
    elif filename in ['package.json', 'requirements.txt', 'pyproject.toml', 'cargo.toml']:
        summary_parts.append("Purpose: Package/Dependencies configuration")
    elif filename in ['dockerfile', 'docker-compose.yml']:
        summary_parts.append("Purpose: Container configuration")
    elif filename.startswith('.'):
        summary_parts.append("Purpose: Configuration/Hidden file")
    elif 'test' in filename or 'spec' in filename:
        summary_parts.append("Purpose: Test file")
    elif 'config' in filename or 'settings' in filename:
        summary_parts.append("Purpose: Configuration file")
    
    return " | ".join(summary_parts) if summary_parts else "Regular file"

def read_file_content(file_path):
    """Safely read file content with encoding detection."""
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            return f"[ERROR: Could not read file - {str(e)}]"
    
    return "[ERROR: Could not decode file with any supported encoding]"

def concatenate_repository(repo_path, output_file=None, max_file_size=50000):
    """Main function to concatenate all repository files."""
    repo_path = Path(repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path '{repo_path}' does not exist.")
        return
    
    if not repo_path.is_dir():
        print(f"Error: '{repo_path}' is not a directory.")
        return
    
    # Determine output file
    if output_file is None:
        output_file = repo_path / "concatenated_repo.txt"
    else:
        output_file = Path(output_file)
    
    print(f"Scanning repository: {repo_path}")
    print(f"Output file: {output_file}")
    
    files_processed = 0
    files_skipped = 0
    total_size = 0
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # Write header
        out_f.write(f"REPOSITORY CONCATENATION\n")
        out_f.write(f"========================\n")
        out_f.write(f"Repository: {repo_path}\n")
        out_f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_f.write(f"Max file size limit: {max_file_size:,} characters\n\n")
        
        # Recursively walk through all files
        for file_path in sorted(repo_path.rglob('*')):
            # Skip if path should be ignored
            relative_path = file_path.relative_to(repo_path)
            
            # Check if any part of the path should be ignored
            should_skip = False
            for part in relative_path.parts:
                if part.lower() in IGNORE_DIRS or part.lower() in IGNORE_FILES:
                    should_skip = True
                    break
            
            if should_skip:
                continue
            
            # Only process files
            if not file_path.is_file():
                continue
            
            # Only process text files
            if not is_text_file(file_path):
                files_skipped += 1
                continue
            
            try:
                # Get relative path for display
                relative_path = file_path.relative_to(repo_path)
                
                # Read file content
                content = read_file_content(file_path)
                
                # Check file size
                if len(content) > max_file_size:
                    content = content[:max_file_size] + f"\n\n[TRUNCATED - File too large, showing first {max_file_size:,} characters]"
                
                # Generate summary
                summary = get_file_summary(relative_path)
                
                # Write file section
                out_f.write("=" * 80 + "\n")
                out_f.write(f"FILE: {relative_path}\n")
                out_f.write(f"SUMMARY: {summary}\n")
                out_f.write("=" * 80 + "\n\n")
                out_f.write(content)
                out_f.write("\n\n")
                
                files_processed += 1
                total_size += len(content)
                
                # Progress indicator
                if files_processed % 10 == 0:
                    print(f"Processed {files_processed} files...")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                files_skipped += 1
        
        # Write footer
        out_f.write("=" * 80 + "\n")
        out_f.write("CONCATENATION COMPLETE\n")
        out_f.write("=" * 80 + "\n")
        out_f.write(f"Files processed: {files_processed}\n")
        out_f.write(f"Files skipped: {files_skipped}\n")
        out_f.write(f"Total content size: {total_size:,} characters\n")
    
    print(f"\nConcatenation complete!")
    print(f"Files processed: {files_processed}")
    print(f"Files skipped: {files_skipped}")
    print(f"Output saved to: {output_file}")
    print(f"Total size: {total_size:,} characters")

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate all text files in a repository for AI context sharing"
    )
    parser.add_argument(
        "repo_path", 
        help="Path to the repository directory"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file path (default: auto-generated in repo directory)"
    )
    parser.add_argument(
        "--max-size", 
        type=int, 
        default=50000,
        help="Maximum file size in characters before truncation (default: 50000)"
    )
    
    args = parser.parse_args()
    
    concatenate_repository(args.repo_path, args.output, args.max_size)

if __name__ == "__main__":
    main()