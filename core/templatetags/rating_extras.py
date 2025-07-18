from django import template
from math import floor, ceil

register = template.Library()


@register.inclusion_tag("core/components/star_rating.html")
def star_rating(rating, show_value=True, show_count=True, count=0):
    """
    Display star rating with proper filled stars
    """
    rating = float(rating) if rating else 0
    full_stars = int(floor(rating))
    half_star = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)

    return {
        "rating": rating,
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
        "show_value": show_value,
        "show_count": show_count,
        "count": count,
    }
