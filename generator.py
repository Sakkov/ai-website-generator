import openai
import sys
import requests
import os
import random
import time

# Variables
try:
    api_key, title, header_prompt, description_prompt, website_type, image_prompt, style, language = sys.argv[1:]
except ValueError:
    print("Usage: python generator.py [api_key] [title] [header_prompt] [meta_description_prompt] [website_type] [image_prompt] [style] [language]")
    sys.exit(1)

openai.api_key = api_key


# Read URLs from file
print("Reading URLs from file...")
urls = []
with open("website_urls.txt", "r", encoding="UTF-8") as file:
    lines = file.readlines()
    for line in lines:
        try:
            url, url_text , description = line.strip().split(";")
        except ValueError:
            url = line
            description = ""
        urls.append({"url": url, "text": url_text, "description": description})
print(f"URLs: {urls}\n\n")

# Use OpenAI API to generate header and paragraph
print("Generating header...")
header = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"""Generate a header for a website using the following as contexts: "{header_prompt}" language: {language}""",
    temperature=0.8,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0.05,
    presence_penalty=0.3
).choices[0].text
print(f"Generated header: {header}\n\n")

# Use OpenAI API to generate meta description and paragraph
print("Generating meta description...")
description = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"""Generate meta description for a {website_type} website using the following context: "{description_prompt}" language: {language}""",
    temperature=0.8,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0.05,
    presence_penalty=0.3
).choices[0].text
print(f"Generated meta description: {description}\n\n")

# Generate prompts for each URL
print("Generating prompts for each URL...")
paragraph_prompts = []
for url_dict in urls:
    url = url_dict["url"]
    url_description = url_dict["description"]
    url_text = url_dict["text"]
    paragraph_prompts.append({"url": url, 
                                "prompt": f"""Generate few lengthy {website_type} website paragraphs with using the following as context "{url_description}" 
                                Use the URL: {url} in html a tags in the paragraph like this "<a href="https://{url}">{url_text}</a>". 
                                Use the {language} language."""})
print(f"Generated prompts for each URL.\n\n")

# Use OpenAI API to generate paragraphs
print("Generating paragraphs...")
generated_paragraphs = []
for paragraph in paragraph_prompts:
    generated_paragraph = openai.Completion.create(
        engine="text-davinci-003",
        prompt=paragraph["prompt"],
        temperature=0.8,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.05,
        presence_penalty=0.3
    ).choices[0].text
    generated_paragraphs.append(f"<p>{generated_paragraph}</p>")
# Format paragraphs into HTML
paragraphs_html = f""" {''.join(generated_paragraphs)} """
print(f"Generated paragraphs: {generated_paragraphs}\n\n")

# Generate header image using DALL·E
print("Generating header image...")
header_image_prompt = f"{image_prompt} DARK COLORS!"
header_image_response = openai.Image.create(
    prompt=header_image_prompt,
    n=1,
    size="1024x1024"
)
header_image_url = header_image_response["data"][0]["url"]
print(f"Generated header image: {header_image_url}\n\n")

# Create directory and image file
print("Creating directory and image file...")
newpath = f"{title}"
if not os.path.exists(newpath):
    os.makedirs(newpath)

with open(f"{title}/header_image.jpg", "wb") as file:
    file.write(requests.get(header_image_url).content)
print(f"Created directory and image file.\n\n")


# HTML
print("Generating HTML, CSS and JavaScrip...")
html = f"""
<!DOCTYPE html>
<html lang="{language[:2].lower()}">
<html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header class="header_text" style="background-image: url(header_image.jpg);">
            <h1>{header}</h1>
    </header>
    <nav>
        <ul>
            <li><a class="active" href="#">Home</a></li>
            <li><a href="#">News</a></li>
            <li><a href="#">Contact</a></li>
            <li><a href="#">About</a></li>
        </ul>
    </nav>
    <main>
      {paragraphs_html}
    </main>
    <footer>
        <p>© {title} {time.strftime("%Y")} | <a href="#">Privacy Policy</a></p>
    <script src="script.js"></script>
  </body>
</html>
"""

# CSS
if style == "modern":
    css = """
    * {
        box-sizing: border-box;
        font-family: Roboto, sans-serif;
        font-size: 20px;
    }
    

    nav ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #261919;
    }

    nav li {
        float: left;
    }

    nav li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }

    nav li a:hover:not(.active) {
        background-color: #111;
    }

    nav .active {
        background-color: #73b5f5;
    }

    body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
    }
    
    header {
        text-align: center;
        background-color: #333;
        color: white;
    }

    .header_text {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        margin: 0;
        padding: 20vh 1vw;
    }

    .header_text h1 {
        font-size: 42px;
    }
      
    main {
        padding: 2em;
    }

    p {
        max-width: 1000px;
        font-size: 1.2em;
        padding: 10vh 5vw;
        background-color: #fff;
        margin: 10vh auto;
    }
    """
