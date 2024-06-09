# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to MCQ Genie! 👋")
    st.subheader('AI Assisted MCQ :blue[A]nalyzer, :red[G]enerator and :green[E]nhancer :sunglasses:', divider='rainbow')

    # st.write(st.__version__)

    mcq_options = st.radio(
     "What would you like to do?",
     ('Analyze', 'Enhance', 'Generate'),
     horizontal=True, index=2)

    if mcq_options == "Generate":

      col1, col2 = st.columns(2)
      with col1:
        program_option = st.selectbox(
        'Choose a Program',
        ('MBA', 'MCA', 'MCom'))

      with col2:
        course_option = st.selectbox(
        'Choose a Course',
        ('Marketing', 'Data Science', 'Accounting and Finance'))

      unit_option = st.selectbox(
      'Choose a Unit',
      ('Unit 1', 'Unit 2', 'Unit 3'))

      # st.radio(
      #     "Select MCQs to Analyze / Enhance",
      #     key="select_mcq",
      #     options=["All Units", "Select Unit"],
      # )
      
      st.text('Enter number of MCQs to be generated based for respective BTL and difficulty levels:')

      # Initial scorecard dataframe
      if "random_key" not in st.session_state:
        st.session_state["random_key"] = 1   
      
      if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(
            [
              {"Bloom Taxanomy Level (BTL)": "[1] Remembering", "Easy": 0, "Medium": 0, "Hard": 0},
              {"Bloom Taxanomy Level (BTL)": "[2] Understanding", "Easy": 0, "Medium": 0, "Hard": 0},
              {"Bloom Taxanomy Level (BTL)": "[3] Applying", "Easy": 0, "Medium": 0, "Hard": 0},
              {"Bloom Taxanomy Level (BTL)": "[4] Analyzing", "Easy": 0, "Medium": 0, "Hard": 0},
              {"Bloom Taxanomy Level (BTL)": "[5] Evaluating", "Easy": 0, "Medium": 0, "Hard": 0},
              {"Bloom Taxanomy Level (BTL)": "[6] Creating", "Easy": 0, "Medium": 0, "Hard": 0}
          ]
        )

      edited_df = st.data_editor(st.session_state.df,
                                  column_config={
                                  "Easy": st.column_config.Column(
                                      "Easy",
                                      help="Difficulty Level",
                                      width="small",
                                      required=True,
                                    ),
                                    "Medium": st.column_config.Column(
                                      "Medium",
                                      help="Difficulty Level",
                                      width="small",
                                      required=True,
                                    ),
                                    "Hard": st.column_config.Column(
                                      "Hard",
                                      help="Difficulty Level",
                                      width="small",
                                      required=True,
                                    )
                                  },
                                  width=1000, 
                                  hide_index=True, 
                                  key=st.session_state["random_key"])

      if not st.session_state.df.equals(edited_df):
        st.session_state.df = edited_df
        st.session_state.easy_count = edited_df['Easy'][0] + edited_df['Easy'][1] + edited_df['Easy'][2] + edited_df['Easy'][3] + edited_df['Easy'][4] + edited_df['Easy'][5]
        st.session_state.medium_count = edited_df['Medium'][0] + edited_df['Medium'][1] + edited_df['Medium'][2] + edited_df['Medium'][3] + edited_df['Medium'][4] + edited_df['Medium'][5]
        st.session_state.hard_count = edited_df['Hard'][0] + edited_df['Hard'][1] + edited_df['Hard'][2] + edited_df['Hard'][3] + edited_df['Hard'][4] + edited_df['Hard'][5]
        st.rerun()

      if 'easy_count' in st.session_state:
        col0, col1, col2, col3 = st.columns(4)
        with st.container(border=True):
          tile0 = col0.container(height=120)
          tile0.title(":hash: " + str(st.session_state.easy_count + st.session_state.medium_count + st.session_state.hard_count))
          tile1 = col1.container(height=120)
          tile1.title(":small_blue_diamond: " + str(st.session_state.easy_count))
          tile2 = col2.container(height=120)
          tile2.title(":small_orange_diamond: " + str(st.session_state.medium_count))
          tile3 = col3.container(height=120)
          tile3.title(":small_red_triangle: " + str(st.session_state.hard_count))
          
          # row1 = st.columns(3)
          # row2 = st.columns(3)

          # for col in row1 + row2:
          #     tile = col.container(height=120)
          #     tile.title(":balloon:")

      else:
        st.session_state.easy_count = 0
        st.session_state.medium_count = 0
        st.session_state.hard_count = 0
        st.rerun()

      c1, c2 = st.columns([.2,.7], gap="small")
      with c1:
          st.button("Generate", type="primary")
      with c2:
        if st.button("Reset"):
          st.text("a")
          # st.cache_data.clear()
          # st.session_state["random_key"] += 1

if __name__ == "__main__":
    run()
