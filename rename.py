import os
import concurrent.futures

def rename_file(file_path):
    """
    Rename the file by appending .jpg if not already present.
    """
    directory, filename = os.path.split(file_path)
    # If the file already ends with .jpg (case-insensitive), skip it.
    if filename.lower().endswith('.jpg'):
        return f"Skipped: {filename}"
    
    new_filename = filename + '.jpg'
    new_file_path = os.path.join(directory, new_filename)
    
    try:
        os.rename(file_path, new_file_path)
        return f"Renamed: {filename} -> {new_filename}"
    except Exception as e:
        return f"Error renaming {filename}: {e}"

def process_folder(folder):
    # Get absolute path to folder
    folder = os.path.abspath(folder)
    
    # List all files in the folder (ignores subdirectories)
    files = [os.path.join(folder, f)
             for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))]
    
    # Process renaming using ProcessPoolExecutor for parallel processing.
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(rename_file, file_path): file_path for file_path in files}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(result)
    return results

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Append '.jpg' to the names of all files in the given folder (multi-core).")
    parser.add_argument('folder', help="Path to the folder to process")
    args = parser.parse_args()
    
    process_folder(args.folder)
