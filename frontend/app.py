import streamlit as st
from datetime import datetime
import fitz
from pathlib import Path

from frontend.services.api_client import (
    upload_documents,
    process_submission,
    get_submission_history,
    get_submission_result
)

st.set_page_config(
    page_title="Dependent Verification Portal",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Dependent Verification Portal")
st.caption("Intelligent Document Processing System")

st.divider()


st.header("New Dependent Verification Submission")

# Employee and dependent information
with st.form("submission_form"):

    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input("Employee ID")

    with col2:
        dependent_name = st.text_input("Dependent Name")

    relationship = st.selectbox(
        "Relationship",
        ["Spouse", "Child", "Adopted Child", "Other"]
    )

    submit = st.form_submit_button(
        "Upload Documents",
        type="primary"
    )

# File uploader outside the form
uploaded_files = st.file_uploader(
    "Upload Supporting Documents",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="document_uploader"
)

# Preview selected documents
if uploaded_files:

    st.subheader("Selected Documents")

    for index, file in enumerate(uploaded_files):

        with st.expander(file.name, expanded=True):

            file_bytes = file.getvalue()

            st.caption(
                f"Size: {file.size / 1024:.2f} KB"
            )

            file_extension = Path(file.name).suffix.lower()

            # Image preview
            if file_extension in [".jpg", ".jpeg", ".png"]:

                st.image(
                    file_bytes,
                    caption=file.name,
                    use_container_width=True
                )

            # PDF preview
            elif file_extension == ".pdf":

                try:
                    with fitz.open(
                        stream=file_bytes,
                        filetype="pdf"
                    ) as pdf_document:

                        total_pages = len(pdf_document)

                        st.info(
                            f"PDF document | {total_pages} pages"
                        )

                        # Preview first three pages
                        preview_pages = min(total_pages, 3)

                        for page_index in range(preview_pages):

                            page = pdf_document[page_index]

                            pixmap = page.get_pixmap(
                                matrix=fitz.Matrix(1.5, 1.5),
                                alpha=False
                            )

                            st.image(
                                pixmap.tobytes("png"),
                                caption=f"Page {page_index + 1}",
                                use_container_width=True
                            )

                        if total_pages > 3:
                            st.caption(
                                f"{total_pages - 3} additional pages "
                                "not displayed in preview."
                            )

                except Exception as error:
                    st.error(
                        f"Unable to preview PDF: {error}"
                    )

                st.download_button(
                    "Download PDF",
                    data=file_bytes,
                    file_name=file.name,
                    mime="application/pdf",
                    key=f"pdf_{index}"
                )


# Upload action
if submit:

    if not employee_id or not dependent_name:
        st.error("Please enter Employee ID and Dependent Name.")

    elif not uploaded_files:
        st.error("Please upload at least one document.")

    else:
        try:
            with st.spinner("Uploading documents..."):

                response = upload_documents(
                    employee_id,
                    dependent_name,
                    relationship,
                    uploaded_files
                )

            st.session_state["submission_id"] = (
                response["data"]["submission_id"]
            )

            st.success("Documents uploaded successfully!")

        except Exception as error:
            st.error(f"Upload failed: {error}")


if "submission_id" in st.session_state:

    submission_id = st.session_state["submission_id"]

    st.divider()

    st.subheader("Submission Details")

    st.code(submission_id)

    if st.button("Start Document Processing", type="primary"):

        try:
            with st.spinner(
                "Running preprocessing, OCR, classification and extraction..."
            ):

                result = process_submission(submission_id)

            st.session_state["processing_result"] = result

            st.success("Document processing completed!")

        except Exception as error:
            st.error(f"Processing failed: {error}")



if "processing_result" in st.session_state:

    result = st.session_state["processing_result"]["data"]

    st.divider()
    st.header("📊 Document Processing Results")

    # Submission summary
    st.subheader("Submission Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Documents",
            result["total_documents"]
        )

    with col2:
        st.metric(
            "Submission Status",
            result["submission_status"]
        )

    with col3:
        st.metric(
            "Submission ID",
            result["submission_id"]
        )

    st.divider()

    # Individual document results
    for document in result["documents"]:

        processing = document["processing"]
        extraction = processing["extraction"]
        preprocessing = document["preprocessing"]

        with st.container(border=True):

            st.subheader(document["original_filename"])

            # Classification
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Document Type**")
                st.success(processing["document_type"])

            with col2:
                st.write("**Classification Status**")
                st.success(
                    processing["classification"]["classification_status"]
                )

            st.write(
                f"**Total Pages:** {document['total_pages']}"
            )

            st.divider()

            # Extracted fields
            st.subheader("Extracted Information")

            fields = extraction["extracted_fields"]

            display_fields = {
                key.replace("_", " ").title():
                value if value is not None else "Not detected"
                for key, value in fields.items()
            }

            st.table(display_fields)

            # Missing fields
            missing_fields = extraction["missing_fields"]

            if missing_fields:
                st.warning(
                    "Missing fields: "
                    + ", ".join(missing_fields)
                )
            else:
                st.success("All expected fields extracted.")

            st.divider()

            # OCR confidence
            st.subheader("OCR Confidence")

            all_scores = []

            for page in processing["ocr_pages"]:
                for block in page["text_blocks"]:
                    score = block.get("confidence")
                    if score is not None:
                        all_scores.append(score)

            if all_scores:
                average_confidence = (
                    sum(all_scores) / len(all_scores)
                ) * 100

                st.metric(
                    "Average OCR Confidence",
                    f"{average_confidence:.2f}%"
                )

                st.progress(
                    min(1.0, max(0.0, average_confidence / 100))
                )

            else:
                st.info("No OCR confidence scores available.")

            st.divider()

            # Document quality
            st.subheader("Document Quality")

            for page in preprocessing["pages"]:

                st.write(f"**Page {page['page_number']}**")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        "Resolution:",
                        page["resolution_status"]
                    )

                with col2:
                    st.write(
                        "Brightness:",
                        page["brightness_status"]
                    )

            st.divider()

            # OCR text
            with st.expander("View Complete OCR Text"):

                for page in processing["ocr_pages"]:

                    st.text_area(
                        f"Page {page['page_number']}",
                        page["full_text"],
                        height=250,
                        key=(
                            f"{document['document_id']}_"
                            f"ocr_{page['page_number']}"
                        )
                    )


