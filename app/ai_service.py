import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .models import Students,env_token



# genai.configure(api_key="hesdh33")
genai.configure(api_key=env_token.objects.first().gemini_token)

model = genai.GenerativeModel("gemini-3.1-flash-lite")


def get_all_students_data():
    """Database থেকে সব student data নিয়ে আসে dict আকারে"""
    students = Students.objects.all().values(
        'id', 'name', 'father_name', 'mother_name', 'date_of_birth',
        'gender', 'blood_group', 'semester', 'roll', 'reg', 'session',
        'shift', 'section', 'mobile_number', 'email',
        'present_address', 'permanent_address',
        'emergency_contact_name', 'emergency_contact_number',
        'nationality', 'religion'
    )
    # date কে string এ convert করি JSON এর জন্য
    result = []
    for s in students:
        s['date_of_birth'] = str(s['date_of_birth']) if s['date_of_birth'] else None
        result.append(s)
    return result


def ask_ai(user_question: str) -> dict:
    """User প্রশ্ন → সব data Gemini কে পাঠায় → answer"""
    try:
        # সব student data নাও
        all_data = get_all_students_data()

        if not all_data:
            return {"success": False, "answer": "Database এ কোনো student নেই।"}

        # Gemini কে prompt বানাও
        prompt = f"""You are a helpful AI assistant for a Student Management System.
You are given the COMPLETE list of students in JSON format. Answer the user's question accurately based on this data.

STUDENT DATA ({len(all_data)} students):
{json.dumps(all_data, ensure_ascii=False, indent=2)}

USER QUESTION: {user_question}

INSTRUCTIONS:
- Answer in the SAME language as the user's question (Bengali → Bengali, English → English).
- Be friendly, concise and accurate.
- If multiple students match, use a neat bullet list or table.
- Translate codes for user: M→Male/পুরুষ, F→Female/মহিলা, O→Other/অন্য
- When showing a student's info, show relevant fields only (name, roll, semester, etc.) — not all 20 fields.
- NEVER show raw JSON to the user. Format it nicely.
- If no student matches, politely say "কোনো student পাওয়া যায়নি".
- If the question is not about students, politely say you can only answer about students.

Answer:"""

        response = model.generate_content(prompt)
        return {
            "success": True,
            "answer": response.text.strip(),
            "total_students": len(all_data),
        }

    except Exception as e:
        return {"success": False, "answer": f"Error: {str(e)}"}