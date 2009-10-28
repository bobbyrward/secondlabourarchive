from django.db import models
from django.contrib.auth.models import User


class DownloadTopics(models.Model):
    number = models.IntegerField()
    date = models.DateTimeField()
    crawl = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.number)

    class Admin:
        pass


class DownloadService(models.Model):
    name = models.CharField(max_length=64)
    url_re = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class Release(models.Model):
    name = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class DownloadLink(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    service = models.ForeignKey(DownloadService)
    date_added = models.DateTimeField(auto_now_add=True)
    #thumbnail_url = models.URLField(verify_exists=False, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d', max_length=255, null=True)
    from_topic = models.ForeignKey(DownloadTopics)
    release = models.ForeignKey(Release, null=True)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.url

    class Admin:
        date_hierarchy = 'date_added'
        list_per_page = 25
        ordering = ('-date_added', 'name')


    class Meta:
        get_latest_by = 'date_added'
        ordering = ('-date_added', 'name')
        unique_together = ('url',)
        verbose_name = 'Link'


class ImportedLink(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    text = models.TextField()
    service = models.ForeignKey(DownloadService)
    date_added = models.DateTimeField(auto_now_add=True)
    thumbnail_url = models.URLField(verify_exists=False, blank=True)

    class Meta:
        unique_together = ('url',)


class UserProfile(models.Model):
    preferred_service = models.ForeignKey(DownloadService)
    user = models.ForeignKey(User, unique=True)

    class Admin:
        pass


class TroubleTicketType(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Admin:
        pass


class TroubleTicket(models.Model):
    link = models.ForeignKey(DownloadLink)
    ticket_type = models.ForeignKey(TroubleTicketType)
    from_user = models.ForeignKey(User)
    date_submitted = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.ticket_type, self.from_user, self.date_submitted)

    class Admin:
        date_hierarchy = 'date_submitted'
        list_per_page = 25
        ordering = ('-date_submitted',)
        pass

