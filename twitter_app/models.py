from django.db import models

# Create your models here.
from django.urls import reverse

from twitter_app.helper import token_generator


class Post(models.Model):
    user = models.ForeignKey('base_user.MyUser',
                             on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="post/",
                                null=True, blank=True)
    like_count = models.IntegerField(default=0)
    context = models.CharField(max_length=5000)

    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.user.get_full_name())

    class Meta:
        ordering = ("-id",)


# modelin_adi  comment_set

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('base_user.MyUser', on_delete=models.CASCADE)
    context = models.CharField(max_length=2000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self)


class LikeModel(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("base_user.MyUser", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.post, self.user.get_full_name())


class Follow(models.Model):
    from_user = models.ForeignKey('base_user.MyUser', related_name="following",
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey('base_user.MyUser', related_name="followers",
                                on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} => {}".format(self.from_user.get_full_name(), self.to_user.get_full_name())


class EmailVerification(models.Model):
    user = models.ForeignKey("base_user.MyUser", on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default=token_generator)
    expire = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_verification_url(self):
        return reverse("verify") + "?uuid={}&token={}".format(self.user.id, self.token)

    def __str__(self):
        return "{} {}".format(self.user.get_full_name(), self.token)
