# Generated by Django 5.0.7 on 2024-11-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeManagementapp', '0003_alter_logindata_user_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='regcolumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columnname', models.CharField(default='', max_length=255)),
                ('type', models.CharField(default='', max_length=255)),
                ('fieldname', models.CharField(default='', max_length=255)),
                ('placeholder', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
