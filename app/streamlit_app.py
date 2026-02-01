import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH so `import src...` works in Streamlit
ROOT = Path(__file__).resolve().parents[1]  # folder containing src/
sys.path.insert(0, str(ROOT))

import os
import streamlit as st
from PIL import Image

from streamlit_drawable_canvas import st_canvas

from src.capture.screenshot_capture import capture_fullscreen
from src.pipeline import run_pipeline


st.set_page_config(page_title="OCR + NLP Suite", layout="wide")
st.title("OCR + NLP End-to-End (Tesseract + EasyOCR + NLP)")

# ---------------------------
# Session state initialization
# ---------------------------
if "captured_image_path" not in st.session_state:
    st.session_state.captured_image_path = None  # for full-screen auto-capture

if "snip_fullscreen_path" not in st.session_state:
    st.session_state.snip_fullscreen_path = None  # base screenshot for snipping

if "snipped_image_path" not in st.session_state:
    st.session_state.snipped_image_path = None  # cropped region image path

# ---------------------------
# Layout
# ---------------------------
col1, col2 = st.columns([1, 1])

# ---------------------------
# LEFT: Input
# ---------------------------
with col1:
    st.subheader("Input")

    mode = st.radio(
        "Choose input mode",
        ["Upload image", "Auto-capture full screen", "Snipping (select area)"],
        horizontal=False
    )

    image_path = None

    # ---------------------------
    # Mode 1: Upload image
    # ---------------------------
    if mode == "Upload image":
        uploaded = st.file_uploader("Upload screenshot/image (png/jpg)", type=["png", "jpg", "jpeg"])
        if uploaded:
            os.makedirs("data/input", exist_ok=True)
            image_path = os.path.join("data/input", uploaded.name)
            with open(image_path, "wb") as f:
                f.write(uploaded.read())

            st.image(image_path, caption="Uploaded image", use_container_width=True)

            # Clear other modes
            st.session_state.captured_image_path = None
            st.session_state.snip_fullscreen_path = None
            st.session_state.snipped_image_path = None

    # ---------------------------
    # Mode 2: Auto-capture full screen
    # ---------------------------
    elif mode == "Auto-capture full screen":
        if st.button("Capture full screen now"):
            os.makedirs("data/input", exist_ok=True)
            st.session_state.captured_image_path = capture_fullscreen(out_dir="data/input")
            st.success(f"Captured: {st.session_state.captured_image_path}")

            # Clear snip mode state
            st.session_state.snip_fullscreen_path = None
            st.session_state.snipped_image_path = None

        if st.session_state.captured_image_path:
            image_path = st.session_state.captured_image_path
            st.image(image_path, caption="Captured screenshot", use_container_width=True)
        else:
            st.info("Click **Capture full screen now** first, then run OCR + NLP.")

    # ---------------------------
    # Mode 3: Snipping (select area)
    # ---------------------------
    else:
        st.markdown("### Snipping (Select a rectangle area)")
        st.caption("Workflow: Capture screen → draw rectangle → OCR only that cropped region.")

        # Step 1: Capture a base screenshot to snip from
        if st.button("Capture screen for snipping"):
            os.makedirs("data/input", exist_ok=True)
            st.session_state.snip_fullscreen_path = capture_fullscreen(out_dir="data/input")
            st.session_state.snipped_image_path = None  # reset previous crop
            st.success(f"Captured base screen: {st.session_state.snip_fullscreen_path}")

            # Clear full-screen mode state
            st.session_state.captured_image_path = None

        # Step 2: Draw rectangle and crop
        if st.session_state.snip_fullscreen_path:
            base_img = Image.open(st.session_state.snip_fullscreen_path).convert("RGB")

            st.info("Draw a rectangle over the text area you want to OCR. (You can redraw to update.)")

            # For performance/UX, you can optionally scale down very large screens
            # but here we keep 1:1 for accurate coordinates.
            canvas_result = st_canvas(
                fill_color="rgba(255, 0, 0, 0.15)",
                stroke_width=2,
                stroke_color="#FF0000",
                background_image=base_img,
                update_streamlit=True,
                height=base_img.height,
                width=base_img.width,
                drawing_mode="rect",
                key="snip_canvas",
            )

            # Extract the most recent rectangle and crop
            if canvas_result.json_data and canvas_result.json_data.get("objects"):
                rect = canvas_result.json_data["objects"][-1]

                left = int(rect.get("left", 0))
                top = int(rect.get("top", 0))
                width = int(rect.get("width", 0))
                height = int(rect.get("height", 0))

                # Guard against invalid rectangles
                if width > 5 and height > 5:
                    right = min(left + width, base_img.width)
                    bottom = min(top + height, base_img.height)
                    left = max(left, 0)
                    top = max(top, 0)

                    cropped = base_img.crop((left, top, right, bottom))

                    os.makedirs("data/input", exist_ok=True)
                    cropped_path = os.path.join("data/input", "snipped_region.png")
                    cropped.save(cropped_path)

                    st.session_state.snipped_image_path = cropped_path
                    image_path = cropped_path  # this is what OCR will use

                    st.success(f"Snip saved: {cropped_path}")
                    st.image(cropped, caption="Cropped region (OCR will run on this)", use_container_width=True)
                else:
                    st.warning("Rectangle too small. Please draw a larger area around the text.")
            else:
                st.caption("No rectangle drawn yet.")

        else:
            st.info("Click **Capture screen for snipping** first.")

        # In snip mode, OCR uses snipped_image_path (if available)
        if st.session_state.snipped_image_path:
            image_path = st.session_state.snipped_image_path

