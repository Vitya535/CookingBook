from sqlalchemy import Column, SmallInteger, String, Integer, Time, Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from server import db


class Implements(db.Model):
    __tablename__ = 'implements'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Implements('{self.id}', '{self.name}')\r\n"


class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    count = Column(SmallInteger())
    unit_of_measurement = Column(String(10))

    def __repr__(self):
        return f"Ingredients('{self.id}', '{self.name}', '{self.count}', '{self.unit_of_measurement}')\r\n"


class TimeOfCook(db.Model):
    __tablename__ = 'time_of_cook'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    freezing = Column(Time())
    chilling = Column(Time())
    preparation = Column(Time(), nullable=False)
    cooking = Column(Time(), nullable=False)
    dishes_with_recipe = relationship("DishesWithRecipe", backref='take_time')

    def __repr__(self):
        return f"TimeOfCook('{self.id}', '{self.freezing}', '{self.chilling}', '{self.preparation}', '{self.cooking}')" \
               f"\r\n"


class DishesWithRecipe(db.Model):
    __tablename__ = 'dishes_with_recipe'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text(), unique=True)
    portion_count = Column(SmallInteger(), nullable=False)
    type_of_dish = Column(String(20), nullable=False)  # зн-я через enum или словарь
    url_on_literature = Column(String(50), nullable=False)
    time_id = Column(Integer(), ForeignKey(TimeOfCook.id))
    implements = relationship('DishesAndImplementsKeys', backref='cooking_with_help')
    ingredients = relationship('DishesAndIngredientsKeys', backref='contains_from')
    step_of_cook = relationship('StepOfCook', backref='have_steps')

    def __repr__(self):
        return f"DishesWithRecipe('{self.id}', '{self.name}', '{self.description}', '{self.portion_count}'," \
               f" '{self.type_of_dish}', '{self.url_on_literature}', '{self.time_id}')\r\n"


class DishesAndImplementsKeys(db.Model):
    __tablename__ = 'dishes_and_implements_keys'
    implements_id = Column(Integer, ForeignKey(Implements.id), primary_key=True)
    dishes_with_recipe_id = Column(Integer, ForeignKey(DishesWithRecipe.id), primary_key=True)


class DishesAndIngredientsKeys(db.Model):
    __tablename__ = 'dishes_and_ingredients_keys'
    dishes_with_recipe_id = Column(Integer, ForeignKey(DishesWithRecipe.id), primary_key=True)
    ingredients_id = Column(Integer, ForeignKey(Ingredients.id), primary_key=True)


class StepOfCook(db.Model):
    __tablename__ = 'step_of_cook'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    number_of_step = Column(SmallInteger(), nullable=False)
    description = Column(SmallInteger(), nullable=False)
    recipe_id = Column(Integer(), ForeignKey(DishesWithRecipe.id))

    def __repr__(self):
        return f"StepOfCook('{self.id}', '{self.number_of_step}', '{self.description}', '{self.recipe_id}')\r\n"
