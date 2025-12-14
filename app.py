import streamlit as st
import torch
import numpy as np
import cv2
from PIL import Image
import segmentation_models_pytorch as smp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# <<< BUILD MODEL >>>
def build_model():
    model = smp.Unet(
        encoder_name="efficientnet-b7",
        encoder_weights="imagenet",
        in_channels=3,
        classes=1,
        activation='sigmoid',
    )
    return model

model = build_model()
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.to(device)
model.eval()

st.title("Brain Tumor Segmentation")
uploaded_file = st.file_uploader("Upload MRI image", type=["jpg","png","jpeg","tif"])

IMG_SIZE = 240  # <-- THAY BẰNG KÍCH THƯỚC IMAGE GỐC CỦA BẠN

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)

    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    input_tensor = torch.from_numpy(img_resized/255.0).permute(2,0,1).float().unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(input_tensor).cpu().numpy()[0][0]

    mask = (pred > 0.4).astype(np.uint8)
    mask_255 = mask * 255

    overlay = img_resized.copy()
    overlay[mask == 1] = [255, 0, 0]

    # 🔘 TOGGLE
    show_overlay = st.checkbox("🔴 Show tumor overlay", value=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(img_resized, caption="Original Image", use_container_width=True)

    with col2:
        st.image(mask_255, caption="Predicted Mask (Binary)", use_container_width=True)

    with col3:
        if show_overlay:
            st.image(overlay, caption="Overlay Mask on Image", use_container_width=True)
        else:
            st.image(img_resized, caption="Overlay OFF (Original Image)", use_container_width=True)
