\# WEEK 9 – PROJECT PROGRESS REPORT



\## Project Title



\*\*PoisonGuard: Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models\*\*



\*\*Domain:\*\* Cybersecurity and Machine Learning Security  

\*\*Week:\*\* 9  

\*\*Project Status:\*\* Integration Testing and Performance Evaluation



\## 1. Objectives

\- Integrate the machine learning modules with the Flask backend and Streamlit dashboard.

\- Execute data poisoning and backdoor attack experiments.

\- Evaluate poison detection and backdoor detection performance.

\- Test mitigation and model retraining.

\- Verify model integrity using SHA-256 hashing.

\- Perform automated testing and update project documentation.



\## 2. Work Completed



1\. Successfully integrated and started the Flask backend.

2\. Verified the backend health endpoint. The response confirmed Flask, Random Forest and healthy status.

3\. Successfully launched the Streamlit PoisonGuard dashboard.

4\. Trained the baseline Random Forest model.

5\. Executed label-flipping data poisoning experiments at 5%, 10%, 20% and 30% poisoning rates.

6\. Executed a backdoor attack experiment using a feature trigger.

7\. Evaluated suspicious sample detection using Isolation Forest.

8\. Evaluated mitigation by removing selected suspicious samples and retraining the model.

9\. Verified model integrity using the SHA-256 algorithm.

10\. Executed automated tests successfully.



\## 3. Experimental Results



\### A. Model Performance



| Model | Accuracy |

|---|---:|

| Baseline | 95.61% |

| Poisoned | 94.74% |

| Final mitigated | 95.61% |



\### B. Data Poisoning Detection



| Metric | Result |

|---|---:|

| Total training samples | 455 |

| Actual poisoned samples | 45 |

| Suspicious samples | 46 |

| True positives | 2 |

| False positives | 44 |

| False negatives | 43 |

| Detection rate | 4.44% |

| False positive rate | 10.73% |



\*\*Observation:\*\* The current Isolation Forest configuration has a low detection rate. It identifies only a small portion of the actual poisoned samples. Improving detection performance remains an important area of work.



\### C. Backdoor Attack Experiment



| Metric | Result |

|---|---:|

| Backdoor samples | 22 |

| Trigger feature | 0 |

| Suspicious samples | 5 |

| Attack success rate | 4.39% |



\### D. Model Evaluation



| Metric | Baseline | Poisoned | Final |

|---|---:|---:|---:|

| Accuracy | 0.9561 | 0.9474 | 0.9561 |

| Precision | 0.9589 | 0.9714 | 0.9718 |

| Recall | 0.9722 | 0.9444 | 0.9583 |

| F1-score | 0.9655 | 0.9577 | 0.9650 |



\### E. Model Integrity



\- Algorithm: SHA-256

\- Verification status: Verified

\- The dashboard successfully generated and displayed the model hash.



\## 4. Automated Testing



The automated test suite was executed using Pytest.



\*\*Result: 4 out of 4 tests passed.\*\*



\- Backdoor attack test – PASSED

\- Label-flipping poisoning test – PASSED

\- Detection metrics test – PASSED

\- Mitigation sample removal test – PASSED



\## 5. Learning Outcomes



\- Understood the integration of Flask with a machine learning application.

\- Learned to execute and evaluate data poisoning and backdoor attack experiments.

\- Understood detection metrics such as precision, recall, detection rate and false positive rate.

\- Learned how mitigation and model retraining affect model performance.

\- Understood SHA-256-based model integrity verification.

\- Gained experience in testing a machine learning security pipeline using Pytest.



\## 6. Challenges Identified



The Isolation Forest detection method currently has a low detection rate for the generated poisoned samples. Further experimentation and improvements to the detection approach are required. The results also show that restoring model accuracy does not necessarily mean all poisoned samples have been identified.



\## 7. Next Week's Plan



\- Improve data poisoning detection performance.

\- Investigate alternative detection techniques and compare their results.

\- Evaluate detection performance with different poisoning rates.

\- Improve backdoor detection and mitigation.

\- Perform further integration and regression testing.

\- Update the research report, results and GitHub repository.



\## 8. Conclusion



During Week 9, the PoisonGuard Flask backend and Streamlit dashboard were successfully integrated and tested. Data poisoning, backdoor attack, detection, mitigation, model evaluation and integrity verification experiments were executed. The final model accuracy returned to the baseline accuracy of 95.61%, and all four automated tests passed. The experiments also identified low poison detection performance, which will be addressed in the next phase of the project.



\*\*Overall Status: Integration and initial evaluation completed; detection improvement is ongoing.\*\*

