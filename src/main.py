import os
import shutil

from copystatic import copy_files_recursive
from markdown_blocks import markdown_to_html_node


dir_path_static = "./static"
dir_path_public = "./public"


def extract_title(markdown):
    lines = markdown.split("\n")
    title_line = lines[0]
    if title_line.startswith("# "):
        return title_line[2:]   
    else:
        raise ValueError("Title not found in markdown")

def write_page(dest_path, content):
    # Also checks if directory exists otherwise create it etc
    print(f"Writing page to {dest_path}")
    # chgeck if directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(content)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page {from_path} -> {dest_path}, Using template {template_path}")
    markdown = open(from_path).read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = open(template_path).read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    write_page(dest_path, template)
    
def generate_pages_recursive(from_dir, template_path, to_dir):
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                # if from_path has a directory we need to structure it the same way in the public directory
                dest_path = from_path.replace(from_dir, to_dir)[:-3] + ".html"
                generate_page(from_path, template_path, dest_path)

   
def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    generate_pages_recursive("./content", "./template.html", "./public")


main()