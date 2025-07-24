import FADE_Release_Python2
import os
import time

mydir = './pngs'
result_dir = './result'

# Create result directory if it doesn't exist
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

my_FADE_Release_Python2 = FADE_Release_Python2.initialize()

# Get all subdirectories in the main directory
subdirs = [d for d in os.listdir(mydir) if os.path.isdir(os.path.join(mydir, d))]

for subdir in subdirs:
    start_time = time.time()
    subdir_path = os.path.join(mydir, subdir)
    
    # Get all files in the subdirectory
    files = os.listdir(subdir_path)
    results = []
    
    # Process each file
    for filename in files:
        filepath = os.path.join(subdir_path, filename)
        if os.path.isfile(filepath):  # Make sure it's a file, not a directory
            yOut = my_FADE_Release_Python2.FADE(filepath)
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

my_FADE_Release_Python2.terminate()