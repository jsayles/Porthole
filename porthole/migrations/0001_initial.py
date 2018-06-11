# Generated by Django 2.0.6 on 2018-06-11 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EthernetPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=4)),
                ('switch_port', models.SmallIntegerField(blank=True, null=True)),
                ('vlan', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('floor', models.CharField(max_length=1)),
                ('number', models.CharField(max_length=5)),
                ('door', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=64)),
                ('make', models.CharField(max_length=64)),
                ('model', models.CharField(max_length=64)),
                ('port_count', models.SmallIntegerField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.Location')),
            ],
        ),
        migrations.AddField(
            model_name='ethernetport',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.Location'),
        ),
        migrations.AddField(
            model_name='ethernetport',
            name='switch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.Switch'),
        ),
    ]
