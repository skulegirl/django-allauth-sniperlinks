# Generated by Django 3.2.10 on 2022-12-01 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_email_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SniperLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mx_domain', models.CharField(blank=True, max_length=100, null=True)),
                ('mail_provider', models.CharField(choices=[('UNKNOWN', 'Unknown'), ('GMAIL', 'Gmail'), ('GSUITE', 'Gsuite'), ('YAHOO', 'Yahoo'), ('AOL', 'AOL'), ('ROGERS', 'ROGERS'), ('OUTLOOK', 'Outlook'), ('ICLOUD', 'iCloud'), ('CHARTER', 'Charter'), ('CENTURYLINK', 'CenturyLink'), ('ONEANDONE', '1and1'), ('COMCAST', 'Comcast'), ('COX', 'Cox'), ('SHAW', 'Shaw'), ('FASTMAIL', 'Fastmail'), ('FRONTIER', 'Frontier'), ('MAILDOTCOM', 'Mail_com'), ('EARTHLINK', 'Earthlink'), ('PRODIGY', 'Prodigy'), ('PROTONMAIL', 'ProtonMail'), ('JUNO', 'Juno'), ('NETADDRESS', 'NetAddress'), ('VIDEOTRON', 'Videotron'), ('WINDSTREAM', 'Windstream'), ('ZOHO', 'Zoho')], default='UNKNOWN', max_length=30)),
                ('email_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.emailaddress')),
            ],
        ),
    ]
