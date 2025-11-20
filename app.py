{
 "cells": [
  {
  
   "execution_count": 2,
   "id": "60f42d76-c9d0-48f5-b697-358a9fc79ec2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from matplotlib.backends.backend_pdf import PdfPages\n",
    "import io\n",
    "\n",
    "# First, define result_df before using it\n",
    "# You need to either load your data or create a DataFrame\n",
    "# For example:\n",
    "# Option 1: Load data from a file\n",
    "# result_df = pd.read_csv('your_data.csv')\n",
    "\n",
    "# Option 2: Create a sample DataFrame for testing\n",
    "result_df = pd.DataFrame({\n",
    "    'dds_computed': [3.5, 4.2, 2.8, 5.1, 3.9, 4.7],\n",
    "    # Add any categorical columns you need for your analysis\n",
    "    'category1': ['A', 'B', 'A', 'C', 'B', 'C'],\n",
    "    'category2': ['X', 'Y', 'X', 'Y', 'Z', 'Z']\n",
    "})\n",
    "\n",
    "# Define cat_cols (list of categorical columns)\n",
    "cat_cols = ['category1', 'category2']  # Adjust based on your actual categorical columns\n",
    "\n",
    "# Calculate overall statistics\n",
    "overall_mean = result_df['dds_computed'].mean()\n",
    "overall_sd = result_df['dds_computed'].std()\n",
    "\n",
    "# Now the rest of your code will work\n",
    "st.metric('Overall mean DDS', f\"{overall_mean:.2f}\")\n",
    "st.metric('Overall DDS SD', f\"{overall_sd:.2f}\")\n",
    "\n",
    "st.subheader('Summary by selected categorical variables')\n",
    "if len(cat_cols) == 0:\n",
    "    st.write('No categorical breakdown chosen — showing overall distribution')\n",
    "    st.write(result_df['dds_computed'].describe())\n",
    "else:\n",
    "    # group and show\n",
    "    group_cols = cat_cols\n",
    "    agg = result_df.groupby(group_cols)['dds_computed'].agg(['mean','std','count']).reset_index()\n",
    "    st.dataframe(agg)\n",
    "\n",
    "# plotting: one plot per categorical variable (if multiple, show first up to 3)\n",
    "to_plot = cat_cols[:3]\n",
    "for cat in to_plot:\n",
    "    st.markdown(f'**DDS by {cat}**')\n",
    "    fig, ax = plt.subplots()\n",
    "    grouped = result_df.groupby(cat)['dds_computed'].agg(['mean','std','count']).sort_values('mean')\n",
    "    grouped['mean'].plot(kind='bar', ax=ax)\n",
    "    ax.set_ylabel('Mean DDS')\n",
    "    ax.set_xlabel(cat)\n",
    "    ax.set_title(f'Mean DDS by {cat}')\n",
    "    st.pyplot(fig)\n",
    "\n",
    "# allow user to download processed data and an Excel report\n",
    "to_download = result_df.copy()\n",
    "csv_bytes = to_download.to_csv(index=False).encode('utf-8')\n",
    "st.download_button('Download processed CSV', data=csv_bytes, file_name='processed_dds.csv', mime='text/csv')\n",
    "\n",
    "# Create a multipage PDF report with charts\n",
    "pdf_buffer = io.BytesIO()\n",
    "with PdfPages(pdf_buffer) as pdf:\n",
    "    # Summary figure\n",
    "    fig, ax = plt.subplots()\n",
    "    ax.hist(result_df['dds_computed'].dropna(), bins=12)\n",
    "    ax.set_title('DDS distribution')\n",
    "    ax.set_xlabel('DDS')\n",
    "    ax.set_ylabel('Frequency')\n",
    "    pdf.savefig(fig)\n",
    "    plt.close(fig)\n",
    "\n",
    "    # Add breakdown plots\n",
    "    for cat in cat_cols[:4]:\n",
    "        fig, ax = plt.subplots()\n",
    "        result_df.boxplot(column='dds_computed', by=cat, ax=ax)\n",
    "        ax.set_title(f'DDS by {cat}')\n",
    "        ax.get_figure()\n",
    "        pdf.savefig(fig)\n",
    "        plt.close(fig)\n",
    "\n",
    "pdf_buffer.seek(0)\n",
    "st.download_button('Download PDF report', data=pdf_buffer, file_name='dds_report.pdf', mime='application/pdf')\n",
    "\n",
    "st.success('Report ready')"
   ]
  },
  {

  
   "id": "46578424-e2b8-464a-92e5-9fa5a3af8a96",

   "outputs": [],

  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
