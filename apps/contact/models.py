from django.conf import settings
from django.db import models


class Contact(models.Model):
    """
    A model representing a contact form submission.

    Fields:
        user (ForeignKey): The user associated with the contact (optional).
        name (CharField): The name of the person submitting the contact form.
        email (EmailField): The email of the person submitting the contact form.
        subject (CharField): The subject of the contact message.
        message (TextField): The content of the contact message.

    Methods:
        save: Custom save method to automatically set name and email if the user is provided.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)

    def __str__(self):
        """
        Returns the name of the contact as the string representation of the model.

        Returns:
            str: The name of the contact.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Custom save method to set the name and email fields based on the user,
        if a user is associated with the contact.

        Args:
            *args: Positional arguments to be passed to the parent save method.
            **kwargs: Keyword arguments to be passed to the parent save method.
        """
        if self.user:
            self.name, self.email = self.user.first_name, self.user.email
        super().save(*args, **kwargs)
