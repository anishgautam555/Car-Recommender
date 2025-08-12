from django import forms

class SimpleRecommender(forms.Form):
    # Write the options and their corresponding attributes
    running_costs = {"Yes": "Yes", "No" : "No"}

    reasons = {"short" : "Short trips (school runs, shopping etc.)",
               "long" : "Long motorway trips",
               "general" : "General use (some short and long trips)",
               "carry" : "Carrying large amounts of items",
               "weekend" : "Fun on the weekends", 
               "many_passengers" : "Carrying lots of passengers"}
    
    price_choices = {"Cheap": "Cheap", "Average Priced": "Average Priced", "Expensive": "Expensive", "I don't mind": "I don't mind"}

    body_choices = {"SUV": "SUV", "Hatchback": "Hatchback", "Saloon": "Saloon", "Estate": "Estate", "Coupe": "Coupe", 
                "Convertible": "Convertible", "Pick-up Truck": "Pick-up Truck", "MPV": "MPV", "Small Van": "Small Van", 
                "Large Van": "Large Van", "I don't mind": "I don't mind"}

    # Create fields with the above selections
    select_reason = forms.ChoiceField(widget=forms.RadioSelect, choices=reasons, label="What do you want to use the car for?")
    select_body = forms.ChoiceField(widget=forms.RadioSelect, choices=body_choices, label="Do you have a shape in mind?")
    select_price = forms.ChoiceField(widget=forms.RadioSelect, choices=price_choices, label="What budget do you have in mind for your car?")
    running_cost_choices = forms.ChoiceField(widget=forms.RadioSelect, choices=running_costs, label="Do you need lower running costs?")
    

class StandardRecommender(forms.Form):

    # Write the options and their corresponding attributes
    economy_choices = {"Uneconomical": "Uneconomical", "Average economy": "Average economy", "Economical": "Economical", "I don't mind": "I don't mind"}

    price_choices = {"Cheap": "Cheap", "Average Priced": "Average Priced", "Expensive": "Expensive", "I don't mind": "I don't mind"}

    engine_choices = {"Smaller Engine": "Smaller Engine", "Average Sized Engine": "Average Sized Engine", "Larger Engine": "Larger Engine", "I don't mind": "I don't mind"}

    power_choices = {"Lower power": "Lower power", "Average power": "Average power", "High power": "High power", "Very high power": "Very high power", "I don't mind": "I don't mind"}

    range_choices = {"Short range": "Short range", "Average range": "Average range", "Long range": "Long range", "Very long range": "Very long range", "I don't mind": "I don't mind"}

    fuel_choices = {"Unleaded": "Petrol (Unleaded)", "Diesel": "Diesel", "I don't mind": "I don't mind"}

    doors_choices = {"2-doored": "2-doored", "3-doored": "3-doored", "4-doored": "4-doored", "5-doored": "5-doored", "I don't mind": "I don't mind"}
    
    seat_choices = {"2-seater": "2-seater", "3-seater": "3-seater", "4-seater": "4-seater", "5-seater": "5-seater", "6-seater": "6-seater", 
                    "7-seater": "7-seater", "8-seater": "8-seater", "12-seater": "12-seater", "15-seater": "15-seater", "I don't mind": "I don't mind"}
    
    gearbox_choices = {"Manual": "Manual", "Automatic": "Automatic", "I don't mind": "I don't mind"}

    body_choices = {"SUV": "SUV", "Hatchback": "Hatchback", "Saloon": "Saloon", "Estate": "Estate", "Coupe": "Coupe", 
                "Convertible": "Convertible", "Pick-up Truck": "Pick-up Truck", "MPV": "MPV", "Small Van": "Small Van", 
                "Large Van": "Large Van", "I don't mind": "I don't mind"}

    # Create fields with the above selections
    body_type = forms.ChoiceField(widget=forms.RadioSelect, choices=body_choices, required=False, label="Body Type")
    gearbox = forms.ChoiceField(widget=forms.RadioSelect, choices=gearbox_choices, required=False, label="Gearbox")
    fuel = forms.ChoiceField(widget=forms.RadioSelect, choices=fuel_choices, required=False, label="Fuel")
    price = forms.ChoiceField(widget=forms.RadioSelect, choices=price_choices, label="Price", required=False)
    engine_size = forms.ChoiceField(widget=forms.RadioSelect, choices=engine_choices, required=False, label="Engine Size")
    range_ = forms.ChoiceField(widget=forms.RadioSelect, choices=range_choices, required=False, label="Range")
    doors = forms.ChoiceField(widget=forms.RadioSelect, choices=doors_choices, required=False, label="Number of Doors")
    power = forms.ChoiceField(widget=forms.RadioSelect, choices=power_choices, required=False, label="Horsepower")
    economy = forms.ChoiceField(widget=forms.RadioSelect, choices=economy_choices, required=False, label="Economy (MPG)")
    seats = forms.ChoiceField(widget=forms.RadioSelect, choices=seat_choices, required=False, label="Number of Seats")
