# import h5py

# model_path = "./data/DoubleUNet/files/model.h5"
# with h5py.File(model_path, 'r') as f:
#     if 'keras_version' in f.attrs:
#         print("Keras version:", f.attrs['keras_version'])
#     if 'backend' in f.attrs:
#         print("Backend:", f.attrs['backend'])


# import os
# from PIL import Image

# def compare_image_sizes(folder1, folder2):
#     """
#     Compare image sizes between two folders. 
#     Outputs images with mismatched sizes.
#     """
#     mismatched_files = []
    
#     # List files in both folders
#     folder1_files = {os.path.splitext(f)[0]: f for f in os.listdir(folder1) if f.endswith('.jpg')}
#     folder2_files = {os.path.splitext(f)[0]: f for f in os.listdir(folder2) if f.endswith('.png')}

#     # Find common file names between the folders
#     common_files = folder1_files.keys() & folder2_files.keys()

#     for file_name in folder1_files:
#         file1_path = os.path.join(folder1, folder1_files[file_name])
#         x = file_name+'_segmentation'
#         file2_path = os.path.join(folder2, folder2_files[x])

#         # Open images and compare sizes
#         with Image.open(file1_path) as img1, Image.open(file2_path) as img2:
#             if img1.size != img2.size:
#                 mismatched_files.append((file1_path, file2_path, img1.size, img2.size))
    
#     # Output results
#     if mismatched_files:
#         print("Mismatched image sizes found:")
#         for file1, file2, size1, size2 in mismatched_files:
#             print(f"{file1} ({size1}) != {file2} ({size2})")
#     else:
#         print("All matched images are of the same size.")

# # Example usage
# folder1_path = '.\data\ISIC2018_Task1-2_Test_Input'
# folder2_path = '.\data\ISIC2018_Task1_Test_GroundTruth'

# compare_image_sizes(folder1_path, folder2_path)


# import os

# def remove_segmentation_postfix(folder_path):
#     """
#     Remove '_segmentation' from file names in the specified folder.
#     """
#     for filename in os.listdir(folder_path):
#         # Split filename and extension
#         name, ext = os.path.splitext(filename)
#         if '_segmentation' in name:
#             # Remove '_segmentation' from the name
#             new_name = name.replace('_segmentation', '') + ext
#             # Rename the file
#             os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
#             print(f"Renamed: {filename} -> {new_name}")

# # Example usage
# folder_path = './data/ISIC2018_Task1_Validation_GroundTruth_'
# remove_segmentation_postfix(folder_path)

# import os
# from PIL import Image

# def convert_jpg_to_png(folder_path):
#     """
#     Convert all .jpg files in the specified folder to .png format.
#     """
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.jpg'):
#             # Full path to the jpg file
#             jpg_path = os.path.join(folder_path, filename)
            
#             # Open the jpg file
#             with Image.open(jpg_path) as img:
#                 # Replace .jpg extension with .png
#                 png_filename = os.path.splitext(filename)[0] + '.png'
#                 png_path = os.path.join(folder_path, png_filename)
                
#                 # Save the image as png
#                 img.save(png_path, 'PNG')
#                 print(f"Converted: {filename} -> {png_filename}")

# # Example usage
# folder_path = './data/ISIC2018_Task1-2_Validation_Input_'
# convert_jpg_to_png(folder_path)


from PIL import Image
import os

def resize_images(folder_path, size=(256, 256)):
    """
    Resize all images in the folder to the specified size.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png')):
            img_path = os.path.join(folder_path, filename)
            with Image.open(img_path) as img:
                resized_img = img.resize(size)
                resized_img.save(img_path)
                print(f"Resized: {filename}")

# Example usage
resize_images('./data/ISIC2018_Task1_Validation_GroundTruth_', size=(512, 384))
resize_images('./data/ISIC2018_Task1-2_Validation_Input_', size=(512, 384))