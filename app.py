import streamlit as st
import os
import io
from PIL import Image


# Function to resize image
def resize_image(input_file, width=None, height=None):
    img = Image.open(input_file)
    output_buffer = io.BytesIO()
    img_format = input_file.name.split(".")[-1].lower()
    
    # Resize the image
    if width is not None and height is not None:
        img = img.resize((width, height))
    elif width is not None:
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
    elif height is not None:
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), Image.ANTIALIAS)
    
    img.save(output_buffer, format='JPEG')
    return output_buffer.getvalue()


page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: rgba(255,244,218,1);
background-size: cover
}
</style>
"""

# Define page for image resizing
def image_resizing():
    st.title("GAMBAR CILIK")
    
    # Input
    st.write("""
    ### Dimensi
    """)
    new_width = st.number_input("Masukkan lebar baru (px)", min_value=1)
    new_height = st.number_input("Masukkan panjang baru (px)", min_value=1)
    
    # Main content
    st.write("""
    ## Pilih gambar yang ingin di-resize!
    """)
    
    # File upload - image
    image_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])
    
    if image_file is not None:
        st.image(image_file, caption="Gambar Diupload", use_column_width=True)
        st.write("Detail Gambar Diupload:")
        image_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
        st.write(image_details)
        
        # Resize image button
        if st.button("Resize Gambar"):
            st.write("Resizing Gambar...")
            resized_image = resize_image(image_file, width=new_width, height=new_height)
            st.success("Resize gambar berhasil!")
            
            # Download button for resized image
            st.write("### Download Gambar")
            image_download_button_str = f"Download Gambar"
            st.download_button(label=image_download_button_str, data=resized_image, file_name=f"{os.path.splitext(image_file.name)[0]}_resized.jpg", mime="image/jpeg", key=None)

# Run the app
if __name__ == '__main__':
    image_resizing()
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.write("Created by Handal Khomsyat - 121705061")
