from django.db import models
from django.utils.translation import gettext_lazy as _
from parts.models import Component, Category
from core.models import TimestampMixin


class RawDataDigikey(TimestampMixin):
    component = models.ForeignKey(Component, related_name='raw_data_digikey', on_delete=models.CASCADE,
                                  verbose_name=_('Компонент'), null=True, blank=True)
    raw_json = models.JSONField(_('Сырые данные JSON'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return f'Raw Data for {self.component.part_number if self.component else "unknown component"} (Digikey)'

    class Meta:
        verbose_name = _('Сырые данные Digikey')
        verbose_name_plural = _('Сырые данные Digikey')


class DigikeyBrand(models.Model):
    name = models.CharField(_('Название'), max_length=255, unique=True, db_index=True)

    def  __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Бренд Digikey')
        verbose_name_plural = _('Бренды Digikey')


class DigikeyComponent(models.Model):
    component = models.OneToOneField(Component, related_name='digikey_info', on_delete=models.CASCADE, verbose_name=_('Компонент'))
    digikey_brand = models.ForeignKey(DigikeyBrand, related_name='components', on_delete=models.CASCADE, verbose_name=_('Бренд Digikey'))
    category = models.ForeignKey(Category, related_name='digikey_components', on_delete=models.CASCADE, verbose_name=_('Категория'))
    url = models.URLField(_('URL'), max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'{self.component.part_number} - Digikey'

    class Meta:
        verbose_name = _('Компонент Digikey')
        verbose_name_plural = _('Компоненты Digikey')


class DigikeyPrice(TimestampMixin):
    digikey_component = models.ForeignKey(DigikeyComponent, related_name='prices', on_delete=models.CASCADE, verbose_name=_('Компонент Digikey'))
    quantity = models.PositiveIntegerField(_('Количество'))
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=4)

    def __str__(self):
        return f'{self.digikey_component.component.part_number} ({self.digikey_component.component.brand.name}) - от {self.quantity}шт. - {self.price}$'

    class Meta:
        verbose_name = _('Цена Digikey')
        verbose_name_plural = _('Цены Digikey')


class DigikeyStock(TimestampMixin):
    digikey_component = models.OneToOneField(DigikeyComponent, related_name='stock', on_delete=models.CASCADE, verbose_name=_('Компонент Digikey'))
    in_stock_quantity = models.PositiveIntegerField(_('Количество на складе'))

    def  __str__(self):
        return f'{self.digikey_component.component.part_number} ({self.digikey_component.component.brand.name}) - {self.in_stock_quantity}шт.'

    class Meta:
        verbose_name = _('Наличие Digikey')
        verbose_name_plural = _('Наличия Digikey')
