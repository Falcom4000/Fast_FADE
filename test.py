import FADE_Release_Python2
import os
import time
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

mydir = './pngs'
result_dir = './result'
def process_subdir(args):
    subdir, process_index = args
    start_time = time.time()
    subdir_path = os.path.join(mydir, subdir)
    print(f"Start processing {subdir_path}")
    
    # Initialize FADE for this process
    my_FADE = FADE_Release_Python2.initialize()
    
    # Get all files in the subdirectory
    files = os.listdir(subdir_path)
    results = []
    
    # Process each file with progress bar only for first process
    if process_index == 0:
        iterator = tqdm(files, desc=f"Processing {subdir}", position=0, leave=False)
    else:
        iterator = files
    
    for filename in iterator:
        filepath = os.path.join(subdir_path, filename)
        if os.path.isfile(filepath):  # Make sure it's a file, not a directory
            yOut = my_FADE.FADE(filepath)
            results.append((filename, yOut))
    
    # Save results to file
    result_filename = os.path.join(result_dir, f"{subdir}.txt")
    with open(result_filename, 'w') as f:
        for filename, yOut in results:
            f.write(f"{filename}\t{yOut}\n")
    
    # Calculate and print timing
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Calculate mean
    if results:
        mean = sum(result[1] for result in results) / len(results)
        print(f"Directory '{subdir}': {len(results)} files processed in {processing_time:.2f}s, mean result: {mean}")
    else:
        print(f"Directory '{subdir}': No files processed in {processing_time:.2f}s")
    
    # Terminate FADE for this thread
    my_FADE.terminate()
    
    return subdir, len(results), processing_time

if __name__ == '__main__':

    # Create result directory if it doesn't exist
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # Get all subdirectories in the main directory
    subdirs = [d for d in os.listdir(mydir) if os.path.isdir(os.path.join(mydir, d))]
    # Process subdirectories in parallel using process pool
    with ProcessPoolExecutor(max_workers=7) as executor:
        futures = [executor.submit(process_subdir, (subdir, i)) for i, subdir in enumerate(subdirs)]
        
        # Wait for all tasks to complete
        for future in futures:
            subdir, file_count, proc_time = future.result()