st.divider()

st.header("📁 Submission History")

if st.button("Refresh Submission History"):

    try:
        history_response = get_submission_history()
        st.session_state["submission_history"] = history_response["data"]

    except Exception as error:
        st.error(f"Unable to load history: {error}")


# Load history automatically on first visit
if "submission_history" not in st.session_state:

    try:
        history_response = get_submission_history()
        st.session_state["submission_history"] = history_response["data"]

    except Exception as error:
        st.error(f"Unable to load history: {error}")


if "submission_history" in st.session_state:

    submissions = st.session_state["submission_history"]

    st.metric("Total Submissions", len(submissions))

    if not submissions:
        st.info("No submissions found.")

    else:

        for submission in submissions:

            created_at = datetime.fromisoformat(
                submission["created_at"]
            ).astimezone().strftime("%d %b %Y, %I:%M %p")

            with st.expander(
                f"{submission['submission_id']} | "
                f"{submission['total_documents']} Documents"
            ):

                st.write("**Created At:**", created_at)

                st.write("**Documents:**")
                for document_name in submission["document_names"]:
                    st.write(f"- {document_name}")

                # NEW:View previous processing results
                if st.button(
                    "View Processing Results",
                    key=f"view_{submission['submission_id']}"
                ):
                    try:
                        historical_result = get_submission_result(
                            submission["submission_id"]
                        )

                        st.session_state["processing_result"] = historical_result

                        st.success("Previous processing results loaded!")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Unable to retrieve results: {error}")