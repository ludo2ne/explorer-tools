import os
import shutil
import csv
import datetime

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class MusicFiles:
    """
    Gestion des fichiers musicaux
    """

    def __init__(self, path):
        self.path = path

    def update_metadata(self, file_path):
        """
        Maj des métadonnées d'un fichier mp3
        """
        try:
            audio = EasyID3(file_path)

            # Get the existing album, date, and title values
            album = audio.get('album', [''])[0]
            date = audio.get('date', [''])[0]
            title = audio.get('title', [''])[0]

            # Check if album is not empty and is a valid year
            if album and album.isdigit() and 1900 <= int(album) <= 2100:
                # Replace the date with the album
                audio['date'] = album
                audio.save()

            # Modify the filename based on the title
            new_file_name = f"{title}.mp3"
            new_file_path = os.path.join(
                os.path.dirname(file_path), new_file_name)

            # Rename the file if the new filename is different
            if os.path.basename(file_path) != new_file_name:
                os.rename(file_path, new_file_path)
                print(
                    f"File renamed: '{os.path.basename(file_path)}' to '{new_file_name}'")

            return new_file_path

        except Exception as e:
            print(f"Error updating metadata for file '{file_path}': {str(e)}")

    def class_in_folders(self):
        """
        Appel la méthode de mise à jour des métadonnées pour chaque fichier
        Puis déplace le fichier dans le bon dossier
        """
        try:
            for file_name in os.listdir(self.path):
                if file_name.endswith('.mp3'):
                    file_path = os.path.join(self.path, file_name)

                    new_file_path = self.update_metadata(file_path)

                    if new_file_path:
                        audio = EasyID3(new_file_path)
                        date = audio.get('date', [''])[0]

                        if date:
                            if '1990' <= date <= '1999':
                                destination_folder = '1990 - 1999'
                            elif '2000' <= date <= '2009':
                                destination_folder = '2000 - 2009'
                            elif '2010' <= date <= '2019':
                                destination_folder = '2010 - 2019'
                            elif date <= '1989':
                                destination_folder = '1989 et avant'
                            else:
                                destination_folder = None

                            if destination_folder:
                                destination_path = os.path.join(
                                    self.path, destination_folder)
                                os.makedirs(destination_path, exist_ok=True)
                                shutil.move(new_file_path, os.path.join(
                                    destination_path, os.path.basename(new_file_path)))
                                print(
                                    f"File moved to folder '{destination_folder}'")

        except Exception as e:
            print(f"Error moving files in folder '{self.path}': {str(e)}")

    def format_size(self, size_bytes):
        """
        Converts a size in bytes to a human-readable format
        """
        for unit in ['', 'KB', 'MB', 'GB', 'TB']:
            if abs(size_bytes) < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def export_details_to_csv(self):

        csv_file = os.path.join(self.path, "song_list.csv")

        # Open the CSV file in write mode with ';' as the delimiter
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")

            # Write the CSV header row
            writer.writerow(["Filename", "Title", "Artist", "Album",
                            "Year", "Gender", "Duration", "Size", "Creation Date"])

            # Iterate over all files in the folder
            for file_name in os.listdir(self.path):
                if file_name.endswith(".mp3"):
                    file_path = os.path.join(self.path, file_name)

                    try:
                        # Open the MP3 file and extract the metadata
                        audio = EasyID3(file_path)
                        title = audio.get("title", [""])[0]
                        artist = audio.get("artist", [""])[0]
                        album = audio.get("album", [""])[0]

                        # La clé date peut contenir 2 types de données :
                        #   l'attribut annee que je rentrais à la main
                        #   une valeur de date sur laquelle je n'avais plus la main depuis la maj du logiciel de download
                        # Extract only the year (first 4 characters)
                        year = audio.get("date", [""])[0]
                        # year = audio.get("date", [""])[0][:4]  # Extract only the year (first 4 characters)

                        gender = audio.get("genre", [""])[0]

                        # Get the duration and size of the MP3 file
                        mp3 = MP3(file_path)
                        duration = str(datetime.timedelta(
                            seconds=int(mp3.info.length)))
                        size = os.path.getsize(file_path)
                        size_human_readable = self.format_size(size)

                        # Get the creation date of the MP3 file
                        creation_date = datetime.datetime.fromtimestamp(
                            os.path.getctime(file_path)).strftime("%Y-%m-%d")

                        # Write the metadata to the CSV file
                        writer.writerow([file_name, title, artist, album, year,
                                        gender, duration, size_human_readable, creation_date])
                    except Exception as e:
                        print(f"Error processing file: {file_name} - {e}")


if __name__ == "__main__":

    new_music = MusicFiles('P:\Ludo\Privé\Zik new')
    new_music.class_in_folders()
    new_music.export_details_to_csv()
