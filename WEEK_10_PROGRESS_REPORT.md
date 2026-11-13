\# WEEK 10 – PROJECT PROGRESS REPORT



\## Project Title



\*\*PoisonGuard: Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models\*\*



\*\*Domain:\*\* Cybersecurity and Machine Learning Security  

\*\*Week:\*\* 10  

\*\*Project Status:\*\* Robust Training Development and Integration



\## 1. Objectives



\- Develop a Robust Training Engine.

\- Implement ensemble learning techniques.

\- Compare baseline and robust models under different poisoning rates.

\- Save and load the trained robust model.

\- Integrate the robust model with the Flask backend.

\- Connect the robust training functionality to the Streamlit dashboard.



\## 2. Work Completed



1\. Developed a robust training module using Random Forest, Extra Trees and Gradient Boosting.

2\. Combined the three classifiers using a Soft Voting Classifier.

3\. Conducted experiments at 5%, 10% and 20% data poisoning rates.

4\. Compared the performance of the baseline Random Forest and robust ensemble.

5\. Saved the trained ensemble model as `robust\_ensemble\_model.pkl`.

6\. Implemented model loading and prediction verification.

7\. Developed the Flask API endpoint `/api/robust-training`.

8\. Successfully tested the robust training API.

9\. Integrated a robust training button into the Streamlit dashboard.

10\. Generated the experiment comparison CSV.



\## 3. Experimental Results



| Poisoning Rate | Baseline Accuracy | Robust Accuracy |

|---|---:|---:|

| 5% | 95.61% | 95.61% |

| 10% | 94.74% | 96.49% |

| 20% | 88.60% | 91.23% |



\### Robust Model Evaluation



\- Accuracy: 96.49%

\- Precision: 95.95%

\- Recall: 98.61%

\- F1 Score: 97.26%



The ensemble achieved higher accuracy than the baseline model at 10% and 20% poisoning rates in the conducted experiments.



\## 4. Technologies and Tools Used



\- Python

\- Scikit-learn

\- Random Forest

\- Extra Trees Classifier

\- Gradient Boosting

\- Voting Classifier

\- Flask

\- Streamlit

\- Pandas

\- Joblib

\- PowerShell

\- Git and GitHub



\## 5. Challenges Encountered



\- Integrating the robust training module with the existing backend.

\- Resolving Python module import and syntax issues.

\- Loading the saved ensemble model through Flask.

\- Connecting the backend API with the Streamlit dashboard.

\- Correcting the dashboard results display.



\## 6. Key Learning Outcomes



\- Learned ensemble learning and soft voting.

\- Understood model evaluation under different data poisoning rates.

\- Learned how to save and load trained machine learning models.

\- Gained experience developing Flask API endpoints.

\- Learned to connect machine learning functionality to a Streamlit dashboard.

\- Improved understanding of accuracy, precision, recall and F1-score.



\## 7. Plan for Next Week



\- Explore additional robust training techniques.

\- Investigate adversarial training and differential privacy.

\- Improve data poisoning and backdoor detection.

\- Perform complete system testing.

\- Improve dashboard visualizations.

\- Update project documentation and research report.



\## 8. Conclusion



During Week 10, the Robust Training Engine was developed using an ensemble of Random Forest, Extra Trees and Gradient Boosting classifiers. Experiments were conducted at different poisoning rates, and the ensemble achieved 96.49% accuracy in the 10% poisoning experiment.



The trained model was saved, tested and integrated into the Flask backend. A corresponding feature was added to the Streamlit dashboard.





