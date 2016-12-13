# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# Add extra import to populate the highlighted field when the model is saved
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField(blank=True, default='')
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python3', max_length=100)
    style = models.CharField(
        choices=STYLE_CHOICES, default='friendly', max_length=100)

    # Information for authentication & permissions
    # owner = models.ForeignKey(
    #     'auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    # Test image
    image = models.ImageField(
        verbose_name=_("Image"),
        blank=True,
        # null=True,
        upload_to='upload/avatars',
        # default='default/avatars/default-avatar.png',
        # validators=[validate_image],
    )

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    # def cache(self):
    #     """Store image locally if we have a URL"""

    #     if self.url and not self.photo:
    #         result = urllib.urlretrieve(self.url)
    #         self.photo.save(
    #                 os.path.basename(self.url),
    #                 File(open(result[0]))
    #                 )
    #         self.save()
    #     # See http://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield 

    def __unicode__(self):
        return self.code
