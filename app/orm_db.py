"""Бд для кулинарной книги через ORM"""
from sqlalchemy import CheckConstraint
from sqlalchemy import Table

from app.extensions import db
from app.utils import TypesOfDish
from app.utils import UnitsOfMeasurement

DISH_AND_INGREDIENT = Table('dish_and_ingredient', db.metadata,
                            db.Column('dish_id', db.Integer,
                                      db.ForeignKey('dish.id', ondelete="CASCADE",
                                                    onupdate="CASCADE")),
                            db.Column('ingredient_id', db.Integer,
                                      db.ForeignKey('ingredient.id', ondelete="CASCADE",
                                                    onupdate="CASCADE")))

RECIPE_AND_IMPLEMENT = Table('recipe_and_implement', db.metadata,
                             db.Column('recipe_id', db.Integer,
                                       db.ForeignKey('recipe.id', ondelete="CASCADE",
                                                     onupdate="CASCADE")),
                             db.Column('implement_id', db.Integer,
                                       db.ForeignKey('implement.id', ondelete="CASCADE",
                                                     onupdate="CASCADE")))


class Dish(db.Model):
    """Табличка блюда"""
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False, unique=True)
    portion_count = db.Column(db.Integer, CheckConstraint('portion_count>0'),
                              nullable=False)
    type_of_dish = db.Column(db.Enum(TypesOfDish), nullable=False)
    recipes = db.relationship('Recipe', backref='dish')
    ingredients = db.relationship('Ingredient', secondary=DISH_AND_INGREDIENT,
                                  backref=db.backref('dishes', lazy='dynamic'))

    def __init__(self, description, name, portion_count, type_of_dish):
        self.description = description
        self.name = name
        self.portion_count = portion_count
        self.type_of_dish = type_of_dish

    def __repr__(self):
        return f"Ingredient({self.id}, {self.name}, {self.description}, {self.portion_count}, {self.type_of_dish})"


class Ingredient(db.Model):
    """Табличка ингредиента"""
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, CheckConstraint('count>0'), nullable=False)
    unit_of_measurement = db.Column(db.Enum(UnitsOfMeasurement), nullable=False)

    def __init__(self, count, name, unit_of_measurement):
        self.count = count
        self.name = name
        self.unit_of_measurement = unit_of_measurement

    def __repr__(self):
        return f"Ingredient({self.id}, {self.name}, {self.count}, {self.unit_of_measurement})"


class Implement(db.Model):
    """Табличка утвари"""
    __tablename__ = 'implement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Implement({self.id}, {self.name})"


class StepOfCook(db.Model):
    """Табличка шага приготовления"""
    __tablename__ = 'step_of_cook'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number_of_step = db.Column(db.Integer, CheckConstraint('number_of_step>0'), nullable=False)
    description = db.Column(db.String, nullable=False, unique=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipe.id', ondelete="CASCADE", onupdate="CASCADE"),
                          nullable=False)

    def __init__(self, number_of_step, description, recipe_id):
        self.number_of_step = number_of_step
        self.description = description
        self.recipe_id = recipe_id

    def __repr__(self):
        return f"StepOfCook({self.id}, {self.number_of_step}, {self.description}, {self.recipe_id})"


class Recipe(db.Model):
    """Табличка рецепта"""
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_url = db.Column(db.String, nullable=False, unique=True)
    literature_url = db.Column(db.String, nullable=False, unique=True)
    time_on_preparation = db.Column(db.String, CheckConstraint('time_on_preparation>0'),
                                    nullable=False)
    time_on_cooking = db.Column(db.String, CheckConstraint('time_on_cooking>0'),
                                nullable=False)
    dish_id = db.Column(db.Integer,
                        db.ForeignKey('dish.id', ondelete="CASCADE", onupdate="CASCADE"),
                        nullable=False)
    steps_of_cook = db.relationship('StepOfCook', backref='recipe')
    implements = db.relationship('Implement', secondary=RECIPE_AND_IMPLEMENT,
                                 backref=db.backref('recipes', lazy='dynamic'))

    def __init__(self, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
        self.img_url = img_url
        self.literature_url = literature_url
        self.time_on_preparation = time_on_preparation
        self.time_on_cooking = time_on_cooking
        self.dish_id = dish_id

    def __repr__(self):
        return f"Recipe({self.id}, {self.img_url}, {self.literature_url}, {self.time_on_preparation}," \
               f" {self.time_on_cooking}, {self.dish_id})"
