from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_userprofile_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='content_type',
            field=models.CharField(choices=[('movie', 'Movie'), ('webseries', 'Web Series')], default='movie', max_length=10),
        ),
        migrations.AddField(
            model_name='movie',
            name='seasons',
            field=models.PositiveIntegerField(default=0, help_text='Number of seasons (for web series only)'),
        ),
        migrations.AddField(
            model_name='movie',
            name='episodes',
            field=models.PositiveIntegerField(default=0, help_text='Number of episodes (for web series only)'),
        ),
    ]