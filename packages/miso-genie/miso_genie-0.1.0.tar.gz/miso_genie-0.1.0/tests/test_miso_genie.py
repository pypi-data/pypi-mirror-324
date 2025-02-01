from miso_genie import MisoGenie

def test_recipe_generation():
    genie = MisoGenie()
    genie.conjure_recipe("soup")
    
def test_wish_granting():
    genie = MisoGenie()
    genie.grant_wish(["tofu"])
