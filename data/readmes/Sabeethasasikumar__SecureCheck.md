PROJECT SUMMARY:
        The Secure Check Dashboard project is a data analytics tool created with Python, Streamlit, and MySQL (TiDB Cloud). It aims to examine police stop data and deliver essential insights via an interactive web interface. The system fetches entries straight from the database and shows pertinent details like total stops, arrests, warnings, and additional related statistics. It also offers features to execute analytical SQL queries and create predictions based on user contributions

ESTABLISHMENT AND IMPLEMENTATION OF THE PROJECT:

  Establish the primary directory:
      Establish a directory called DigitalLedger to keep all the project documents. This will serve as the primary project foElder.

  Generate subdirectories:
      Within the DigitalLedger directory, establish the subsequent subfolders to arrange your files:
      dashboard/ → This directory holds the primary Streamlit file (App.py), which operates the dashboard.
      Scripts/ → This directory contains the SSL certificate file (isrgrootx1.pem) utilized for database connectivity.
      data/ → This folder is available for you to keep your datasets if required.

  Include your primary Streamlit file:
      Within the dashboard directory, insert your primary application file titled App.py.
      This document includes the code necessary for connecting to the database and operating the Streamlit dashboard.

  Execute the project
      Launch the terminal within the DigitalLedger folder.
      Enable your virtual environment (if it has been set up).
      Execute the Streamlit application with the following command:
      streamlit run dashboard/App.py

Streamlit will display a local URL (such as http://localhost:8501). Access it in your browser to see the dashboard
