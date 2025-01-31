
from nbconvert import RSTExporter
import nbformat
import os
import shutil

DOC_PATH = os.path.abspath(os.path.dirname(__file__))

def convert_notebook_to_rst(input_file, output_dir, file_name):
    # Load the notebook
    with open(input_file, "r", encoding="utf-8") as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Create an RST exporter
    rst_exporter = RSTExporter()

    # Generate RST content
    rst_content, resources = rst_exporter.from_notebook_node(notebook_content)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.rst")

    # Add a link to the jupyter notebook file to the documentation
    rst_content += f"\n:download:`Link to the jupyter notebook file </../notebooks/{file_name}.ipynb>`.\n"

    # Write RST content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rst_content)

    print(f"Conversion successful. RST file saved to: {output_file}")

    # Copy images to the output folder
    for image_filename, image_data in resources["outputs"].items():
        print(image_filename)
        image_path = os.path.join(output_dir, image_filename)
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)


def get_all_ipynb_files(doc_path=DOC_PATH, examples_path="notebooks"):
    notebooks_path = os.path.join(doc_path, examples_path)

    all_examples_folders = os.listdir(notebooks_path)
    notebooks = []
    images = []
    path_dict= {}

    for example in all_examples_folders:

        if example ==".DS_Store":
            continue
        
        
        for file in os.listdir(os.path.join(notebooks_path, example)):
            if file.endswith("ipynb"):
                notebooks.append(
                    (
                f"{DOC_PATH}/{examples_path}/{example}/{file}",
                file.split(".ipynb")[0]
                     )
                     )
                path_dict[example] = file.split(".ipynb")[0]


        for file in os.listdir(os.path.join(notebooks_path, example)):
                
            if file.endswith((".jpg",".png")):
 
                images.append(
                    (
                        f"{DOC_PATH}/{examples_path}/{example}/{file}",
                        path_dict[example]
                    )

                    )

    return notebooks,images


def copy_image_to_directory(source_image_path, destination_directory):

    # Get the basename of the image file
    image_name = os.path.basename(source_image_path)
    
    # Define the destination path
    destination_path = os.path.join(destination_directory, image_name)
    
    # Copy the image to the destination directory
    shutil.copy2(source_image_path, destination_path)
    
    return destination_path

def update_notebooks_rst_files(doc_path=DOC_PATH):
    files,images = get_all_ipynb_files(doc_path)
    print(images)
    for file, folder in files:
        convert_notebook_to_rst(
            file,
            output_dir=os.path.join(doc_path, "source", "examples", folder),
            file_name=folder,
        )

    for file,path in images:

        copy_image_to_directory(
            file,
            os.path.join(doc_path, "source", "examples", path),
        )





if __name__ == "__main__":
    update_notebooks_rst_files()

