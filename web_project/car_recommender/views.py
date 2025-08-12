from django.shortcuts import render
from . import forms

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import requests
import random

# Returns a request for the home page
def home(request):
      return render(request, "index.html")

# Returns a request for the standard recommender
def standard(request):
    
    # When a request is received, collect the information from the form
    if request.method == "POST" and "run_standard_recommender":
        standard_recommender = forms.StandardRecommender(request.POST, request.FILES)

        # Validate results and place the clean data into the recommendation system
        if standard_recommender.is_valid():
            results, ds_response = run_standard_model(standard_recommender.cleaned_data)

        # Post results to the front-end
        return render(request, "standard-recommender.html", {"standard_recommender": standard_recommender, "standard_results": results, "ds_response": ds_response})

    # If no request is received, show the empty form
    else:
        standard_recommender = forms.StandardRecommender()
        return render(request, "standard-recommender.html", {"standard_recommender": standard_recommender})

# Returns a request for the simple recommender
def simple(request):

    # When a request is received, collect the information from the form
    if request.method == "POST" and "run_simple_recommender":
        simple_recommender = forms.SimpleRecommender(request.POST, request.FILES)
        
        # Validate results and place the clean data into the recommendation system
        if simple_recommender.is_valid():
            results, ds_response = run_simple_model(simple_recommender.cleaned_data)

        # Post results to the front-end
        return render(request, "simple-recommender.html", {"simple_recommender": simple_recommender, "simple_results": results, "ds_response": ds_response})

    # If no request is received, show the empty form
    else:
        simple_recommender = forms.SimpleRecommender()
        return render(request, "simple-recommender.html", {"simple_recommender": simple_recommender})


def run_simple_model(data):

    # Initialise information to be blank
    economy = "" 
    price = ""
    engine_size = "" 
    power = ""
    range_ = ""
    fuel = ""
    doors = ""
    seats = ""
    gearbox = ""
    body_type = ""

    # Convert form data into usable results for the recommendation system
    if data["select_reason"] == "short":
        fuel = "Unleaded"
        body_type = "Hatchback"
        engine_size = random.choice(["Smaller engine", "Average engine"])
    elif data["select_reason"] == "long":
        range_ = random.choice(["Long range", "Very long range"])
    elif data["select_reason"] == "general":
        body_type = random.choice(["SUV", "Saloon", "Estate"])
        doors = "5-doored"
        seats = "5-seater"
        gearbox = "Automatic"
    elif data["select_reason"] == "carry":
        body_type = random.choice(["Pick-up Truck", "Large Van", "Small Van"])
    elif data["select_reason"] == "weekend":
        body_type = random.choice(["Coupe", "Convertible"])
        power = random.choice(["Average power", "High power"])
        gearbox = "manual"
    elif data["select_reason"] == "many_passengers":
        body_type = "MPV"
        seats = random.choice(["7-seater", "8-seater", "12-seater", "15-seater"])

    if data["select_body"] != "I don't mind":
        body_type = data["select_body"]

    if data["select_price"] != "I don't mind":
        price = data["select_price"]

    if data["running_cost_choices"] == "Yes":
        economy = "Economical"

    # Create list with the data in the correct order for the recommendation system
    user_data = [economy, price, engine_size, power, range_, fuel, doors, seats, gearbox, body_type]

    # Remove blanks
    user_data = list(filter(lambda x: x != "", user_data))

    # Import and initialise dataset
    df_cars = pd.read_csv("static/datasets/Clean Car API Data.csv", index_col=0)
    df_cars = df_cars[["Car Name", "Overall"]].reset_index()
    df_temp = df_cars[["Car Name", "Overall"]]

    # Create temporary DataFrame and add user data under the name "User Requirements"  
    df_temp.loc[len(df_temp)] = ["User Requirements", user_data]
    df_temp = df_temp[df_temp.notnull()]

    # Prepare columns for model
    df_temp["Overall"] = df_temp["Overall"].apply(str)
    combined_features = df_temp["Overall"].str.replace("|", " ")

    # Vectorise the data
    vectoriser = TfidfVectorizer()
    matrix = vectoriser.fit_transform(combined_features.values.astype("U"))

    # Apply linear kernel
    similarity = linear_kernel(matrix, matrix)

    # Get similarity results
    similarity_df = pd.DataFrame(similarity, index=df_temp["Car Name"], columns=df_temp["Car Name"])

    # Find cars similar to user requirements
    car = str(df_temp["Car Name"].loc[len(df_temp) - 1])
    get_car = similarity_df.index.get_loc(car)

    # Collect the top 5 results as key value pairs, with the keys = car name and values = similarity
    recommendations_dict = similarity_df.iloc[get_car].sort_values(ascending=False)[1:6].to_dict()
    recommendations = []

    # Collect car names to ask DeepSeek about cars
    recs_for_deepseek = recommendations_dict.keys()

    # Write the recommendations in a clearer format
    a = 1
    for x in recommendations_dict:
        recommendations.append(f"{a}: {x} ({round(recommendations_dict[x] * 100, 2)}% similar)")
        a += 1

    recommendations = "\n".join(recommendations)

    # Get DeepSeek's information about recommendations
    deepseek_response = dict(ask_deepseek(", ".join(recs_for_deepseek))).get("choices", [])[0].get("message").get("content")

    # Return recommendations and DeepSeek response
    return recommendations, deepseek_response

