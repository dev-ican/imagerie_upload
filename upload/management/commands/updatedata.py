from django.core.management.base import BaseCommand, CommandError
from app.models import Produits

import requests
import json
import unicodedata

class Command(BaseCommand):
    help = "Importe un jeu de donnée venant d'OpenFoodFact"

    def handle(self, *args, **options):
        liste=["ingredients_text","image_ingredients_url","nutrition-score-fr_100g","image_front_url","image_nutrition_url","quantity","product_name","ingredients_text_fr"]

        records = Produits.objects.filter(_id__gt=0)


        for records_id in records:
            barre_code = records_id._id
            split_codebarre = str(barre_code).split('.')
            codebarre = split_codebarre[0]
            url_request = 'https://world.openfoodfacts.org/api/v0/product/' + str(codebarre) + '.json'
            payload = {}
            headers = {
                'content-type' : 'application/x-www-form-urlencoded'
            }
            r = requests.request("GET",url_request,headers=headers,data=payload)
            results = json.loads(r.content)


            for item in liste:
                if int(liste.index(item)) == 2:
                    var_item = results['product']['nutriments'].get(item)
                    var_bdd = records_id.grade
                    if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(grade=var_item)
                else: 
                    index = liste.index(item)
                    if index == 0:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.ingredient
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(ingredient=var_item)
                    elif index == 1:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.url_image_ingredients
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(url_image_ingredients=var_item)
                    elif index == 3:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.image_front_url
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(image_front_url=var_item)
                    elif index == 4:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.image_nutrition_url
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(image_nutrition_url=var_item)
                    elif index == 5:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.nova_groups
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(nova_groups=var_item)
                    elif index == 6:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.generic_name_fr
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(generic_name_fr=var_item)
                    elif index == 7:
                        var_item = results['product'].get(item)
                        var_bdd = records_id.ingredients_text_fr
                        if str(var_bdd) != str(var_item) and var_item != None:
                            Produits.objects.filter(id=records_id.id).update(ingredients_text_fr=var_item)


        self.stdout.write(self.style.SUCCESS('commande succes'))