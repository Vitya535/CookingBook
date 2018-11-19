"""Бд для кулинарной книги через ORM"""
from sqlalchemy import CheckConstraint, Table
from app import db, ma
from sqlalchemy.exc import IntegrityError


DishAndIngredient = Table('DishAndIngredient', db.metadata,
                          db.Column('Dish_Id', db.Integer, db.ForeignKey('Dish.Id')),
                          db.Column('Ingredient_Id', db.Integer, db.ForeignKey('Ingredient.Id')))

RecipeAndImplement = Table('RecipeAndImplement', db.metadata,
                           db.Column('Recipe_Id', db.Integer, db.ForeignKey('Recipe.Id')),
                           db.Column('Implement_Id', db.Integer, db.ForeignKey('Implement.Id')))


# ToDo - сделать добавление по Enum (в тех таблицах где это нужно)
class Dish(db.Model):
    """Табличка блюда"""
    __tablename__ = 'Dish'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False, unique=True, default="")
    Description = db.Column(db.String, nullable=False, unique=True, default="")
    Portion_count = db.Column(db.Integer, CheckConstraint('Portion_count>0'), nullable=False, default=None)
    Type_Of_Dish = db.Column(db.String, nullable=False, default="")
    Recipes = db.relationship("Recipe", backref='dish')
    Ingredients = db.relationship("Ingredient", secondary=DishAndIngredient)

    def __init__(self, name="", description="", portion_count="", type_of_dish=""):
        self.Description = description
        self.Name = name
        self.Portion_count = portion_count
        self.Type_Of_Dish = type_of_dish

    def __repr__(self):
        return "Ingredient(%r, %r, %r, %r, %r)" % (self.Id, self.Name, self.Description, self.Portion_count,
                                                   self.Type_Of_Dish)


# ToDo - сделать добавление по Enum (в тех таблицах где это нужно)
class Ingredient(db.Model):
    """Табличка ингредиента"""
    __tablename__ = 'Ingredient'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False, default="")
    Count = db.Column(db.Integer, CheckConstraint('Count>0'), default=None)
    Unit_of_measurement = db.Column(db.String, default="")

    def __init__(self, name="", count="", unit_of_measurement=""):
        self.Count = count
        self.Name = name
        self.Unit_of_measurement = unit_of_measurement

    def __repr__(self):
        return "Ingredient(%r, %r, %r, %r)" % (self.Id, self.Name, self.Count, self.Unit_of_measurement)


class Implement(db.Model):
    """Табличка утвари"""
    __tablename__ = 'Implement'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False, unique=True, default="")

    def __init__(self, name=""):
        self.Name = name

    def __repr__(self):
        return "Implement(%r, %r)" % (self.Id, self.Name)


class StepOfCook(db.Model):
    """Табличка шага приготовления"""
    __tablename__ = 'StepOfCook'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Number_of_step = db.Column(db.Integer, CheckConstraint('Number_of_step>0'), nullable=False, default=None)
    Description = db.Column(db.String, nullable=False, unique=True, default="")
    Recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.Id', ondelete="CASCADE", onupdate="CASCADE"),
                          nullable=False, default=None)

    def __init__(self, number_of_step="", description="", recipe_id=""):
        self.Number_of_step = number_of_step
        self.Description = description
        self.Recipe_id = recipe_id

    def __repr__(self):
        return "StepOfCook(%r, %r, %r, %r)" % (self.Id, self.Number_of_step, self.Description, self.Recipe_id)


class Recipe(db.Model):
    """Табличка рецепта"""
    __tablename__ = 'Recipe'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Img_url = db.Column(db.String, nullable=False, unique=True, default="")
    Literature_url = db.Column(db.String, nullable=False, unique=True, default="")
    Time_on_preparation = db.Column(db.String, CheckConstraint('Time_on_preparation>0'),
                                    nullable=False, default="")
    Time_on_cooking = db.Column(db.String, CheckConstraint('Time_on_cooking>0'), nullable=False, default="")
    Dish_id = db.Column(db.Integer, db.ForeignKey('Dish.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False,
                        default=None)
    Steps_of_cook = db.relationship("StepOfCook", backref='recipe')
    Implements = db.relationship("Implement", secondary=RecipeAndImplement)

    def __init__(self, img_url="", literature_url="", time_on_preparation="", time_on_cooking="", dish_id=""):
        self.Img_url = img_url
        self.Literature_url = literature_url
        self.Time_on_preparation = time_on_preparation
        self.Time_on_cooking = time_on_cooking
        self.Dish_id = dish_id

    def __repr__(self):
        return "Recipe(%r, %r, %r, %r, %r, %r)" % (self.Id, self.Img_url, self.Literature_url, self.Time_on_preparation,
                                                   self.Time_on_cooking, self.Dish_id)


def orm_add(title_of_table):
    """Добавление в бд"""
    try:
        new_row = eval(title_of_table)()
        db.session.add(new_row)
        db.session.flush()
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def orm_delete(delete_id, title_of_table):
    """Удаление из бд"""
    obj_for_delete = eval(title_of_table).query.get(delete_id)
    db.session.delete(obj_for_delete)
    db.session.flush()
    db.session.commit()


def orm_update(value, update_id, attr_title, title_of_table):
    """Редактирование в бд"""
    print(update_id)
    obj_for_update = eval(title_of_table).query.get(update_id)
    setattr(obj_for_update, attr_title, value)
    db.session.flush()
    db.session.commit()


class DishSchema(ma.ModelSchema):
    class Meta:
        model = Dish


class IngredientSchema(ma.ModelSchema):
    class Meta:
        model = Ingredient


class ImplementSchema(ma.ModelSchema):
    class Meta:
        model = Implement


class StepOfCookSchema(ma.ModelSchema):
    class Meta:
        model = StepOfCook


class RecipeSchema(ma.ModelSchema):
    class Meta:
        model = Recipe


dishes_schema = DishSchema(many=True)
ingredients_schema = IngredientSchema(many=True)
implements_schema = ImplementSchema(many=True)
steps_of_cook_schema = StepOfCookSchema(many=True)
recipes_schema = RecipeSchema(many=True)


METADATA = db.metadata
db.create_all()
