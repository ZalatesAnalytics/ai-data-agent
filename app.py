import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st
#start here app.py
st.set_page_config(page_title="DDS Analyzer", layout="wide")
st.title("Dietary Diversity Score (DDS) — Analysis & Report")

# File uploader
uploaded = st.file_uploader("Upload your data file (CSV or Excel)", type=["csv", "xls", "xlsx"])

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".csv"):
            result_df = pd.read_csv(uploaded)
        else:
            result_df = pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"Failed to read uploaded file: {e}")
        st.stop()

    if 'dds_computed' not in result_df.columns:
        st.error("Column 'dds_computed' not found. Please include a numeric 'dds_computed' column.")
        st.stop()

    # Identify categorical columns
    all_cat = result_df.select_dtypes(include=['object', 'category']).columns.tolist()
    all_cat += [c for c in result_df.columns if result_df[c].nunique() <= 20 and c not in all_cat]
    all_cat = list(dict.fromkeys(all_cat))  # unique

    # Summary by categorical variables
    st.subheader('Summary by selected categorical variables')
    cat_cols = st.multiselect('Choose categorical columns for breakdown (optional)', options=all_cat)

    if len(cat_cols) == 0:
        st.write('No categorical breakdown chosen — showing overall distribution')
        st.write(result_df['dds_computed'].describe())
    else:
        group_cols = cat_cols
        agg = result_df.groupby(group_cols)['dds_computed'].agg(['mean', 'std', 'count']).reset_index()
        st.dataframe(agg)

        # Plots (up to 3 categorical columns)
        st.subheader('Plots')
        to_plot = cat_cols[:3]
        for cat in to_plot:
            st.markdown(f'**DDS by {cat}**')
            fig, ax = plt.subplots()
            grouped = result_df.groupby(cat)['dds_computed'].agg(['mean', 'std', 'count']).sort_values('mean')
            grouped['mean'].plot(kind='bar', ax=ax)
            ax.set_ylabel('Mean DDS')
            ax.set_xlabel(cat)
            ax.set_title(f'Mean DDS by {cat}')
            st.pyplot(fig)
            plt.close(fig)

    # Download processed CSV
    st.subheader('Download processed data')
    to_download = result_df.copy()
    csv_bytes = to_download.to_csv(index=False).encode('utf-8')
    st.download_button('Download processed CSV', data=csv_bytes, file_name='processed_dds.csv', mime='text/csv')

    # Generate PDF report
    st.subheader('Download PDF report')
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        # Overall DDS distribution
        fig, ax = plt.subplots()
        ax.hist(result_df['dds_computed'].dropna(), bins=12)
        ax.set_title('DDS distribution')
        ax.set_xlabel('DDS')
        ax.set_ylabel('Frequency')
        pdf.savefig(fig)
        plt.close(fig)

        # Boxplots by categorical columns (up to 4)
        for cat in cat_cols[:4]:
            fig, ax = plt.subplots()
            result_df.boxplot(column='dds_computed', by=cat, ax=ax)
            ax.set_title(f'DDS by {cat}')
            plt.suptitle('')
            pdf.savefig(fig)
            plt.close(fig)

    pdf_buffer.seek(0)
    st.download_button('Download PDF report', data=pdf_buffer, file_name='dds_report.pdf', mime='application/pdf')

    st.success('Report ready')

else:
    st.info('Upload a data file to get started.')
