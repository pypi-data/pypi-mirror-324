# streamlit-analytics-cards

A project to create custom Streamlit components using React and TypeScript for analytics and insights.

View a demo: [💾](https://analytics-cards.streamlit.app/)
View it on PyPI: [👾](https://pypi.org/project/streamlit-analytics-cards/0.1.0/)

## Using the component

## **Prerequisites**

- [Python 3.7+](https://www.python.org/downloads/)
- [Streamlit](https://docs.streamlit.io/)

## **Installation**

```bash
pip install streamlit-analytics-cards
```

## **Implementation**

```python
from streamlit_analytics_cards import card as stac
# Render the component in your Streamlit app
stac(
            template="CardOne",
            title="Attrition Diversity",
            subtitle="Female Attrition",
            main_value="4.7%",
            secondary_value="52",
            delta="Y/Y 5.1%, -0.4%",
            chart_data=df["Number of Exits"].tolist(),
            x_axis_label=df.columns[0],
            color_scheme={"background": "#FFFFFF", "text": "#000000"},
            key="card_1",
        )
```

---

## For developers

## **Prerequisites**

Before you start, ensure you have the following installed on your system:

- [Python 3.7+](https://www.python.org/downloads/)
- [Node.js 14+ and npm](https://nodejs.org/)
- [Streamlit](https://docs.streamlit.io/)

---

## **Installation**

1. **Clone the repository**:

   ```bash
   git clone https://github.com/natxc/streamlit-analytics-cards.git
   cd streamlit-analytics-cards
   ```

2. **Set up the Python environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**:
   Navigate to the `frontend/` folder and install the required Node.js packages:
   ```bash
   cd frontend
   npm install
   ```

---

## **Development**

### **Run the Frontend**

Start the development server for the React app:

```bash
npm start
```

This will start a local development server at [http://localhost:3000](http://localhost:3000).

---

### **Run the Streamlit**

In the root directory, start the Streamlit app:

```bash
streamlit run streamlit_app/app.py
```

---

## **Production Build**

1. **Build the Frontend**:
   Navigate to the `frontend/` folder and run:

   ```bash
   npm run build
   ```

   This will create a production-ready build in the `frontend/build` directory.

2. **Run Streamlit in Production Mode**:
   Ensure `_RELEASE` is set to `True` in the `__init__.py` file:

   ```python
   _RELEASE = True
   ```

   Then start the Streamlit app:

   ```bash
   streamlit run streamlit_app/app.py
   ```
