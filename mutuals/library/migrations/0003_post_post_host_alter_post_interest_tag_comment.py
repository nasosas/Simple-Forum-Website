# Generated by Django 4.1.3 on 2022-11-22 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_post_interest_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.user'),
        ),
        migrations.AlterField(
            model_name='post',
            name='interest_tag',
            field=models.ManyToManyField(related_name='interest_tag', to='library.interest'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.user')),
            ],
        ),
    ]
