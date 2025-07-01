from django.db import models

class GenreChoice(models.TextChoices):
    ACTION = 'ACTION', 'Action'
    ADVENTURE = 'ADVENTURE', 'Adventure'
    ANIMATION = 'ANIMATION', 'Animation'
    COMEDY = 'COMEDY', 'Comedy'
    CRIME = 'CRIME', 'Crime'
    DOCUMENTARY = 'DOCUMENTARY', 'Documentary'
    DRAMA = 'DRAMA', 'Drama'
    FANTASY = 'FANTASY', 'Fantasy'
    HISTORICAL = 'HISTORICAL', 'Historical'
    HORROR = 'HORROR', 'Horror'
    MUSICAL = 'MUSICAL', 'Musical'
    MYSTERY = 'MYSTERY', 'Mystery'
    ROMANCE = 'ROMANCE', 'Romance'
    SCIFI = 'SCIFI', 'Sci-Fi'
    THRILLER = 'THRILLER', 'Thriller'
    WAR = 'WAR', 'War'
    WESTERN = 'WESTERN', 'Western'
    FAMILY = 'FAMILY', 'Family'
    BIOGRAPHY = 'BIOGRAPHY', 'Biography'
    SPORTS = 'SPORTS', 'Sports'

class LanguageChoice(models.TextChoices):
    BANGLA = "BANGLA", "Bangla"
    ENGLISH = "ENGLISH", "English"
    HINDI = "HINDI", "Hindi"