from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_movie_average_rating_movie_cast_movie_director_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='newsletter',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='public_profile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='show_activity',
            field=models.BooleanField(default=True),
        ),
    ]