# Generated by Django 4.2.5 on 2023-09-16 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sms_service', '0002_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('sender', models.IntegerField()),
                ('receiver', models.IntegerField()),
            ],
        ),
    ]
