# Generated by Django 4.0.2 on 2022-03-04 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_transaction_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='data_time',
            new_name='date_time',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.quizs'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.registeruser'),
        ),
    ]
