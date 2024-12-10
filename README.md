# IT Services Chatbot

Welcome to the **IT Services Chatbot**! This chatbot is designed specifically for university IT service teams and is written in Python. It provides a user-friendly interface and combines rule-based pattern matching with the Logistic Regression ML algorithm to assist with IT queries.

---

## How It Works

The chatbot uses the following process to handle user queries:

1. **Text Processing and Classification**:
   - User input text is converted into a vector using a `CountVectorizer` instance from `scikit-learn`.
   - A Logistic Regression model then classifies the input into one of eight categories:
     - `email_issue`
     - `goodbye`
     - `greetings`
     - `matlab`
     - `password_requirement`
     - `password_reset`
     - `wifi`
     - `need_clarification`

2. **Dialogue Trees**:
   - Each category corresponds to a predefined dialogue tree stored in `dialoguetree.json`.
   - Dialogue trees are traversed in **reverse-level order** until a keyword phrase from the user's input matches a node.
   - Once a match is found, the chatbot begins iterating through the subnodes of the matched node, providing detailed instructions.
   - If no match is found, the chatbot starts iterating through the subnodes of the **root** of the tree.

3. **User Interaction**:
   - **Positive Response ("Yes")**: 
     - If the user answers "yes," the chatbot continues to the **next subnode on the same level**, offering sequential instructions.
   - **Negative Response ("No")**: 
     - If the user answers "no," the chatbot moves **down to the children of the current subnode** for more specific guidance.
     - If the current node has no subnodes, then the chatbot tells the user that it cannot give any further guidance and asks the user to contact IT services by phone.
     - After finishing the deeper level, the chatbot **returns to the previous level** to ensure the user receives complete instructions.
---

## Installation

### Required Python Libraries
Ensure the following Python libraries are installed on your system:
- `pickle` (pre-installed; `pip` command may display an error if reinstalled)
- `streamlit`
- `json` (pre-installed; `pip` command may display an error if reinstalled)
- `pandas`
- `numpy`
- `scikit-learn`

To install a library, run the following command in your terminal:
```bash
pip install <library_name>
```

Alternatively install all required libraries in requirements.txt by running the following command:
```bash
pip install -r requirements.txt
```

---

### Additional Setup for Windows
1. After installing `streamlit`, you might see a yellow warning message displaying a path to add to your system's environment variables.
2. Copy the path, which should look similar to:
   ```
   C:\Users\username\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\Scripts
   ```
3. Add this path to your system environment variables:
   - Open **Edit the System Environment Variables** on your PC.
   - Click on the **Environment Variables** button to open a pop-up window.
   - In the **System Variables** section, select the `Path` variable and click the **Edit** button.
   - In the new pop-up window, click **New** and paste the copied path into the blank field.
4. Close all windows and re-open the terminal.

### Additional Setup for MacOS
Refer to the [Streamlit installation guide](https://docs.streamlit.io/library/get-started/installation) for detailed instructions.

---

## Directory Requirements
Ensure the following files are in the same directory before starting the chatbot:
- `luc.py`
- `dmu.py`
- `finalchatbot.py`
- `dialoguetree.json`
- `vectorizer.p`
- `model.p`
- `luc.p`
- `dmu.p`

### Important Notes
- **Training Data**:
  - The `vectorizer.p` and `model.p` files are generated by running `training.py`.
  - Files with the .p extension are pickle files, which serialize Python objects, where vectorizer.p is a serialized CountVectorizer instance and model.p is a serialized LogisticRegression instance trained on a dataset of 359 chat text segments classified into 8 categoires.
  - Running `training.py` again will regenerate these files using new training data.
  - The training dataset is not included in this repository due to data protection concerns.
- **Other Files**:
  - The `luc.p` file is generated by running `luc.py`.
  - The `dmu.p` file is generated by running `dmu.py`.

---

## Running the Chatbot
To launch the chatbot:
1. Open your terminal and navigate to the directory containing the required files.
2. Run the following command:
   ```bash
   streamlit run finalchatbot.py
   ```

### Stopping the Chatbot
To terminate the application, press `Ctrl + C` in your terminal.





