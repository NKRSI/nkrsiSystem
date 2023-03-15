from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class FrontPage(models.Model):
    order = models.IntegerField(_('order'), default=0,
                                help_text=_('Order in which links will be presented on home page. '
                                            'The lower number the higher position.'))
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField(_('text'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(FrontPage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('front subpage')
        verbose_name_plural = _('front subpages')

    def __str__(self):
        return self.title


class FrontPageImage(models.Model):
    order = models.IntegerField(_('order'), default=0,
                                help_text=_('Order in which links will be presented on home page. '
                                            'The lower number the higher position.'))
    text = models.TextField(_('text'))
    img = models.ImageField(_('image'))
    page = models.ForeignKey(FrontPage, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('front subpage image')
        verbose_name_plural = _('front subpage images')

