import csv
import re

# Fungsi untuk membaca file txt dan memparse konten
def parse_txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Regex untuk memparse tanggal, waktu, nomor telepon/nama, dan pesan
    message_pattern = re.compile(r'(\d{2}/\d{2}/\d{2}) (\d{2}.\d{2}) - (.*?): (.*)')
    join_pattern = re.compile(r'(\d{2}/\d{2}/\d{2}) (\d{2}.\d{2}) - (.*?) bergabung menggunakan tautan undangan grup ini')

    data = []

    for line in lines:
        message_match = message_pattern.match(line)
        join_match = join_pattern.match(line)

        if message_match:
            date, time, sender, message = message_match.groups()
            data.append([date, time, sender, message])
        elif join_match:
            date, time, info = join_match.groups()
            data.append([date, time, info, 'Bergabung dalam grup'])

    # Menulis ke file CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Tanggal', 'Waktu', 'Pengirim', 'Pesan'])
        csv_writer.writerows(data)

# Contoh penggunaan
input_file = 'dataset.txt'  # Nama file txt input
output_file = 'dataset.csv'  # Nama file csv output

parse_txt_to_csv(input_file, output_file)