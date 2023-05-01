import http.client
import json
import os
from typing import List, Tuple


class TerminalColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class RecipeInstruction:
    def __init__(self, number, step, ingredients, equipments):
        self.number = number
        self.step = step
        self.ingredients = ingredients
        self.equipments = equipments

    def __str__(self):
        step_detail = f"    {TerminalColors.OKGREEN}• step {self.number}: {self.step}{TerminalColors.ENDC}\n"
        if self.ingredients:
            step_detail += f'\n        {TerminalColors.OKBLUE}required ingredient(s){TerminalColors.ENDC}: {", ".join(self.ingredients)}\n'
        if self.equipments:
            step_detail += f'\n        {TerminalColors.OKBLUE}required equipment(s){TerminalColors.ENDC}: {", ".join(self.equipments)}\n'
        step_detail += "\n"
        return step_detail


class Chef:
    def __init__(self):
        self.conn = http.client.HTTPSConnection(
            "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        )
        self.headers = {
            "content-type": "application/octet-stream",
            "X-RapidAPI-Key": os.getenv("SPOONACULAR_API_KEY"),
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        }

    def api_key_set(self) -> bool:
        return True if os.getenv("SPOONACULAR_API_KEY") else False

    def search_recipes(self, query: str) -> Tuple[List[int], List[str]]:
        self.conn.request(
            "GET",
            f"/recipes/complexSearch?query={query.replace(' ','%20')}&offset=0&number=10&",
            headers=self.headers,
        )
        res = self.conn.getresponse()
        data = res.read().decode("utf-8")
        response_json = json.loads(data)
        results = response_json["results"]
        prev_title = None
        idx = 1
        ids = []
        recipes = []
        for result in results:
            title = result["title"]
            recipe = title
            ids.append(result["id"])
            if prev_title != title:
                idx = 1
            else:
                if idx == 1:
                    recipes[-1] = recipes[-1] + " (Version 1)"
                idx += 1
                recipe = f"{title} (Version {idx})"
            recipes.append(recipe)
            prev_title = title
        for i in range(len(ids)):
            print(f"{ids[i]}, {recipes[i]}")
        return (ids, recipes)

    def get_analyzed_recipe_instructions(
        self, recipe_id: int
    ) -> List[RecipeInstruction]:
        self.conn.request(
            "GET",
            f"/recipes/{recipe_id}/analyzedInstructions?stepBreakdown=true",
            headers=self.headers,
        )
        res = self.conn.getresponse()
        data = res.read().decode("utf-8")
        instructions = json.loads(data)
        instruction_list = []
        print(
            f"\n\n{TerminalColors.HEADER}==== Recipe from Chef Auto-GPT ===={TerminalColors.ENDC}\n"
        )
        for instruction in instructions:
            name = instruction["name"]

            if name:
                print("====", name, "====")
            ingredients = []
            equipments = []
            for step in instruction["steps"]:
                for ingredient in step["ingredients"]:
                    ingredients.append(ingredient["name"])
                for equipment in step["equipment"]:
                    equipments.append(equipment["name"])
                recipe_instruction = RecipeInstruction(
                    number=step["number"],
                    step=step["step"],
                    ingredients=ingredients,
                    equipments=equipments,
                )
                instruction_list.append(recipe_instruction)
                print(recipe_instruction)
        print(
            f"{TerminalColors.HEADER}==== End of Recipe ===={TerminalColors.ENDC}\n\n"
        )
        return instruction_list
