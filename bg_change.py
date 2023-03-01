
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import pixellib
from pixellib.tune_bg import alter_bg

st.set_page_config(layout="wide", page_title="Image Background Changer")

st.write("## Swap image background")
st.write(
    ":dog: Upload image to change the background. :grin:"
)
st.write(
    ":dog: Upload new background. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload and download :gear:")


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def swap_bg(img, bg):
    change_bg = alter_bg()
    change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    res = change_bg.change_bg_img(f_image_path = img,b_image_path = bg)
    return res

def change_bg(img, background):
    image = Image.open(img)
    bg = Image.open(background)
    col1.write("Original Image :camera:")
    col1.image(image)

    res = swap_bg(img, bg)
    col2.write("Image New BG :wrench:")
    col2.image(bg)
    col3.write("Image with new Background :wrench:")
    col3.image(res)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download Image with new BG", convert_image(res), "chg_bg.png", "image/png")


col1, col2, col3 = st.columns(3)
img = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
bg = st.sidebar.file_uploader("Upload Background", type=["png", "jpg", "jpeg"])

change_bg(img, bg)
