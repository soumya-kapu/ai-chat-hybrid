import streamlit as st
import numpy as np
import pandas as pd

st.title("🚀 AI Dev Stack Working")

st.write("If you see this, your setup is correct!")

data = pd.DataFrame(
    np.random.randn(10, 3),
    columns=["A", "B", "C"]
)

st.line_chart(data)
