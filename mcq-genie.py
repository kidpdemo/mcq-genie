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
import json
import time
import os
from generate_mcqs_v3 import mcq_init, mcq_generate

LOGGER = get_logger(__name__)

# global ans
# ans = [
#     {
#         "question": "What is the primary purpose of the recording function in accounting?",
#         "options": [
#             "To document financial transactions",
#             "To interpret financial outcomes",
#             "To classify financial data",
#             "To summarize financial information"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "Recording function in accounting primarily involves documenting financial transactions."
#         ],
#         "justification_btl": "The question focuses on understanding the purpose of a specific accounting function, which aligns with the Bloom's Taxonomy level: Understanding.",
#         "justification_distractors": [
#             "To interpret financial outcomes: This option confuses the role of recording with interpreting, which is not the primary purpose of the recording function.",
#             "To classify financial data: This option describes the classifying function rather than the recording function.",
#             "To summarize financial information: Summarizing is part of the summarizing function, not recording."
#         ],
#         "justification_difficulty": "The question requires understanding the core purpose of the recording function in accounting, which represents a high level of difficulty (10) for postgraduate students.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.1 INTRODUCTION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 229,
#             "prompt_tokens": 345,
#             "total_tokens": 574
#         }
#     },
#     {
#         "question": "Which function of accounting involves arranging financial transactions into categories based on similarity?",
#         "options": [
#             "Recording",
#             "Classifying",
#             "Summarizing",
#             "Interpreting"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The classifying function in accounting involves arranging transactions into categories based on similarity."
#         ],
#         "justification_btl": "This question assesses the understanding of a specific accounting function, which corresponds to the Bloom's Taxonomy level: Understanding.",
#         "justification_distractors": [
#             "Recording: Recording is about documenting transactions, not categorizing them.",
#             "Summarizing: Summarizing involves condensing information, not categorizing.",
#             "Interpreting: This option focuses on deriving meaning from financial data, which is different from classifying transactions."
#         ],
#         "justification_difficulty": "Identifying the function that involves categorizing financial transactions requires a significant understanding of accounting concepts, making it a difficulty level 10 question for postgraduate students.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.1 INTRODUCTION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 229,
#             "prompt_tokens": 345,
#             "total_tokens": 574
#         }
#     },
#     {
#         "question": "Which group of people is concerned with the solvency of a business in terms of payment ability?",
#         "options": [
#             "Owners",
#             "Creditors",
#             "Government",
#             "Suppliers"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "Creditors are interested in the solvency of a business to ensure payment ability."
#         ],
#         "justification_btl": "This question evaluates the ability to identify stakeholders concerned with business solvency, aligning with the Bloom's Taxonomy level: Understanding.",
#         "justification_distractors": [
#             "Owners: While owners have an interest in the business's financial health, creditors specifically focus on payment ability.",
#             "Government: The government is more concerned with tax compliance rather than payment solvency.",
#             "Suppliers: Suppliers provide goods and services but are not primarily focused on the business's ability to pay debts."
#         ],
#         "justification_difficulty": "Distinguishing creditors as the key group concerned with a business's payment ability requires a deep understanding of stakeholder interests, making this a difficulty level 10 question for postgraduate students.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.1 INTRODUCTION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 229,
#             "prompt_tokens": 345,
#             "total_tokens": 574
#         }
#     },
#     {
#         "question": "Why are the principles of accounting different from those of the natural sciences and mathematics?",
#         "options": [
#             "They are based on experiential evidence",
#             "They can't be derived from or proved by the laws of nature",
#             "They are universally accepted as fundamental truths",
#             "They rely solely on quantitative data"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The principles of accounting being different from natural sciences and mathematics stem from the fact that they cannot be derived from or proved by the laws of nature."
#         ],
#         "justification_btl": "The question assesses the understanding of the differentiation between accounting principles and those of natural sciences and mathematics.",
#         "justification_distractors": [
#             "This distractor is incorrect as the principles of accounting do not rely on experiential evidence.",
#             "This distractor is incorrect as the principles of accounting are not universally accepted as fundamental truths.",
#             "This distractor is incorrect as the principles of accounting do not solely rely on quantitative data."
#         ],
#         "justification_difficulty": "The question requires the ability to understand the fundamental difference between accounting principles and those of natural sciences and mathematics, therefore indicating a high level of difficulty.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.2 CONCEPTUAL FRAMEWORK OF FINANCIAL ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 979,
#             "total_tokens": 1213
#         }
#     },
#     {
#         "question": "How are liabilities defined in accounting?",
#         "options": [
#             "Legal obligations to pay for future transactions",
#             "Economic advantages owned by the enterprise",
#             "Future economic benefits controlled by an individual",
#             "Physical goods or intangible rights with economic value"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "Liabilities in accounting refer to legal obligations to pay for future transactions."
#         ],
#         "justification_btl": "The question tests the comprehension of the definition of liabilities in accounting.",
#         "justification_distractors": [
#             "This distractor is incorrect as it describes assets, not liabilities.",
#             "This distractor is incorrect as it describes assets, not liabilities.",
#             "This distractor is incorrect as it describes assets, not liabilities."
#         ],
#         "justification_difficulty": "Understanding the specific definition of liabilities in accounting requires foundational knowledge, making the question difficult.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.2 CONCEPTUAL FRAMEWORK OF FINANCIAL ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 979,
#             "total_tokens": 1213
#         }
#     },
#     {
#         "question": "What is the distinction between fixed assets and current assets in accounting?",
#         "options": [
#             "Fixed assets are tangible, while current assets are intangible",
#             "Fixed assets are used for long-term business operations, while current assets are for short-term conversion to cash",
#             "Fixed assets are liabilities, while current assets are equities",
#             "Fixed assets represent physical goods, while current assets represent services"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The distinction lies in the fact that fixed assets are purchased for long-term business operations, whereas current assets are kept for short-term conversion to cash."
#         ],
#         "justification_btl": "This question assesses the understanding of the differences between fixed assets and current assets in accounting terminology.",
#         "justification_distractors": [
#             "This distractor is incorrect as it does not accurately differentiate between fixed and current assets.",
#             "This distractor is incorrect as it confuses fixed assets with liabilities.",
#             "This distractor is incorrect as it does not accurately describe the distinction between fixed and current assets."
#         ],
#         "justification_difficulty": "Understanding the nuanced differences between fixed and current assets in accounting requires a solid grasp of the fundamental definitions, justifying the high difficulty level of this question.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.2 CONCEPTUAL FRAMEWORK OF FINANCIAL ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 979,
#             "total_tokens": 1213
#         }
#     },
#     {
#         "question": "Which accounting concept focuses on presenting financial statements that provide accurate and sufficient information to users?",
#         "options": [
#             "Cost Concept",
#             "Full Disclosure Concept",
#             "Revenue Recognition Concept",
#             "Objectivity Concept"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The Full Disclosure Concept emphasizes providing true and fair information in financial statements to users."
#         ],
#         "justification_btl": "This question aligns with the Bloom's Taxonomy level of Understanding as it tests the awareness of the Full Disclosure Concept in accounting.",
#         "justification_distractors": [
#             "The Cost Concept primarily deals with recording transactions based on cost rather than market value.",
#             "The Revenue Recognition Concept dictates when revenue should be recorded in accounting.",
#             "The Objectivity Concept focuses on recording transactions based on objective and factual evidence."
#         ],
#         "justification_difficulty": "This question is at a difficulty level of 10 as it requires the recognition and understanding of the purpose of financial statements in accounting.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.3 DIFFERENT ACCOUNTING CONCEPTS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 217,
#             "prompt_tokens": 624,
#             "total_tokens": 842
#         }
#     },
#     {
#         "question": "Which accounting principle ensures that each transaction is recorded with objective and factual evidence?",
#         "options": [
#             "Matching Concept",
#             "Business Entity Concept",
#             "Objectivity Concept",
#             "Going Concern Concept"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "The Objectivity Concept mandates that transactions must be recorded based on objective evidence."
#         ],
#         "justification_btl": "This question adheres to the Bloom's Taxonomy level of Understanding by assessing knowledge of the Objectivity Concept in accounting.",
#         "justification_distractors": [
#             "The Matching Concept involves aligning revenues with expenses to calculate a company's earnings.",
#             "The Business Entity Concept distinguishes the owner from the business as separate entities.",
#             "The Going Concern Concept is focused on the long-term viability of a business entity."
#         ],
#         "justification_difficulty": "The question's difficulty is rated 10 as it requires comprehension of the principle related to factual and objective recording of transactions.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.3 DIFFERENT ACCOUNTING CONCEPTS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 217,
#             "prompt_tokens": 624,
#             "total_tokens": 842
#         }
#     },
#     {
#         "question": "Which accounting concept emphasizes that transactions should be expressed solely in terms of money?",
#         "options": [
#             "Duality or Double Entry Concept",
#             "Accounting Period Concept",
#             "Money Measurement Concept",
#             "Cost Concept"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "The Money Measurement Concept insists that all transactions must be captured in monetary terms."
#         ],
#         "justification_btl": "This question fits into the Bloom's Taxonomy level of Understanding as it examines knowledge of expressing transactions in monetary units.",
#         "justification_distractors": [
#             "The Duality or Double Entry Concept focuses on recording both aspects of a transaction.",
#             "The Accounting Period Concept deals with dividing a business's lifespan into operational periods.",
#             "The Cost Concept involves recording transactions based on cost rather than market value."
#         ],
#         "justification_difficulty": "This question poses a difficulty level of 10 as it necessitates the understanding of expressing business events solely in monetary terms.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.3 DIFFERENT ACCOUNTING CONCEPTS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 217,
#             "prompt_tokens": 624,
#             "total_tokens": 842
#         }
#     },
#     {
#         "question": "Which accounting assumption states that a company is seen as a separate entity from its owners to keep personal transactions separate?",
#         "options": [
#             "Consistency",
#             "Going Concern Concept",
#             "Separate Business Entity",
#             "Money Measurement Concept"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "The concept of a separate business entity highlights the distinction between the company and its owners."
#         ],
#         "justification_btl": "The question requires understanding of the concept of a separate business entity and its significance in accounting practices.",
#         "justification_distractors": [
#             "'Consistency' refers to maintaining uniformity in accounting policies over time.",
#             "'Going Concern Concept' relates to the assumption of the business continuing operations in the foreseeable future.",
#             "'Money Measurement Concept' focuses on transactions that can be measured in monetary terms."
#         ],
#         "justification_difficulty": "The question assesses a fundamental accounting assumption, requiring a solid grasp of the concept, aligning it with a difficulty level of 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.4 ASSUMPTIONS AND CONVENTIONS OF ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 204,
#             "prompt_tokens": 734,
#             "total_tokens": 939
#         }
#     },
#     {
#         "question": "Which principle emphasizes that accounting information should be provided in a timely manner to be relevant for decision-making?",
#         "options": [
#             "Materiality",
#             "Consistency",
#             "Timeliness",
#             "Cost-Benefit Principle"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "The principle of 'Timeliness' stresses the importance of providing accounting information on time for relevancy."
#         ],
#         "justification_btl": "Understanding the significance of timely accounting information is crucial for effective decision-making process.",
#         "justification_distractors": [
#             "'Materiality' focuses on reporting information that impacts decision-making.",
#             "'Consistency' mandates uniformity in accounting policies over time.",
#             "'Cost-Benefit Principle' weighs the costs against benefits of using accounting principles."
#         ],
#         "justification_difficulty": "The question requires recognition of the principle relating to the timeliness of accounting information, presenting a difficulty level of 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.4 ASSUMPTIONS AND CONVENTIONS OF ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 204,
#             "prompt_tokens": 734,
#             "total_tokens": 939
#         }
#     },
#     {
#         "question": "Which accounting concept states that all transactions must be measurable in monetary terms to be recorded in accounting?",
#         "options": [
#             "Going Concern Concept",
#             "Money Measurement Concept",
#             "Consistency",
#             "Industry Practice"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The 'Money Measurement Concept' necessitates that transactions recorded in accounting must be quantifiable in monetary units."
#         ],
#         "justification_btl": "Understanding the requirement for transactions to be measurable in monetary terms for recording in accounting falls under the foundational level of comprehension.",
#         "justification_distractors": [
#             "'Going Concern Concept' relates to the continued operation of the business.",
#             "'Consistency' emphasizes maintaining uniformity in accounting policies.",
#             "'Industry Practice' focuses on accounting principles specific to different industries."
#         ],
#         "justification_difficulty": "This question assesses knowledge about the concept of measuring transactions in monetary units, corresponding to a difficulty level of 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.4 ASSUMPTIONS AND CONVENTIONS OF ACCOUNTING.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 204,
#             "prompt_tokens": 734,
#             "total_tokens": 939
#         }
#     },
#     {
#         "question": "What is the purpose of the accounting equation in the double-entry accounting system?",
#         "options": [
#             "To ensure that assets are greater than liabilities",
#             "To balance the balance sheet by equating total assets to total liabilities and shareholders' equity",
#             "To calculate the profit margin of a company",
#             "To determine the market value of a corporation"
#         ],
#         "correct_answer_index": [
#             1
#         ],
#         "justification_opt": [
#             "The purpose of the accounting equation is to balance the balance sheet by equating total assets to total liabilities and shareholders' equity."
#         ],
#         "justification_btl": "The question aligns with the Bloom's Taxonomy level: Understanding by assessing the foundational knowledge of the purpose of the accounting equation.",
#         "justification_distractors": [
#             "The incorrect options are eliminated as they do not reflect the purpose of the accounting equation.",
#             "The incorrect options do not align with the foundational understanding of the accounting equation's purpose."
#         ],
#         "justification_difficulty": "The question challenges the foundational knowledge of accounting principles while requiring a clear understanding of the purpose of the accounting equation, making it a difficulty level 10 question.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.5 ACCOUNTING EQUATIONS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 594,
#             "total_tokens": 827
#         }
#     },
#     {
#         "question": "How does shareholders\u2019 equity relate to a company's financial position?",
#         "options": [
#             "It represents the total liabilities of a business",
#             "It is the amount of money a company owes to its shareholders",
#             "It is the difference between total assets and total liabilities",
#             "It shows the profit margin for the current year"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "Shareholders' equity is the difference between total assets and total liabilities, representing the net worth of the business."
#         ],
#         "justification_btl": "This question aligns with the Bloom's Taxonomy level: Understanding as it assesses the comprehension of shareholders' equity in relation to financial position.",
#         "justification_distractors": [
#             "The distractors do not accurately reflect the relationship between shareholders' equity and a company's financial position.",
#             "The distractors do not demonstrate an understanding of the concept of shareholders' equity."
#         ],
#         "justification_difficulty": "The question challenges the understanding of the concept of shareholders' equity and its significance in assessing a company's financial position, making it a difficulty level 10 question.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.5 ACCOUNTING EQUATIONS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 594,
#             "total_tokens": 827
#         }
#     },
#     {
#         "question": "What role do liabilities play in the accounting equation?",
#         "options": [
#             "They represent the profits generated by a business",
#             "They indicate the amount that shareholders can claim from the company",
#             "They are amounts owing by the company that must be paid to creditors",
#             "They are subtracted from total assets to calculate net income"
#         ],
#         "correct_answer_index": [
#             2
#         ],
#         "justification_opt": [
#             "Liabilities are amounts owing by the company that must be paid to creditors, which is essential in the accounting equation's balance."
#         ],
#         "justification_btl": "The question targets the Bloom's Taxonomy level: Understanding by assessing the comprehension of the role of liabilities in the accounting equation.",
#         "justification_distractors": [
#             "The distractors do not accurately reflect the role of liabilities in the accounting equation.",
#             "The distractors do not align with the foundational understanding of liabilities within the accounting equation."
#         ],
#         "justification_difficulty": "The question tests the fundamental knowledge of the purpose of liabilities in the accounting equation, making it a difficulty level 10 question.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.5 ACCOUNTING EQUATIONS.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 233,
#             "prompt_tokens": 594,
#             "total_tokens": 827
#         }
#     },
#     {
#         "question": "What is the main purpose of concept of GAAP in accounting?",
#         "options": [
#             "To standardize financial reporting practices",
#             "To increase government regulations",
#             "To eliminate financial transactions",
#             "To promote tax evasion"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "The concept of GAAP aims to standardize financial reporting practices for better comparability and transparency."
#         ],
#         "justification_btl": "The question focuses on explaining the purpose of GAAP in accounting, aligning with the Bloom's Taxonomy level: Understanding.",
#         "justification_distractors": [
#             "These distractors are incorrect as they do not align with the actual purpose of GAAP in accounting."
#         ],
#         "justification_difficulty": "The question is designed to assess understanding of GAAP, which is a foundational aspect in accounting, hence the difficulty level is set at 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.8 GLOSSARY.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 187,
#             "prompt_tokens": 1093,
#             "total_tokens": 1281
#         }
#     },
#     {
#         "question": "Why are GAAP principles important for financial statement users?",
#         "options": [
#             "To provide accurate and reliable information",
#             "To complicate financial analysis",
#             "To hide financial results",
#             "To increase financial risks"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "GAAP principles are crucial for financial statement users as they ensure that the information provided is accurate and reliable."
#         ],
#         "justification_btl": "This question requires understanding of the importance of GAAP principles for users of financial statements.",
#         "justification_distractors": [
#             "The distractors present incorrect reasons that do not align with the significance of GAAP principles."
#         ],
#         "justification_difficulty": "The question is designed to evaluate the understanding of the importance of GAAP principles in providing accurate financial information, hence the difficulty level is set at 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.8 GLOSSARY.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 187,
#             "prompt_tokens": 1093,
#             "total_tokens": 1281
#         }
#     },
#     {
#         "question": "How do GAAP guidelines impact the decision-making process of businesses?",
#         "options": [
#             "By ensuring consistent and comparable financial information",
#             "By increasing financial complexity",
#             "By diminishing transparency",
#             "By promoting unethical practices"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "GAAP guidelines play a crucial role in decision-making by providing businesses with consistent and comparable financial information."
#         ],
#         "justification_btl": "This question addresses the impact of GAAP guidelines on the decision-making process of businesses, aligning with the Bloom's Taxonomy level: Understanding.",
#         "justification_distractors": [
#             "The distractors present incorrect impacts that do not align with the actual influence of GAAP guidelines."
#         ],
#         "justification_difficulty": "The question focuses on the understanding of how GAAP guidelines influence decision-making, a foundational aspect in accounting, setting the difficulty level at 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-1.8 GLOSSARY.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 187,
#             "prompt_tokens": 1093,
#             "total_tokens": 1281
#         }
#     },
#     {
#         "question": "What is the role of International Financial Reporting Standards (IFRS) in accounting?",
#         "options": [
#             "To ensure consistency, transparency, and comparability of financial statements globally",
#             "To manage day-to-day business transactions effectively",
#             "To calculate the accounting equation accurately",
#             "To determine shareholders' equity levels"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "IFRS sets common rules for consistent financial reporting globally."
#         ],
#         "justification_btl": "This question tests the understanding of the role of IFRS in ensuring consistency in financial reporting, which aligns with the 'Understanding' level of Bloom's Taxonomy.",
#         "justification_distractors": [
#             "Incorrect: Managing day-to-day business transactions is more related to operational accounting tasks, not specifically governed by IFRS.",
#             "Incorrect: Calculating the accounting equation accurately is a fundamental accounting concept but not the primary role of IFRS.",
#             "Incorrect: Determining shareholders' equity levels is a financial analysis aspect influenced by accounting standards but not the main role of IFRS."
#         ],
#         "justification_difficulty": "This question is of Difficulty Level 10 as it requires a deep understanding of the role of IFRS in financial reporting.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-Conclusion 1.7 CONCLUSION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 245,
#             "prompt_tokens": 355,
#             "total_tokens": 600
#         }
#     },
#     {
#         "question": "What does the accounting equation ensure in the double-entry accounting system?",
#         "options": [
#             "Balance sheet consistency through balanced entries",
#             "Approval of financial statements by regulators",
#             "Maximization of retained earnings for businesses",
#             "Reduction of shareholders' equity liabilities"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "The accounting equation ensures balance sheet consistency through balanced entries in the double-entry accounting system."
#         ],
#         "justification_btl": "This question assesses understanding of the purpose of the accounting equation in maintaining balance sheet accuracy, matching the 'Understanding' level of Bloom's Taxonomy.",
#         "justification_distractors": [
#             "Incorrect: Regulatory approval is related to compliance rather than the accounting equation in the system.",
#             "Incorrect: Maximizing retained earnings is a financial management objective, not a direct role of the accounting equation.",
#             "Incorrect: The accounting equation does not directly impact reducing shareholders' equity liabilities."
#         ],
#         "justification_difficulty": "This question is set at Difficulty Level 10 due to the necessity for a comprehensive understanding of the accounting equation's function.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-Conclusion 1.7 CONCLUSION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 245,
#             "prompt_tokens": 355,
#             "total_tokens": 600
#         }
#     },
#     {
#         "question": "Who are the primary users of financial statements according to the text?",
#         "options": [
#             "Investors, creditors, government, consumers, owners, etc.",
#             "Accountants and financial analysts only",
#             "Suppliers and distributors",
#             "Marketing and sales teams"
#         ],
#         "correct_answer_index": [
#             0
#         ],
#         "justification_opt": [
#             "The text mentions investors, creditors, government, consumers, owners, etc., as primary users of financial statements."
#         ],
#         "justification_btl": "This question evaluates comprehension regarding the diverse users of financial statements as stated in the text, fitting the 'Understanding' level of Bloom's Taxonomy.",
#         "justification_distractors": [
#             "Incorrect: Accountants and financial analysts are users but not the only primary users mentioned in the text.",
#             "Incorrect: Suppliers and distributors typically analyze different types of reports for their purposes, not financial statements directly.",
#             "Incorrect: Marketing and sales teams are more concerned with operational data rather than financial statements."
#         ],
#         "justification_difficulty": "With requiring knowledge of the stated primary users of financial statements, this question stands at Difficulty Level 10.",
#         "course": "New_MBA_Accounting and Finance",
#         "course_code": "23VMB0C103",
#         "unit_numbers": [
#             1
#         ],
#         "btl": "Understanding",
#         "difficulty": 10,
#         "audience": "postgraduate",
#         "section": "New_MBA_Accounting and Finance_01-Conclusion 1.7 CONCLUSION.txt",
#         "model_used": "gpt-4-turbo",
#         "learning_outcomes": [
#             "Explain conceptual framework of accounting including GAAP."
#         ],
#         "usage": {
#             "completion_tokens": 245,
#             "prompt_tokens": 355,
#             "total_tokens": 600
#         }
#     }
# ]

