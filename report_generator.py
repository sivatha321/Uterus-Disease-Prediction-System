from groq import Groq

client = Groq(
    api_key=""
)

def generate_medical_report(patient):

    symptoms = ", ".join(
        [s.name for s in patient.symptoms.all()]
    )

    prompt = f"""
You are an experienced gynecologist.

Patient Age: {patient.age}

BMI Category:
{patient.bmi_category}

Final Diagnosis:
{patient.rf_disease}

Symptoms:
{symptoms}

Generate a professional medical report with the following sections:

CLINICAL FINDINGS

* Mention the diagnosed uterine condition.
* Mention relevant observations related to the patient's BMI category.
* Mention relevant observations related to the patient's symptoms.
* Explain whether the BMI status may influence overall health or disease management.

CLINICAL INTERPRETATION

* Explain the diagnosis in simple clinical language.

RECOMMENDATIONS

* Suggest appropriate lifestyle modifications, diet, follow-up consultations, and further evaluation if needed.

DISCLAIMER

* State that this report is AI-assisted and should not replace professional medical advice.

Do NOT include:

* Patient Name
* Age
* BMI heading
* Patient Information
* Final Diagnosis heading
* Symptoms heading

Return plain text only.
"""


    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return completion.choices[0].message.content