from flask import Flask, render_template, abort, request, flash, redirect, url_for

from model import (Recipe, find_all, find_by_id, find_by_name,
                   save, delete_by_id)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # flash üzenetekhez kell


@app.route('/')
def list_all():
    if request.args.get('search'):
        recipes = find_by_name(request.args.get('search'))
    else:
        recipes = find_all()

    return render_template('list.html', recipes=recipes)


@app.route('/view/<int:recipe_id>')
def view(recipe_id):
    recipe = find_by_id(recipe_id) or abort(404)

    return render_template('view.html', recipe=recipe)


@app.route('/create', methods=('GET', 'POST'))
def create():
    recipe = Recipe()
    errors = []

    if request.method == 'POST':
        recipe.update(request.form)
        errors = recipe.validate()

        if len(errors) == 0:
            save(recipe)
            flash('Recipe created.')

            return redirect(url_for('list_all'))

    return render_template(
        'form.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
def edit(recipe_id):
    recipe = find_by_id(recipe_id) or abort(404)
    errors = []

    if request.method == 'POST':
        recipe.update(request.form)
        errors = recipe.validate()

        if len(errors) == 0:
            save(recipe)
            flash('Recipe saved.')

            return redirect(url_for('edit', recipe_id=recipe.recipe_id))

    return render_template(
        'form.html',
        recipe=recipe,
        errors=errors
    )


@app.route('/delete/<int:recipe_id>', methods=('POST',))
def delete(recipe_id):
    find_by_id(recipe_id) or abort(404)
    delete_by_id(recipe_id)
    flash('Recipe deleted.')

    return redirect(url_for('list_all'))


if __name__ == '__main__':
    app.run()
