# Generated by Django 2.0.7 on 2018-07-13 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iris',
            name='iris_class',
            field=models.IntegerField(choices=[(0, 'IRIS_SETOSA'), (1, 'IRIS_VERSICOLOR'), (2, 'IRIS_VIRGINICA')], default=0),
        ),
    ]
