from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json() 
        return pokemon_data
    else:
        return None
    

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    pokemon_info = None  
    
    if request.method == 'POST':
        strength = request.form.get('strength')
        pokemon_name = request.form.get('pokemon_name').lower()


        if not strength.isdigit():
            result = "Error: The bench weight must be an integer. \nPlease enter a valid number."
        else:
            pokemon_info = get_pokemon_info(pokemon_name)

            if pokemon_info:
                if int(strength) > int(pokemon_info["weight"]):
                    result = f"Congrats! You are strong enough! \n{pokemon_name} weighs {pokemon_info['weight']} pounds \nwhile you bench {strength} pounds."
                else:
                    result = f"Sorry, you are not strong enough.\n{pokemon_name} weighs {pokemon_info['weight']} pounds \nwhile you only bench {strength} pounds."
            else:
                result = f"{pokemon_name} doesnt exist, check spelling and try again."

    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <title>PokéBench</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
        <link href="https://fonts.cdnfonts.com/css/pokemon-solid" rel="stylesheet">
        <style>
        @import url('https://fonts.cdnfonts.com/css/pokemon-solid');
        </style>
        <style> 
        @import url('https://fonts.googleapis.com/css?family=Press+Start+2P');
        </style>
    </head>
    <body>
        <h1>PokéBench</h1>
        <form method="post">
            <label>How much do you bench? (in pounds):</label><br>
            <input type="text" name="strength"><br><br>
            <label>Choose a Pokémon:</label><br>
            <input type="text" name="pokemon_name"><br><br>
            <input type="submit" value="Submit">
        </form>
        <div class="response-container">
            <p style="white-space: pre-line;">{{ result }}</p>
        </div>
    </body>
    </html>
''', result=result)




if __name__ == '__main__':
    app.run(debug=True)