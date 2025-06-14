# Generated by Django 4.2.16 on 2024-11-01 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=127)),
                ('type', models.CharField(choices=[('NESTED', 'Nested'), ('STRING', 'String'), ('NUMBER', 'Number'), ('BOOLEAN', 'Boolean'), ('ARRAY', 'Array')], default='NESTED', editable=False, max_length=7)),
                ('value', models.JSONField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pairs.keyvalue')),
            ],
        ),
    ]
