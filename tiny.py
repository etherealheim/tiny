import streamlit as st
from PIL import Image
import io
import os
import zipfile
import tempfile

def compress_image(image, quality=85):
    buffered = io.BytesIO()
    image.save(buffered, format=image.format, optimize=True, quality=quality)
    return buffered

def main():
    st.title("Multi-Image Compressor")
    st.write("Upload one or more images to compress them!")

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # Compression quality slider
        quality = st.slider("Compression quality", 0, 100, 85)

        if st.button("Compress Images"):
            # Create a temporary directory to store compressed images
            with tempfile.TemporaryDirectory() as temp_dir:
                compressed_files = []
                total_original_size = 0
                total_compressed_size = 0

                for uploaded_file in uploaded_files:
                    # Open and compress each image
                    image = Image.open(uploaded_file)
                    original_size = uploaded_file.size
                    total_original_size += original_size

                    compressed_image = compress_image(image, quality)
                    compressed_size = compressed_image.getbuffer().nbytes
                    total_compressed_size += compressed_size

                    # Save compressed image to temporary directory
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(compressed_image.getbuffer())
                    compressed_files.append(temp_file_path)

                    # Display compression results for each image
                    st.write(f"Compressed {uploaded_file.name}")
                    st.write(f"Original size: {original_size/1024:.2f} KB")
                    st.write(f"Compressed size: {compressed_size/1024:.2f} KB")
                    st.write(f"Compression ratio: {compressed_size/original_size:.2%}")
                    st.write("---")

                # Display total compression results
                st.write("Total Compression Results:")
                st.write(f"Total original size: {total_original_size/1024:.2f} KB")
                st.write(f"Total compressed size: {total_compressed_size/1024:.2f} KB")
                st.write(f"Overall compression ratio: {total_compressed_size/total_original_size:.2%}")

                # Create zip file
                zip_path = os.path.join(temp_dir, "compressed_images.zip")
                with zipfile.ZipFile(zip_path, "w") as zip_file:
                    for file in compressed_files:
                        zip_file.write(file, os.path.basename(file))

                # Provide download button for zip file
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="Download compressed images (ZIP)",
                        data=f.read(),
                        file_name="compressed_images.zip",
                        mime="application/zip"
                    )

if __name__ == "__main__":
    main()