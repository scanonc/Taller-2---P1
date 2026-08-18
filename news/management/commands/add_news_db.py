import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import News

class Command(BaseCommand):
    help = 'Populate database with the first 5 news items from CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'Fake.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File not found at: {csv_file_path}'))
            return

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                if count >= 5:
                    break

                # Mapeo de columnas según el CSV proporcionado
                headline_text = row['title'].strip()
                body_text = row['text'].strip()
                raw_date = row['date'].strip()

                # Parseo del formato de fecha: "December 31, 2017"
                try:
                    date_val = datetime.strptime(raw_date, '%B %d, %Y').date()
                except ValueError:
                    # En caso de error o fecha no válida, se asigna la fecha actual
                    date_val = datetime.now().date()

                # Crear registro en la base de datos
                News.objects.create(
                    headline=headline_text,
                    body=body_text,
                    date=date_val
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {count} news items to the database.')
        )