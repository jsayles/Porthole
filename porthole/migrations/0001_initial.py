# Generated by Django 2.0.6 on 2018-06-28 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('floor', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=4)),
                ('switch_port', models.SmallIntegerField(blank=True, null=True)),
                ('closet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='porthole.Location')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.Location')),
            ],
            options={
                'ordering': ['closet__number', 'label'],
            },
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.SmallIntegerField()),
                ('make', models.CharField(blank=True, max_length=64, null=True)),
                ('model', models.CharField(blank=True, max_length=64, null=True)),
                ('port_count', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['stack', 'unit'],
            },
        ),
        migrations.CreateModel(
            name='SwitchStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4', unique=True)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('port', models.SmallIntegerField(default=22)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.Location')),
            ],
        ),
        migrations.CreateModel(
            name='VLAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=16)),
                ('description', models.CharField(blank=True, max_length=64, null=True)),
                ('ip_range', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'ordering': ['tag'],
            },
        ),
        migrations.AddField(
            model_name='switch',
            name='stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.SwitchStack'),
        ),
        migrations.AddField(
            model_name='port',
            name='switch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='porthole.Switch'),
        ),
        migrations.AddField(
            model_name='port',
            name='vlan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porthole.VLAN'),
        ),
    ]
