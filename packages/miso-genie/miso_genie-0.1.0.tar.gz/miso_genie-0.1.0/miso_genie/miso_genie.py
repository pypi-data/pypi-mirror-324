import random

class MisoGenie:
    def __init__(self):
        self.miso_types = ["white", "red", "yellow", "black"]
        self.recipes = {
            "soup": ["miso soup", "ramen broth", "veggie stew"],
            "marinade": ["salmon glaze", "tofu marinade", "grilled veggies"],
            "dessert": ["miso caramel", "miso cookies", "ice cream topping"]
        }
        self.puns = [
            "I’m here to *soy*-light you with miso magic! 🧞♂️",
            "Let’s *ferment* some ideas!",
            "Your culinary wish is my command!"
        ]

    def rub_lamp(self):
        """Activate the genie with a 'lamp rub'"""
        print(random.choice(self.puns))

    def conjure_recipe(self, category=None):
        """Generate a random miso recipe"""
        if not category:
            category = random.choice(list(self.recipes.keys()))
        recipe = random.choice(self.recipes[category])
        print(f"🧞✨ Poof! Try this: **{recipe}** with {random.choice(self.miso_types)} miso!")

    def grant_wish(self, ingredients):
        """Suggest a dish based on ingredients"""
        dishes = {
            "tofu": "miso-maple glazed tofu",
            "salmon": "miso-mirin grilled salmon",
            "eggplant": "miso-roasted eggplant",
            "chocolate": "miso-chocolate brownies"
        }
        for item in ingredients:
            if item in dishes:
                print(f"🧞 Use {item} for: {dishes[item]}!")
                return
        print("🧞✨ Magic can’t fix a bare pantry... but add miso to ANYTHING!")
