# QuickDraw
This code helps to convert ndjson files to images from the quickdraw dataset

# Steps
1. Download the ndjson files from glcoud using gsutil. Note that we will be using the simplified version that is commonly enough for experimentation.
gsutil -m cp 'gs://quickdraw_dataset/full/simplified/*.ndjson' .

Suposse we saved the data into <DIR>/ndjson, and  the images will be saved to <DIR>/sketches

2. Run the bash script **qd_save_sketches.sh** to leverage parallelism.
  2.1. Prepare a file with the list of categories. We call it **category.txt**
  2.2. Split the file into N files to run in parallel. You can use the command **split** of linux.
  2.4. Change the correspoding paths to <DIR> in the bash script.
  BASE=<DIR>
  DIR=<DIR>
  2.3. Modify the bash script to be aligned with the number of thread you want to run.
  for i in {<start>..<end>} 
  2.4. Finally run 
  bash qd_save_sketches.sh
  
  Good Luck!!
  
  
  
 
