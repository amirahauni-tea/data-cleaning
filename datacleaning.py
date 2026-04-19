import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="wide")

st.title("🧹 Data Cleaning App")
st.write("Upload your dataset and clean it easily!")

# =========================
# Upload File
# =========================
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # =========================
        # Store Original & Cleaned Data
        # =========================
        if "original_data" not in st.session_state:
            st.session_state.original_data = data.copy()

        if "cleaned_data" not in st.session_state:
            st.session_state.cleaned_data = data.copy()

        original_df = st.session_state.original_data
        df = st.session_state.cleaned_data.copy()

        # =========================
        # Data Preview (ORIGINAL)
        # =========================
        st.subheader("📊 Original Data Preview")

        preview_df = original_df.copy()
        bool_cols = preview_df.select_dtypes(include=['bool']).columns
        preview_df[bool_cols] = preview_df[bool_cols].astype('str')

        st.dataframe(preview_df)

        # =========================
        # Missing Values
        # =========================
        st.subheader("❗ Missing Values")
        missing = df.isnull().sum()
        st.dataframe(missing[missing > 0])

        # =========================
        # Duplicate Records
        # =========================
        st.subheader("🔁 Duplicate Records")
        duplicates = df.duplicated().sum()
        st.write(f"Total Duplicate Rows: {duplicates}")

        # =========================
        # Buttons Section
        # =========================
        col1, col2, col3 = st.columns(3)

        # Drop Missing
        with col1:
            if st.button("🗑️ Drop Missing Values"):
                st.session_state.cleaned_data = df.dropna()
                st.success("Missing values removed!")

        # Fill Missing
        numeric_method = st.selectbox(
            "💠 Choose Your Numeric Fill Method 💠",
            ["Mean", "Mode"]
        )

        with col2:
            if st.button("⚙️ Fill Missing Values"):
                df = df.copy()

                for col in df.columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        if numeric_method == "Mean":
                            df[col] = df[col].fillna(df[col].mean())
                        else:
                            if df[col].mode().empty:
                                df[col] = df[col].fillna(0)
                            else:
                                df[col] = df[col].fillna(df[col].mode()[0])
                    else:
                        df[col] = df[col].fillna("Unknown")

                st.session_state.cleaned_data = df
                st.success("Missing values handled!")

        # Remove Duplicates
        with col3:
            if st.button("🧹 Remove Duplicates"):
                st.session_state.cleaned_data = df.drop_duplicates()
                st.success("Duplicates removed!")

        # =========================
        # Cleaned Data Preview (FULL DATA)
        # =========================
        st.subheader("🧼 Cleaned Data Preview (Full Dataset)")

        cleaned_df = st.session_state.cleaned_data
        st.dataframe(cleaned_df)

        # =========================
        # Summary
        # =========================
        st.write("### 🔍 Changes Summary")
        st.write(f"Rows before: {original_df.shape[0]} | Rows after: {cleaned_df.shape[0]}")
        st.write(f"Columns: {cleaned_df.shape[1]}")

        # =========================
        # Download
        # =========================
        st.subheader("⬇️ Download Cleaned File")

        csv = cleaned_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")