import os


def get_songs(directory):
    # List all files in the directory (ignore directories)
    filenames_with_extension = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]

    # Remove the file extension from each filename
    filenames_without_extension = [
        os.path.splitext(filename)[0] for filename in filenames_with_extension
    ]

    return filenames_without_extension
