from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userprofile_download_url_userprofile_share_enabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='allow_download',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='download_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='share_enabled',
            field=models.BooleanField(default=True),
        ),
    ]