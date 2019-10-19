# Generated by Django 2.2.5 on 2019-10-14 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('degree', models.CharField(choices=[('Bachelor', 'Bachelor'), ('Master', 'Master')], max_length=120)),
                ('course', models.CharField(choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('Civil', 'Civil')], max_length=120)),
                ('public', models.CharField(choices=[('1', 'Public'), ('0', 'Specific')], max_length=120)),
            ],
        ),
    ]
