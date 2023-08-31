from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


def is_file_field_or_image_field(
        field: models.ImageField | models.FileField) -> bool:
    return any([isinstance(field, models.FileField),
                isinstance(field, models.ImageField)])


@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if is_file_field_or_image_field(field):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if is_file_field_or_image_field(field):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(
                    sender, instance, field, instance_in_db_file_field)


def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(
        **dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)


class Account(AbstractUser, PermissionsMixin):
    patronymic = models.CharField(
        _('patronymic'),
        max_length=150,
        blank=True
    )
    biography = models.TextField(
        _('biography'),
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    phone_number = PhoneNumberField(
        _('phone number'),
        region='RU',
        unique=True,
        blank=True
    )
    avatar = models.ImageField(
        _('avatar image'),
        max_length=None,
        upload_to='users/avatar/',
        null=True,
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.email
