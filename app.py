import streamlit as st
from datetime import datetime

from src.predict import predict_image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HydroVision",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌊 HydroVision")

    st.caption("AI-Powered Flood Detection & Risk Assessment")

    st.divider()

    # --------------------------------------------------------
    # NEW ANALYSIS
    # --------------------------------------------------------

    if st.button(
        "＋ New Analysis",
        use_container_width=True
    ):
        st.session_state.result = None
        st.session_state.uploaded_name = None
        st.rerun()

    # --------------------------------------------------------
    # RECENT
    # --------------------------------------------------------

    st.subheader("Recent")

    if not st.session_state.history:

        st.caption("No analyses yet.")

    else:

        for item in reversed(
            st.session_state.history[-8:]
        ):
            st.caption("• " + item)

    st.divider()

    # --------------------------------------------------------
    # ABOUT HYDROVISION
    # --------------------------------------------------------

    with st.expander("About HydroVision"):

        st.write(
            "HydroVision is an AI-powered flood detection "
            "system that analyzes satellite imagery to "
            "identify possible flood-affected regions."
        )

    # --------------------------------------------------------
    # AI SYSTEM
    # --------------------------------------------------------

    with st.expander("AI System"):

        st.write(
            """
            Model: U-Net

            Framework: TensorFlow / Keras

            Input Size: 256 × 256

            Task: Binary Segmentation
            """
        )

    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    with st.expander("How It Works"):

        st.write(
            """
            1. Upload a satellite image

            2. The image is preprocessed

            3. The U-Net model predicts flood regions

            4. Flood coverage is calculated

            5. A risk level is generated

            6. A recommendation is provided
            """
        )

    # --------------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------------

    with st.expander("Model Information"):

        st.write("Model: U-Net")

        st.write("Input: 256 × 256 satellite image")

        st.write("Framework: TensorFlow / Keras")

        st.write("Task: Binary flood segmentation")

        st.write("Segmentation threshold: 0.50")


# ============================================================
# CENTERED HEADER
# ============================================================

left, center, right = st.columns([1, 2, 1])

with center:

    st.title("🌊 HydroVision")

    st.caption(
        "AI-Powered Satellite Flood Detection & Risk Assessment"
    )


# ============================================================
# WELCOME MESSAGE
# ============================================================

if st.session_state.result is None:

    left, center, right = st.columns([1, 3, 1])

    with center:

        st.subheader(
            "What can I help you analyze?"
        )

        st.write(
            "Upload a satellite image and let HydroVision "
            "detect possible flood-affected regions."
        )


st.write("")


# ============================================================
# CENTERED UPLOAD AREA
# ============================================================

left, center, right = st.columns([2, 5, 2])

with center:

    upload_col, button_col = st.columns(
        [7, 1],
        vertical_alignment="bottom"
    )

    # --------------------------------------------------------
    # IMAGE UPLOAD
    # --------------------------------------------------------

    with upload_col:

        uploaded_file = st.file_uploader(
            "📎 Upload satellite image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp",
                "tif",
                "tiff"
            ],
            label_visibility="collapsed"
        )

    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------

    with button_col:

        analyze = st.button(
            "➤",
            use_container_width=True,
            help="Analyze satellite image"
        )


# ============================================================
# ANALYZE IMAGE
# ============================================================

if uploaded_file is not None and analyze:

    with st.spinner(
        "HydroVision is analyzing the satellite image..."
    ):

        try:

            result = predict_image(uploaded_file)

            st.session_state.result = result

            st.session_state.uploaded_name = (
                uploaded_file.name
            )

            # ------------------------------------------------
            # ADD TO HISTORY
            # ------------------------------------------------

            timestamp = datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )

            history_item = (
                f"{uploaded_file.name} — {timestamp}"
            )

            st.session_state.history.append(
                history_item
            )

            st.rerun()

        except Exception as e:

            st.error(
                "Unable to analyze the uploaded image."
            )

            with st.expander("Technical Details"):

                st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result is not None:

    result = st.session_state.result

    # ========================================================
    # AI RESPONSE
    # ========================================================

    st.divider()

    st.subheader("HydroVision")

    st.write(
        "I've analyzed the satellite image using the "
        "trained U-Net flood segmentation model."
    )


    # ========================================================
    # DETECTION RESULT
    # ========================================================

    st.subheader("Flood Detection Result")

    image_col1, image_col2 = st.columns(
        2,
        gap="large"
    )

    # --------------------------------------------------------
    # ORIGINAL IMAGE
    # --------------------------------------------------------

    with image_col1:

        st.image(
            result["original"],
            caption="Original Satellite Image",
            width=450
        )

    # --------------------------------------------------------
    # FLOOD DETECTION
    # --------------------------------------------------------

    with image_col2:

        st.image(
            result["overlay"],
            caption="AI Flood Detection",
            width=450
        )


    # ========================================================
    # FLOOD ANALYSIS
    # ========================================================

    st.subheader("Flood Analysis")

    stat1, stat2 = st.columns(2)

    # --------------------------------------------------------
    # FLOOD COVERAGE
    # --------------------------------------------------------

    with stat1:

        st.metric(
            "🌊 Flood Coverage",
            result["flood_percentage"]
        )

    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    with stat2:

        risk = result["risk_level"]

        if "low" in risk.lower():

            st.success(
                f"⚠️ Risk Level: {risk}"
            )

        elif "moderate" in risk.lower():

            st.warning(
                f"⚠️ Risk Level: {risk}"
            )

        else:

            st.error(
                f"⚠️ Risk Level: {risk}"
            )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    st.subheader("💡 Recommendation")

    st.write(
        result["recommendation"]
    )


    # ========================================================
    # FLOOD MASK
    # ========================================================

    with st.expander("View Flood Segmentation Mask"):

        st.image(
            result["mask"],
            caption="Predicted Flood Mask",
            width=450
        )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report = f"""
HydroVision AI Report
==============================

Image : {st.session_state.uploaded_name}

Flood Coverage : {result["flood_percentage"]}

Risk Level : {result["risk_level"]}

------------------------------

Recommendation

{result["recommendation"]}

------------------------------

Generated by HydroVision
AI-Powered Satellite Flood Detection
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="HydroVision_Report.txt",
        mime="text/plain"
    )
