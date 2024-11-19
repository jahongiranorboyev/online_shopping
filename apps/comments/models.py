from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductComment(models.Model):
    """
    Represents a comment on a product by a user, including a rating and message.

    Fields:
        product (ForeignKey): The product being commented on.
        user (ForeignKey): The user who posted the comment (optional).
        rating (IntegerField): The rating given to the product (0-5).
        name (CharField): The name of the person who posted the comment (if not a registered user).
        email (EmailField): The email of the commenter.
        message (CharField): The content of the comment.
        created_at (DateTimeField): The timestamp when the comment was created.

    Methods:
        save(): Saves the comment, using the user's name and email if available.
    """
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        help_text="The product that this comment is related to."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who posted the comment (if logged in)."
    )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="The rating given to the product (0-5)."
    )
    name = models.CharField(
        max_length=120,
        help_text="The name of the commenter (if user is not logged in)."
    )
    email = models.EmailField(
        help_text="The email of the commenter."
    )
    message = models.CharField(
        max_length=250,
        help_text="The content of the comment."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of when the comment was created."
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically set the name and email
        from the user if the comment is posted by a registered user.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments passed to the save method.

        Saves:
            The product comment instance, updating the name and email if the user is authenticated.
        """
        if self.user:
            self.name = self.user.get_full_name()
            self.email = self.user.email
        super().save(*args, **kwargs)
