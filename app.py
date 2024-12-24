from flask import Flask, request, render_template
import requests

app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json() 
        image_url = pokemon_data["sprites"]["front_default"]
        return {"weight": pokemon_data["weight"], "image_url": image_url}
    else:
        return None
    

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    pokemon_info = None  
    image_url = None
    
    if request.method == 'POST':
        strength = request.form.get('strength')
        pokemon_name = request.form.get('pokemon_name').lower()

        if not strength.isdigit():
            result = "Error: The bench weight must be an integer. \nPlease enter a valid number."
        else:
            pokemon_info = get_pokemon_info(pokemon_name)

            if pokemon_info:
                image_url = pokemon_info["image_url"]
                if int(strength) > int(pokemon_info["weight"]):
                    result = f"Congrats! You are strong enough! \n{pokemon_name} weighs {pokemon_info['weight']} pounds \nwhile you bench {strength} pounds."
                else:
                    result = f"Sorry, you are not strong enough.\n{pokemon_name} weighs {pokemon_info['weight']} pounds \nwhile you only bench {strength} pounds."
            else:
                result = f"{pokemon_name} doesn't exist, check spelling and try again."

    return render_template('index.html', result=result, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
