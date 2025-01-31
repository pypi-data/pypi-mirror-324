import markdown
import imgkit
import os
import threading

from markdown_to_png.tool import progress_bar


def markdown_to_png(markdown_path, output_path, css_path='template/style.css'):
    """ converts a markdown(.md) file to a styled png image.

        :param markdown_path: Path to the Markdownfile
        :param output_path: Output path for the PNG file
        :param css_path: Path to the CSS file for styling
    """

    if not markdown_path.endswith('.md'):
        markdown_path += '.md'
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    # convert paths to absolute
    html_path = 'template/temp.html'

    # check if `template` directory is exists, if it doesn't exists then make the directory
    if "template" not in os.listdir():
        os.mkdir("template")

    html_file_path = os.path.abspath(html_path)
    css_file_path = os.path.abspath(css_path)

    # read the markdown file
    with open(f'{markdown_path}', 'r') as f:
        text = f.read()

    # convert markdown to HTML
    html = markdown.markdown(text)


    # write the css dynamically
    with open(css_file_path, 'w') as css_file:
        css_file.write(f"""* {{
    font-family: Vazirmatn;
}}
    """)

    # save html to a file
    with open(html_path, 'w') as html_file:
        html_file.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{output_path}</title>
    <link rel="stylesheet" href="{css_file_path}" type="text/css">
    <!-- Include Vazirmatn from Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>\n
""")
        html_file.write(html)
        html_file.write("\n\n</body>\n</html>")

    # convert HTML to PNG
    options = {
        'format': 'png',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
    }

    print("Starting conversion...")
    estimated_duration = 5

    # start the progress bar in a separate thread
    progress_thread = threading.Thread(target=progress_bar, args=(50, estimated_duration))
    progress_thread.start()

    # perform the conversion
    try:
        imgkit.from_file(html_path, f'{output_path}.png', options=options, css=css_path)
    finally:
        progress_thread.join()  # wait for the progress bar to complete
        print("\nConversion Complete!")
