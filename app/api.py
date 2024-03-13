#api.py
from app import app
from app.models import Recipe
from flask import Flask, jsonify


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes_query = Recipe.query.all()
    recipes = []
    for recipe in recipes_query:
        recipes.append({
            'id': recipe.id,
            'title': recipe.title,
            'image_filename': recipe.image_filename,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'timestamp': recipe.timestamp.isoformat(),
            'user_id': recipe.user_id
        })
    return jsonify(recipes)
