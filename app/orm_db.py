"""Бд для кулинарной книги через ORM"""
from sqlalchemy import CheckConstraint
from sqlalchemy import Table

from app import DB
from app import MA
from app.utils import TypesOfDish
from app.utils import UnitsOfMeasurement

DISH_AND_INGREDIENT = Table('dish_and_ingredient', DB.metadata,
                            DB.Column('dish_id', DB.Integer,
                                      DB.ForeignKey('dish.id', ondelete="CASCADE",
                                                    onupdate="CASCADE")),
                            DB.Column('ingredient_id', DB.Integer,
                                      DB.ForeignKey('ingredient.id', ondelete="CASCADE",
                                                    onupdate="CASCADE")))

RECIPE_AND_IMPLEMENT = Table('recipe_and_implement', DB.metadata,
                             DB.Column('recipe_id', DB.Integer,
                                       DB.ForeignKey('recipe.id', ondelete="CASCADE",
                                                     onupdate="CASCADE")),
                             DB.Column('implement_id', DB.Integer,
                                       DB.ForeignKey('implement.id', ondelete="CASCADE",
                                                     onupdate="CASCADE")))


class Dish(DB.Model):
    """Табличка блюда"""
    __tablename__ = 'dish'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String, nullable=False, unique=True)
    description = DB.Column(DB.String, nullable=False, unique=True)
    portion_count = DB.Column(DB.Integer, CheckConstraint('portion_count>0'),
                              nullable=False)
    type_of_dish = DB.Column(DB.Enum(TypesOfDish), nullable=False)
    recipes = DB.relationship('Recipe', backref='dish')
    ingredients = DB.relationship('Ingredient', secondary=DISH_AND_INGREDIENT,
                                  backref=DB.backref('dishes', lazy='dynamic'))

    def __init__(self, description, name, portion_count, type_of_dish):
        self.description = description
        self.name = name
        self.portion_count = portion_count
        self.type_of_dish = type_of_dish

    def __repr__(self):
        return f"Ingredient({self.id}, {self.name}, {self.description}, {self.portion_count}, {self.type_of_dish})"


class Ingredient(DB.Model):
    """Табличка ингредиента"""
    __tablename__ = 'ingredient'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String, nullable=False)
    count = DB.Column(DB.Integer, CheckConstraint('count>0'), nullable=False)
    unit_of_measurement = DB.Column(DB.Enum(UnitsOfMeasurement), nullable=False)

    def __init__(self, count, name, unit_of_measurement):
        self.count = count
        self.name = name
        self.unit_of_measurement = unit_of_measurement

    def __repr__(self):
        return f"Ingredient({self.id}, {self.name}, {self.count}, {self.unit_of_measurement})"


class Implement(DB.Model):
    """Табличка утвари"""
    __tablename__ = 'implement'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Implement({self.id}, {self.name})"


class StepOfCook(DB.Model):
    """Табличка шага приготовления"""
    __tablename__ = 'step_of_cook'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    number_of_step = DB.Column(DB.Integer, CheckConstraint('number_of_step>0'), nullable=False)
    description = DB.Column(DB.String, nullable=False, unique=True)
    recipe_id = DB.Column(DB.Integer,
                          DB.ForeignKey('recipe.id', ondelete="CASCADE", onupdate="CASCADE"),
                          nullable=False)

    def __init__(self, number_of_step, description, recipe_id):
        self.number_of_step = number_of_step
        self.description = description
        self.recipe_id = recipe_id

    def __repr__(self):
        return f"StepOfCook({self.id}, {self.number_of_step}, {self.description}, {self.recipe_id})"


class Recipe(DB.Model):
    """Табличка рецепта"""
    __tablename__ = 'recipe'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    img_url = DB.Column(DB.String, nullable=False, unique=True)
    literature_url = DB.Column(DB.String, nullable=False, unique=True)
    time_on_preparation = DB.Column(DB.String, CheckConstraint('time_on_preparation>0'),
                                    nullable=False)
    time_on_cooking = DB.Column(DB.String, CheckConstraint('time_on_cooking>0'),
                                nullable=False)
    dish_id = DB.Column(DB.Integer,
                        DB.ForeignKey('dish.id', ondelete="CASCADE", onupdate="CASCADE"),
                        nullable=False)
    steps_of_cook = DB.relationship('StepOfCook', backref='recipe')
    implements = DB.relationship('Implement', secondary=RECIPE_AND_IMPLEMENT,
                                 backref=DB.backref('recipes', lazy='dynamic'))

    def __init__(self, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
        self.img_url = img_url
        self.literature_url = literature_url
        self.time_on_preparation = time_on_preparation
        self.time_on_cooking = time_on_cooking
        self.dish_id = dish_id

    def __repr__(self):
        return f"Recipe({self.id}, {self.img_url}, {self.literature_url}, {self.time_on_preparation}," \
               f" {self.time_on_cooking}, {self.dish_id})"


class DishSchema(MA.SQLAlchemySchema):
    """Схема для таблички блюда"""

    class Meta:
        """Метаданные для схемы таблички блюда"""
        model = Dish


class IngredientSchema(MA.SQLAlchemySchema):
    """Схема для таблички ингредиента"""

    class Meta:
        """Метаданные для схемы таблички ингредиента"""
        model = Ingredient


class ImplementSchema(MA.SQLAlchemySchema):
    """Схема для таблички утвари"""

    class Meta:
        """Метаданные для схемы таблички утвари"""
        model = Implement


class StepOfCookSchema(MA.SQLAlchemySchema):
    """Схема для таблички шага приготовления"""

    class Meta:
        """Метаданные для схемы таблички шага приготовления"""
        model = StepOfCook


class RecipeSchema(MA.SQLAlchemySchema):
    """Схема для таблички рецептов"""

    class Meta:
        """Метаданные для схемы таблички рецептов"""
        model = Recipe


DISHES_SCHEMA = DishSchema(many=True)
INGREDIENTS_SCHEMA = IngredientSchema(many=True)
IMPLEMENTS_SCHEMA = ImplementSchema(many=True)
STEPS_OF_COOK_SCHEMA = StepOfCookSchema(many=True)
RECIPES_SCHEMA = RecipeSchema(many=True)
