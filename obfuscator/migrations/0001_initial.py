# Generated by Django 3.1.2 on 2021-01-18 21:34

from django.db import migrations, models
import django.db.models.deletion
import obfuscator.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_id', models.CharField(max_length=50, unique=True, validators=[obfuscator.models.is_positive])),
                ('last_photo_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_photo', models.ImageField(max_length=250, upload_to=obfuscator.models.get_image_path)),
                ('faces_location_arr', models.CharField(blank=True, max_length=400)),
                ('face_count', models.IntegerField(blank=True, default=0)),
                ('participant_faces', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant_blur', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant_pixel', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant_deepfake', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant_masked', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant_avatar', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('deepfake_all', models.ImageField(blank=True, max_length=250, upload_to='')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obfuscator.participant')),
            ],
        ),
    ]
