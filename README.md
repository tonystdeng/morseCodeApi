# Morse Code Api
## Description
This project is a simple API that gives users Morse Code translation.
## Usage
### GET requests
You can request translation data in json dictionary format by endpoint `api/<orientation>/<specification>`.

Orientation endpoints avalible:

- `c2m` for character to morse code.
- `m2c` for morse code to character.

Specification endpoints available:

- None for a full dictionary
- `alpha` for a dictionary that only contains alphabetical characters.
- `numeric` for a dictionary that only contains numeric characters.
- `symbol` for a dictionary that only contains symbol characters.
- `char` for live translation, requires parameter `key`, user should input a character/morse code based on the orientation. e.g.`api/c2m/char?key="a"`(results in morse code for "a")
### POST requests
You have the power to add translation to our database, and we will appreciate your support!

POST to endpoint `api/c2m` for character to morse code in formate `{char0: morse_code0, char1: morse_cose1, ...}`.

or POST to endpoint `api/m2c` for morse code to character in formate `{morse_code0: char0, morse_cose1: char1, ...}`.

<!--npx github-readme-to-html -s "dark" -t "API description" -d "templates"-->