def run_standard_model(data):

    user_data = []

    # Convert data into a usable format for the model, and add to a list in the correct order
    if len(data["economy"]) != 0 and data["economy"] != "I don't mind": 
        user_data.append(data["economy"])

    if len(data["price"]) != 0 and data["price"] != "I don't mind":
        user_data.append( data["price"])
        
    if len(data["engine_size"]) != 0 and data["engine_size"] != "I don't mind":
        user_data.append(data["engine_size"])
        
    if len(data["power"]) != 0 and data["power"] != "I don't mind":
        user_data.append(data["power"])
        
    if len(data["range_"]) != 0 and data["range_"] != "I don't mind":
        user_data.append(data["range_"])
        
    if len(data["fuel"]) != 0 and data["fuel"] != "I don't mind":
        user_data.append(data["fuel"])
        
    if len(data["doors"]) != 0 and data["doors"] != "I don't mind":
        user_data.append(data["doors"])
        
    if len(data["seats"]) != 0 and data["seats"] != "I don't mind":
        user_data.append(data["seats"])
        
    if len(data["gearbox"]) != 0 and data["gearbox"] != "I don't mind":
        user_data.append(data["gearbox"])
        
    if len(data["body_type"]) != 0 and data["body_type"] != "I don't mind":
        user_data.append(data["body_type"])

    # Import and initialise dataset
    df_cars = pd.read_csv("static/datasets/Clean Car API Data.csv", index_col=0)
    df_cars = df_cars[["Car Name", "Overall"]].reset_index()
    df_temp = df_cars[["Car Name", "Overall"]]
    
    # Create temporary DataFrame and add user data under the name "User Requirements"  
    df_temp.loc[len(df_temp)] = ["User Requirements", user_data]
    df_temp = df_temp[df_temp.notnull()]

    # Prepare columns for the model
    df_temp["Overall"] = df_temp["Overall"].apply(str)
    combined_features = df_temp["Overall"].str.replace("|", " ")

    # Vectorise data
    vectoriser = TfidfVectorizer()
    matrix = vectoriser.fit_transform(combined_features.values.astype("U"))

    # Apply cosine similarity
    similarity = cosine_similarity(matrix)

    # Get similarity results
    similarity_df = pd.DataFrame(similarity, index=df_temp["Car Name"], columns=df_temp["Car Name"])

    # Find cars similar to user requirements   
    car = str(df_temp["Car Name"].loc[len(df_temp) - 1])
    get_car = similarity_df.index.get_loc(car)

    # Collect the top 5 results as key value pairs, with the keys = car name and values = similarity
    recommendations_dict = similarity_df.iloc[get_car].sort_values(ascending=False)[1:6].to_dict()
    recommendations = []

    # Collect car names to ask DeepSeek about cars
    recs_for_deepseek = recommendations_dict.keys()

    # Write the recommendations in a clearer format
    a = 1
    for x in recommendations_dict:
        recommendations.append(f"{a}: {x} ({round(recommendations_dict[x] * 100, 2)}% similar)")
        a += 1

    recommendations = "\n".join(recommendations)

    # Get DeepSeek's information about recommendations
    deepseek_response = dict(ask_deepseek(", ".join(recs_for_deepseek))).get("choices", [])[0].get("message").get("content")

    # Return recommendations and DeepSeek response
    return recommendations, deepseek_response


def ask_deepseek(message):
    # API key for DeepSeek-R1 model, and the URL to access the API
    api_key = "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"
    api_url = "https://openrouter.ai/api/v1/chat/completions"

    # Add API key to header to use the API
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    # Create the request body
    data = {"model": "deepseek/deepseek-chat:free",
            "messages": [{
                "role": "user", 
                "content": f"Can you explain the pros and cons of the following for a UK buyer, for someone who doesn't know much about cars: {message}?\
                             Do not write an opening statement, but do use UK spelling and grammar. Write with HTML formatting, like an article.\
                             Also do not use an opening or closing HTML tag. Do not use a table for formatting."
            }]}

    # Post the request and collect the response
    response = requests.post(api_url, json=data, headers=headers)

    # Return the response
    return response.json()
