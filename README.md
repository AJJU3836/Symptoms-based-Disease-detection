# Symptom-Based Doctor Suggestion System 🩺

A smart, rule-based web application designed to help patients find the right specialist based on their specific medical symptoms and age group. 

## 🚀 Features

*   **Patient Registration & Login:** Secure portal for patients to create accounts and log in.
*   **Symptom Mapping:** Admin can map various symptoms to specific medical specialities (e.g., Chest Pain ➡️ Cardiology).
*   **Smart Recommendation:** Patients select their symptoms, and the system filters and recommends doctors who specialize in those symptoms.
*   **Age-Based Filtering:** The system automatically categorizes patients into "Children" or "Adults" based on their Date of Birth and filters doctors accordingly.
*   **Quick Access:** Patients can save recommended doctors for future quick access.
*   **Admin Dashboard:** Admins can manage Patients, Doctors, Specialities, and Symptoms.

## 🛠️ Tech Stack

*   **Backend:** Python 3, Django (Web Framework)
*   **Database:** SQLite (Default Django DB)
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, Bootstrap
*   **Additional Libraries:** jQuery, Owl Carousel, Font Awesome

## 💻 Installation & Setup

Follow these steps to run the project locally on your machine.

**1. Clone the repository**
```bash
git clone https://github.com/AJJU3836/symptom-based-doctor-suggestion.git
cd symptom-based-doctor-suggestion
```

**2. Create a Virtual Environment**
```bash
python -m venv venv
```

**3. Activate the Virtual Environment**
*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **Mac/Linux:**
    ```bash
    source venv/bin/activate
    ```

**4. Install Dependencies**
Because this project utilizes specific older versions of Django and Viewflow, make sure to install them exactly as follows:
```bash
pip install setuptools
pip install django-viewflow
pip install Django==2.2.4
```
*(Note: Installing `django-viewflow` might upgrade Django to a newer version automatically, which is why we explicitly downgrade it back to `2.2.4` afterward to maintain compatibility).*

**5. Run the Server**
```bash
python manage.py runserver
```

**6. Access the Application**
Open your browser and navigate to:
`http://127.0.0.1:8000/`

## 🔐 Default Admin Credentials

To access the admin panel, navigate to `http://127.0.0.1:8000/login`, select the **Admin** role, and use the following hardcoded credentials:

*   **Mobile:** `8767541300`
*   **Password:** `ajay123`