elif style == "classic":
    css = """
    * {
    box-sizinepeat: no-repeat;
        background-size: cover;
    }

    nav ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #8B2500;
    }

    nav li {
        float: left;
    }

    nav li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }

    nav li a:hover:not(.active) {
        background-color: #4A1A1A;
    }

    nav .active {
        background-color: #B22222;
    }

    body {
        font-family: Times New Roman, serif;
        background-color: #F5DEB3;
    }

    header {
        text-align: center;
        background-color: #CD5C5C;
        color: white;
        background-position: center;
        background-r
        padding: 20vh 1vw;
        margin: 0;g: border-box;
        font-family: Georgia, serif;
        font-size: 18px;
    }

    .header_text h1 {
        font-size: 36px;
    }

    main {
        padding: 2em;
    }

    p {
        max-width: 800px;
        font-size: 1.1em;
        padding: 10vh 5vw;
        background-color: #FFF8DC;
        margin: 10vh auto;
    }
    """
elif style == "random":
    inspirations = ["Hyer", 
                    "Mubasic", 
                    "Digital Cover", 
                    "IBM’s The Harmonic State", 
                    "Superlist", 
                    "Swab the World", 
                    "Newest Americans", 
                    "Spotify Design", 
                    "Andy Warhol", 
                    "Human Interaction Company", 
                    "Garoa Skincare", 
                    "1917: In the Trenches", 
                    "Image Source", 
                    "The Octopus: A design blog by IDEO", 
                    "Nomadic Tribe", 
                    "Image Source", 
                    "Diana Danieli", 
                    "George Nakashima Woodworkers", 
                    "crypton.trading", 
                    "Southwest: Heart of Travel", 
                    "Overflow", 
                    "Frans Hals Museum", 
                    "Simply Chocolate", 
                    "NOWNESS", 
                    "Rainforest Guardians", 
                    "Protest Sportswear", 
                    "The Teacher's Guild", 
                    "Virgin America", 
                    "Feed", 
                    "ETQ", 
                    "Mikiya Kobayashi", 
                    "Woven Magazine", 
                    "JOHO's Bean", 
                    "World of SWISS", 
                    "Guillaume Tomasi", 
                    "The District", 
                    "Tej Chauhan", 
                    "Amanda Martocchio Architecture"]
    inspiration = random.choice(inspirations)
    print(f"Your inspiration is {inspiration}!")
    css = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""Experimental, complex, unconventional, innovative css style file. "{inspiration}" website as inspiration. 
                    Huge paddings and margins. Readable, vibrant and high contrast text.  html structure: 
                    <body>
                    <header class="header_text" style="background-image: url(header_image.jpg);">
                            <h1>{header}</h1>
                    </header>
                    <nav>
                        <ul>
                            <li><a class="active" href="#">Home</a></li>
                            <li><a href="#">News</a></li>
                            <li><a href="#">Contact</a></li>
                            <li><a href="#">About</a></li>
                        </ul>
                    </nav>
                    <main>
                        (paragraphs_html)
                    </main>
                    <footer>
                        <p>© {title} {time.strftime("%Y")} | <a href="#">Privacy Policy</a></p>
                    <script src="script.js"></script>
                    </body>
                """,
        temperature=0.5,
        max_tokens=2048,
        top_p=0.8,
    ).choices[0].text

else:
    css = """
    * {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    font-size: 18px;
    }

    body {
    background-color: #f2f2f2;
    }

    header {
    text-align: center;
    background-color: #4285f4;
    color: white;
    padding: 1em;
    }

    header h1 {
    font-size: 36px;
    margin: 0;
    }

    nav {
    background-color: #fff;
    display: flex;
    justify-content: center;
    }

    nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    }

    nav li {
    margin: 0 10px;
    }

    nav a {
    color: #333;
    text-decoration: none;
    font-size: 18px;
    padding: 10px;
    }

    nav a:hover {
    background-color: #ddd;
    }

    main {
    padding: 2em;
    }

    p {
    max-width: 800px;
    font-size: 1.1em;
    padding: 10vh 5vw;
    background-color: #fff;
    margin: 10vh auto;
    }

    """

# JavaScript
javascript = """
console.log("Welcome to my website!");
"""
print(f"Generated HTML, CSS and JavaScript.\n\n")


# Write HTML, CSS, and JavaScript to files
print("Writing HTML, CSS, and JavaScript to files...")
# Write HTML to file
with open(f"{title}/index.html", "w", encoding="UTF-8") as file:
    file.write(html)

# Write CSS to file
with open(f"{title}/style.css", "w", encoding="UTF-8") as file:
    file.write(css)

# Write JavaScript to file
with open(f"{title}/script.js", "w", encoding="UTF-8") as file:
    file.write(javascript)
print(f"Wrote HTML, CSS, and JavaScript to files.\n\n")