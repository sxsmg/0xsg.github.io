import os
import markdown
import yaml
import sys

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split the file into front matter and content
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"Error: Invalid format in {file_path}. Make sure there's front matter separated by '---'.")
            return None, None
        
        front_matter = yaml.safe_load(parts[1])
        markdown_content = parts[2]
        
        return front_matter, markdown_content
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None, None

def convert_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)

def generate_html_post(template_path, markdown_path, output_path):
    try:
        # Read the template
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
        
        # Read and convert the markdown file
        front_matter, markdown_content = read_markdown_file(markdown_path)
        if front_matter is None or markdown_content is None:
            return False
        
        html_content = convert_markdown_to_html(markdown_content)
        
        # Replace placeholders in the template
        html_post = template.replace('{{TITLE}}', front_matter.get('title', 'Untitled'))
        html_post = html_post.replace('{{DATE}}', front_matter.get('date', 'Undated'))
        html_post = html_post.replace('{{CONTENT}}', html_content)
        
        # Write the generated HTML to a file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_post)
        
        return True
    except Exception as e:
        print(f"Error generating HTML for {markdown_path}: {str(e)}")
        return False

def main():
    template_path = 'post_template.html'
    markdown_dir = 'posts'
    output_dir = 'posts'
    
    if not os.path.exists(template_path):
        print(f"Error: Template file {template_path} not found.")
        sys.exit(1)
    
    if not os.path.exists(markdown_dir):
        print(f"Error: Markdown directory {markdown_dir} not found.")
        sys.exit(1)
    
    success_count = 0
    failure_count = 0
    
    for filename in os.listdir(markdown_dir):
        if filename.endswith('.md'):
            markdown_path = os.path.join(markdown_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.md', '.html'))
            if generate_html_post(template_path, markdown_path, output_path):
                print(f'Generated: {output_path}')
                success_count += 1
            else:
                print(f'Failed to generate: {output_path}')
                failure_count += 1
    
    print(f"\nSummary: {success_count} file(s) generated successfully, {failure_count} file(s) failed.")

if __name__ == '__main__':
    main()