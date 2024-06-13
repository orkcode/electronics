from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