def run():
    st.set_page_config(
        page_title="MCQ Genie",
        page_icon="👋",
    )

    st.write("# Welcome to MCQ Genie! 👋")
    st.subheader('AI Assisted MCQ :blue[A]nalyzer, :red[G]enerator and :green[E]nhancer :sunglasses:', divider='rainbow')

    # st.write(st.__version__)
    # st.write(os.getcwd())

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
        ('Marketing', 'Data Science', 'Accounting and Finance'),
        index=2)

      with col1:
        no_of_questions = st.selectbox(
          'Number of questions',
          ('1', '2', '3', '4', '5', '6'),
          index=2
        )

      with col2:
        no_of_distractors = st.selectbox(
          'Number of distractors',
          ('1', '2', '3', '4', '5', '6'),
          index=2
        )

      unit_option = st.selectbox(
      'Choose a Unit',
      ('Unit 01 - Introduction to Financial Accounting', 'Unit 02 - Accounting Cycle', 'Unit 03 - Depreciation', 'Unit 04 - Financial Statements'),
      index=3)

      # st.radio(
      #     "Select MCQs to Analyze / Enhance",
      #     key="select_mcq",
      #     options=["All Units", "Select Unit"],
      # )
      
      st.write('Number of MCQs to be generated (BTL and difficulty levels)')

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
      else:
        st.session_state.easy_count = 0
        st.session_state.medium_count = 0
        st.session_state.hard_count = 0
        st.rerun()

      if st.button("Generate", type="primary"):
        with st.spinner("Analyzing and generating questions...This will take a minute."):

            with open("documents/course_details.json", 'r') as f:
              det = json.load(f)
              f.close()
            
            unit_number = unit_option.split(' ')[1][1]

            for l in det["learning_outcomes"]:
              if l["unit"] == int(unit_number):
                lo = "LO - " + l["outcome"][0]

            det['unit_to_generate_mcqs_for'] = int(unit_number)
            det['dir_of_course_unit_segments'] = "documents/New_MBA_Accounting and Finance_0" + unit_number + "-segments"

            with open("documents/course_details.json", 'w') as f1:
              json.dump(det, f1)
              f1.close()

            c = mcq_init()
            ans = mcq_generate(c)

            st.subheader('MCQ Genie Output:', divider='rainbow')
            #st.selectbox("Course", (ans[0]["course_code"] + " " + ans[0]["course"], ""), disabled=True, label_visibility="collapsed")
            st.selectbox("Selected Unit", (unit_option, ""), disabled=True, label_visibility="collapsed")
            st.selectbox("Learning Outcome", (lo, ""), disabled=True, label_visibility="collapsed")

            sections = []
            tabs_texts = []
            n = 0
            for a in ans:
              if a["section"] not in sections:
                n = n + 1
                sections.append(a["section"])
                tabs_texts.append("Section " + str(n))
                             
            tabs = st.tabs(tabs_texts)
            n = 0
            for t in tabs:
              with t:
                question = 0
                for a in ans:
                  if a["section"] == sections[n]:
                    if question == 0:
                      st.header(a["section"].split("1.")[1].split(".txt")[0], divider='rainbow')
                    question = question + 1
                    c1, c2 = st.columns(2)
                    with c1:
                      st.subheader("Question " + str(question))
                    with c2:
                      st.caption("BTL LeveL: Understanding")
                    st.radio(a["question"], a["options"], a["correct_answer_index"][0])
                    exp = st.expander("See justification")
                    exp.markdown(f"""
                      {a["justification_opt"][0]}

                      #### BTL Level
                      {a["justification_btl"]}

                      #### Distractors
                      - {a["justification_distractors"]}

                    """)
                    st.divider()
                n = n + 1

if __name__ == "__main__":
    run()

