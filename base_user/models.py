from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from base_user.tools.common import get_user_profile_photo_file_name, GENDER
from twitter_app.models import Follow

USER_MODEL = settings.AUTH_USER_MODEL
from easy_thumbnails.files import get_thumbnailer


# Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Tələb olunur. 75 simvol və ya az. Hərflər, Rəqəmlər və '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'),
                                                              'yanlışdır')
                                ])
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)
    profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    background = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, verbose_name="cinsi", null=True, blank=True)

    slug = models.SlugField(max_length=255, null=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """
        Important non-field stuff
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.first_name

    def get_timeline_url(self):
        return reverse("timeline", kwargs={"slug": self.slug})

    def get_background(self):
        if self.background:
            return self.background.url
        else:
            return "/static/twitter/images/resources/timeline-1.jpg"

    def get_following_count(self):
        return Follow.objects.filter(
            from_user=self,
            status=True
        ).count()

    def get_followers_count(self):
        return Follow.objects.filter(
            to_user=self,
            status=True
        ).count()

    def get_avatar(self):
        if self.profile_picture:
            return get_thumbnailer(self.profile_picture)['avatar'].url
        else:
            return "https://graph.facebook.com/%s/picture?type=large" % '100002461198950'
