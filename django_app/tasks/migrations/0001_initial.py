from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=20, choices=[('created','created'),('in_progress','in_progress'),('completed','completed')], default='created')),
            ],
        ),
    ]
