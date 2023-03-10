# AI Website Generator

This is a small project to create websites easily using the power of OpenAi's API. To run this you have install the openai python package.

# Installation

```console
pip install openai
git clone https://github.com/Sakkov/ai-website-generator.git
```

# Usage

```console
python generator.py [api_key] [title] [header_prompt] [meta_description_prompt] [website_type] [image_prompt] [style] [language]
```

Example:
```console
python generator.py API_KEY "example" "Example by AI website generator" "An example website made by an AI website generator developed by Saku Kovanen" "Educational" "AI robot making a website" random English
```
You can find the website made with this call in the example directory in this project.

## [api_key]
You can get your api_key from OpenAi's website https://platform.openai.com/account/api-keys.

Example: "fu-Tm90IGEgcmVhbCBhcGkga2V5IGhhaGEgNDIgNjkgcGkgPSA0"

## [title]
This variable sets the title of the website. and the directory that will be created by running the code.

Example: "Saku Kovanen", "YouTube", "Fiksukuljetus | Muutot Pirkanmaalla"

## [header_prompt]
This variable is used in the prompt to generate the header.

Examples: "Poliisi: kuljettaja ei halunnut asioida poliisin kanssa", "Searching factual information is more difficult than ever before"

## [meta_description_prompt]
This variable is used in the prompt to generate the meta description.

Examples: "Experiment with DALL·E, an AI system by OpenAI", "This search engine helps you turn information into action, making it faster and easier to go from searching to doing."

## [website_type]
This variable is used in generating the meta description and the paragraphs.

Examples: "Social media", "Search engine"

## [image_prompt]
This variable is used as the prompt to generate the background image of the header element.

Examples: "a pencil and watercolor drawing of a bright city in the future with flying cars", "photograph of an astronaut riding a horse"

## [Style]
This variable is used to define the CSS style.

Style options are:
 - modern 
 - classic 
 - random
 - default

The option "random" will use OpenAI api to generate a new CSS stylesheet with some inspiration from random selected website from a list "37 of the Best Website Designs to Inspire You in 2022" published at https://blog.hubspot.com/marketing/best-website-designs-list

## [Language]
This variable defines the language used on the website.

Examples: "Finnish", "English"

# URLs
You can specify the urls you want to use and the display text for the url in the "website_urls.txt" file. Use multiple lines for multiple paragraphs. The format you need to use in the file:
```console
[url];[display_text];[paragraph_prompt]
```

Example:
```console
sakukovanen.fi;Saku Kovanen;2nd year Aalto University student and part-time entrepreneur.
kovanen.io;kovanen.io;kovanen.io - NOT A TAXI SERVICE This site is for testing purposes.
kovanen.io/recommendation;Recommendation application;The tool is a simple media recommendation tool.
random-bible.kovanen.io;Random Bible;The tool gives you a random verse from the Bible.
github.com/Sakkov;Sakkov Github;👋 Hi, I’m @Sakkov 🎓 I study Digital Systems and Design as my major in Aalto University
www.google.com;Göögel;The Reddit and Twitter communities had contrasting views on the reasons behind Google's perceived shortcomings.
```

# About examples
The example named "example" is the first example which was made with the first published version (Alpha 1.0) of this program. The example named "example2" was made using the version (Alpha 1.1 22.02.2023)