from django.utils.timezone import now


def user_image_location(user, file):
    """
    Generate a file path for the user's image upload based on the current date.

    Args:
        user (CustomUser): The user instance.
        file (File): The file being uploaded.

    Returns:
        str: The file path where the image will be stored.
    """
    today = now()
    return f'users/{user.get_username()}/{today.year}/{today.month}/{today.day}/{file.name}'