# ---------------------------
# RIGHT: Settings + Run
# ---------------------------
with col2:
    st.subheader("Settings")

    ocr_engine = st.selectbox("OCR Engine", ["tesseract", "easyocr"], index=0)

    tess_lang = st.text_input(
        "Tesseract languages (printed text)",
        value="eng",
        help="Examples: eng | fra | eng+fra | eng+hin"
    )

    easy_langs = st.text_input(
        "EasyOCR languages (handwritten)",
        value="en",
        help="Comma separated: en,fr,hi"
    )

    run_nlp = st.toggle("Run NLP (summary, NER, keywords)", value=True)

    # Disable run button until we have a valid image_path
    run_clicked = st.button(
        "Run OCR + NLP",
        type="primary",
        disabled=not bool(image_path)
    )

    if run_clicked:
        try:
            with st.spinner("Running OCR + NLP..."):
                out_txt, out_json, result = run_pipeline(
                    image_path=image_path,
                    ocr_engine=ocr_engine,
                    tesseract_lang=tess_lang.strip(),
                    easyocr_langs=tuple([x.strip() for x in easy_langs.split(",") if x.strip()]),
                    run_nlp=run_nlp
                )

            st.success("Done!")
            st.write("**Text output:**", out_txt)
            st.write("**JSON output:**", out_json)

            st.subheader("Extracted Text")
            st.text_area("OCR Text", value=result.get("text", ""), height=220)

            if run_nlp:
                st.subheader("Detected Language")
                st.write(result.get("language", "unknown"))

                st.subheader("Summary")
                st.text_area("Summary", value=result.get("summary", ""), height=140)

                st.subheader("Keywords")
                st.write(result.get("keywords", []))

                st.subheader("Entities")
                st.json(result.get("entities", []))

            # Download buttons
            try:
                with open(out_txt, "rb") as f:
                    st.download_button(
                        "Download .txt",
                        f,
                        file_name=os.path.basename(out_txt),
                        mime="text/plain"
                    )
            except Exception as e:
                st.warning(f"Could not load txt for download: {e}")

            try:
                with open(out_json, "rb") as f:
                    st.download_button(
                        "Download .json",
                        f,
                        file_name=os.path.basename(out_json),
                        mime="application/json"
                    )
            except Exception as e:
                st.warning(f"Could not load json for download: {e}")

        except Exception as e:
            st.error(f"Run failed: {e}")
            st.stop()

# ---------------------------
# Footer tips
# ---------------------------
st.markdown("---")
st.caption(
    "Pls Note: For best OCR accuracy, zoom text to 125–150%, use a light background, and crop tightly (Snipping mode). "
    "If you have multiple monitors, update your capture code to target the correct monitor."
)
