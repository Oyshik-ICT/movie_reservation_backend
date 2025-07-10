from django.db import models

class RowChoice(models.TextChoices):
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"
    D = "D", "D"
    E = "E", "E"
    F = "F", "F"
    G = "G", "G"
    H = "H", "H"
    I = "I", "I"
    J = "J", "J"

class SeatNumberChoice(models.IntegerChoices):
    ONE = 1, "1"
    TWO = 2, "2"
    THREE = 3, "3"
    FOUR = 4, "4"
    FIVE = 5, "5"
    SIX = 6, "6"
    SEVEN = 7, "7"
    EIGHT = 8, "8"
    NINE = 9, "9"
    TEN = 10, "10"

class SeatTypeChoice(models.TextChoices):
    REGULAR = "regular", "Regular"
    PREMIUM = "premium", "Premium" 
    VIP = "vip", "VIP"
    RECLINER = "recliner", "Recliner"