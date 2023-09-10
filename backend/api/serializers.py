import re

from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from sensors.models import Sensor, Tag, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'password',
                  'first_name', 'last_name', 'is_subscribed']
        write_only_fields = ['password']
        extra_kwargs = {'password': {'write_only': True},
                        'is_subscribed': {'read_only': True}}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return user.follower.filter(author=obj).exists()
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# class RecipeRetrieveSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True, read_only=True)
#     author = UserSerializer(read_only=True)
#     ingredients = serializers.SerializerMethodField()
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = '__all__'

#     def get_ingredients(self, obj):
#         return obj.ingredients.values(
#             'id', 'name', 'measurement_unit',
#             amount=F('ingredients_amount__amount')
#         )

#     def get_is_favorited(self, obj):
#         user = self.context.get('request').user
#         if not user.is_anonymous:
#             return obj.favorites.filter(user=user).exists()
#         return False

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context.get('request').user
#         if not user.is_anonymous:
#             return obj.cart.filter(user=user).exists()
#         return False


# class RecipeCreateSerializer(serializers.ModelSerializer):
#     author = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )
#     ingredients = serializers.SerializerMethodField()
#     image = Base64ImageField(max_length=None, use_url=True)

#     class Meta:
#         model = Recipe
#         fields = '__all__'
#         read_only_fields = ['author']

#     def validate_name(self, value):
#         if re.match(r'^[0-9\W]+$', value):
#             raise ValidationError(
#                 {'name': 'Can\'t contains only symbols and numbers.'})
#         return value

#     def validate(self, data):
#         ingredients = self.initial_data['ingredients']
#         ingredient_list = []
#         if not ingredients:
#             raise serializers.ValidationError(
#                 'Must be at least one ingredient.'
#             )
#         for item in ingredients:
#             ingredient = get_object_or_404(
#                 Ingredient, id=item['id']
#             )
#             if ingredient in ingredient_list:
#                 raise serializers.ValidationError(
#                     'Ingredient already add in recipe.'
#                 )
#             if int(item.get('amount')) < 1:
#                 raise serializers.ValidationError(
#                     'Minimal amount is 1.'
#                 )
#             ingredient_list.append(ingredient)
#         data['ingredients'] = ingredients
#         return data

#     def get_ingredients(self, obj):
#         return obj.ingredients.values(
#             'id', 'name', 'measurement_unit',
#             amount=F('ingredients_amount__amount')
#         )

#     def add_tags_ingredients(self, instance, **validate_data):
#         ingredients = validate_data['ingredients']
#         tags = validate_data['tags']
#         for tag in tags:
#             instance.tags.add(tag)
#         IngredientInRecipe.objects.bulk_create([
#             IngredientInRecipe(
#                 recipe=instance,
#                 ingredient_id=ingredient.get('id'),
#                 amount=ingredient.get('amount')
#             ) for ingredient in ingredients
#         ])
#         return instance

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         recipe = super().create(validated_data)
#         self.add_tags_ingredients(recipe, ingredients=ingredients, tags=tags)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.ingredients.clear()
#         instance.tags.clear()
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         instance = self.add_tags_ingredients(
#             instance, ingredients=ingredients, tags=tags)
#         return super().update(instance, validated_data)


# class FavoriteOrShoppingCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ['id', 'name', 'cooking_time', 'image']
#         read_only_fields = ['id', 'name', 'cooking_time', 'image']


# class FollowSerializer(serializers.ModelSerializer):
#     email = serializers.ReadOnlyField(source='author.email')
#     id = serializers.ReadOnlyField(source='author.id')
#     username = serializers.ReadOnlyField(source='author.username')
#     first_name = serializers.ReadOnlyField(source='author.first_name')
#     last_name = serializers.ReadOnlyField(source='author.last_name')
#     is_subscribed = serializers.SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Follow
#         fields = ['email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed', 'recipes', 'recipes_count']

#     def get_is_subscribed(self, obj):
#         user = self.context.get('request').user
#         if not user.is_anonymous:
#             return obj.author.following.filter(user=user).exists()
#         return False

#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit = request.GET.get('recipes_limit')
#         recipes = obj.author.recipes.all()
#         if limit and limit.isdigit():
#             recipes = recipes[:int(limit)]
#         return FavoriteOrShoppingCartSerializer(recipes, many=True).data

#     def get_recipes_count(self, obj):
#         return obj.author.recipes.count()

#     def validate(self, data):
#         author = self.context.get('author')
#         user = self.context.get('request').user
#         if user.follower.filter(author=author).exists():
#             raise ValidationError(
#                 detail='You already follow this author.',
#                 code=status.HTTP_400_BAD_REQUEST)
#         if user == author:
#             raise ValidationError(
#                 detail='Can\'t follow yourself.',
#                 code=status.HTTP_400_BAD_REQUEST)
#         return data
