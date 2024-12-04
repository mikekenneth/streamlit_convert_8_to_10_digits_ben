import streamlit as st
from helpers import process_individual_vcard


def process_vcf_file(
    infile_content, prefix_to_add, sample_only=False, sample_size: int = 200, drop_duplicates_in_vcard=True
):
    current_vcard, vcard_counter, vcard_updated = [], 0, 0
    outfile_content = ""
    for line in infile_content.split("\n"):
        line = line.replace("\n", "").replace("\r", "")
        if line.strip() == "BEGIN:VCARD":
            current_vcard = []
        elif line.strip() == "END:VCARD":
            vcard, updated_state = process_individual_vcard(current_vcard, drop_duplicates_in_vcard, prefix_to_add)
            if updated_state:
                outfile_content += "BEGIN:VCARD\n"
                outfile_content += "\n".join(vcard)
                outfile_content += "\nEND:VCARD\n"
                vcard_updated += 1
            vcard_counter += 1
            if sample_only and vcard_counter >= sample_size:
                return {"proccessed": vcard_counter, "updated": vcard_updated, "outfile_content": outfile_content}
        else:
            current_vcard.append(line)
    return {"proccessed": vcard_counter, "updated": vcard_updated, "outfile_content": outfile_content}


st.set_page_config(page_title="BJ 8 to 10 Phone Number Converter", page_icon="🇧🇯")
st.markdown("# Welcome to the 8 digits to 10 Converter for Benin Republic (BJ 🇧🇯 ) Phone Numbers")
st.markdown("## How does it work?")
st.info(
    """The VCF contains each contact as a `VCARD`.
    The tool goes through each vcard and append an additional `TEL` Number in the vcard with the `01` prefix."""
)
st.warning(
    """ **VERY IMPORTANT: THIS APPLICATION DOES NOT STORE AND SHARE YOU CONTACT DATA. You can eplore the source on github if you have doubts.**\n
    **Important**: Only Phone Numbers that has either has 8 digits OR 12 characters and startswith `+229` are updated.
    The output VCF contains only the VCARDs that where updated (appended with a new number that has the '01' prefix)"""
)
st.markdown("### To begin, follow the steps below:")
st.info(
    """
    1. Export your contact to a VCF file. (This is the default format of most Phones)
    2. Upload it here to get the converted VCF file of your Benin contacts.
    3. Import the Converted VFC File into you phone.
    4. [Optional] Merge you contacts using your phone or online tools like Google Contacts to eliminate duplicates completely.
    """
)

st.header("Example")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Original")
    st.markdown(
        """```python
BEGIN:VCARD
VERSION:2.1
N:Test;Contact;;;
FN:Test Contact
TEL;CELL:97970000
TEL;CELL:+22997970000
TEL;WORK:+112345648945
TEL;WORK:+332345648945
TEL;HOME:21000000
END:VCARD
```"""
    )

with col2:
    st.markdown("### Converted")
    st.markdown(
        """```python
BEGIN:VCARD
VERSION:2.1
N:Test;Contact;;;
FN:Test Contact
TEL;CELL:97970000
TEL;CELL:+22997970000
TEL;WORK:+112345648945
TEL;WORK:+332345648945
TEL;HOME:21000000
TEL;CELL:0197970000
TEL;CELL:+2290197970000
TEL;HOME:0121000000
END:VCARD
```"""
    )

st.subheader("Convert VCF file", anchor="upload_file")

with st.form(key="main"):
    prefix_list = ["01"]
    selected_prefix = st.selectbox(label="Prefix to Add", options=prefix_list, index=0)
    uploaded_file = st.file_uploader("Choose a VCF file", accept_multiple_files=False, type=["vcf"])
    sample_only = st.checkbox("Process only the first 200 Contacts in the VCF file", value=False)
    drop_duplicates_in_vcard = st.checkbox("Drop duplicates in VCARD", value=True)
    submit = st.form_submit_button("Generate")

if submit:
    if uploaded_file is not None:
        infile_buffer = uploaded_file.read().decode("utf-8")
        result_data = process_vcf_file(
            infile_content=infile_buffer,
            prefix_to_add=selected_prefix,
            sample_only=sample_only,
            drop_duplicates_in_vcard=drop_duplicates_in_vcard,
        )

        st.subheader("Result: Converted Contacts (VCF) file", divider="green", anchor="result")
        st.table({k: v for k, v in result_data.items() if not k == "outfile_content"})
        st.download_button(
            label=f"Download converted VCF files: {uploaded_file.name}_converted.vcf",
            data=result_data.get("outfile_content"),
            file_name=f"{uploaded_file.name}_converted.vcf",
            mime="text/vcf",
        )
