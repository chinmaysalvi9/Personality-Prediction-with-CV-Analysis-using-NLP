import json
import threading
from flask import Flask, request
from flask_app_config import database
from logic import calculate_scores_util


app = Flask(__name__)


@app.route("/get_admins", methods=["GET"])
def get_admins():
    return list(database["admin"].distinct("_id"))


@app.route("/get_jobs", methods=["GET"])
def get_jobs():
    request_data = request.get_json()
    document_filter = dict()

    if "document_filter" in request_data:
        document_filter = request_data["document_filter"]

    response_data = []

    for job in database["jobs"].find(document_filter):
        response_data.append({
            'title': job['title'],
            'location': job['location'],
            'description': job['description'],
            'type': job['type'],
            'isShortlisted': job['isShortlisted'],
            'lastdate': job['lastdate']
        })

    return response_data


@app.route("/candidate_data", methods=["GET"])
def candidate_data():
    return json.dumps(database["candidate"].find_one({"_id": request.get_json()["user_id"]}))


@app.route("/give_test", methods=["GET"])
def candidate_test_status():
    user_id = request.get_json()["user_id"]

    if database["candidate"].find_one({"_id": user_id})["gaveTest"]:
        return {"start_test": False}

    database["candidate"].update_one({"_id": user_id}, {"$set": {"gaveTest": True}})
    return {"start_test": True}


@app.route("/candidate_apply_job", methods=["GET"])
def candidate_apply_job():
    data = request.get_json()
    candidate_data = database["candidate"].find_one({"_id": data["user_id"]})

    if candidate_data["alreadyApplied"]:
        return {"alreadyApplied": True, "title": candidate_data.get("title", "")}

    database["candidate"].update_one(
        {"_id": data["user_id"]},
        {
            "$set": {
                "alreadyApplied": True,
                "title": data["title"],
            }
        },
    )
    return {"alreadyApplied": False, "title": data["title"]}


@app.route("/calculate_scores", methods=["GET", "POST"])
def calculate_scores():
    try:
        data = request.get_json()
        threading.Thread(target=calculate_scores_util, args=(data["title"],)).start()
        return {"status": True, "error_msg": ""}
    except Exception as e:
        return {"status": False, "error_msg": e}


@app.route("/check_shortlisting_status", methods=["GET"])
def check_shortlisting_status():
    try:
        data = request.get_json()
        return {"status": database["jobs"].find_one({"title": data["title"]}).get("current_status", ""),
                "error_msg": ""}
    except Exception as e:
        return {"status": "Error", "error_msg": e}


@app.route("/shortlist", methods=["GET"])
def shortlist():
    try:
        data = request.get_json()

        for candidate_id in data["ids"]:
            database["candidate"].update_one(
                {"_id": candidate_id}, {"$set": {"isShortlisted": True}}
            )
        return "True"
    except Exception as e:
        return f"False: {e}"


@app.route("/candidates", methods=["GET"])
def get_candidates():
    data = request.get_json()
    response_data = []

    for candidate in database["candidate"].find({"title": data['job']}):
        response_data.append({
            '_id': candidate['_id'],
            'title': candidate['title'],
            'file_score': candidate['file_score'],
            'alreadyApplied': candidate['alreadyApplied'],
            'gaveTest': candidate['gaveTest'],
            'aptitude_score': candidate['aptitude_score'],
            'personality_score': candidate['personality_score'],
            'isShortlisted': candidate['isShortlisted']
        })
    return response_data


@app.route("/add_aptitude_question", methods=["GET"])
def add_aptitude_question():
    try:
        data = request.get_json()
        database["aptitude"].insert_one(dict(zip(
            ["question", "correct_option", "option_1", "option_2", "option_3", "option_4"],
            data["question_data"]
        )))
        return "True"
    except:
        return "False"


@app.route("/add_personality_question", methods=["GET"])
def add_personality_question():
    try:
        data = request.get_json()
        database["personality"].insert_one(
            {
                "question": data["question"],
                "type": data["type"],
                "ispositive": data["ispositive"],
            }
        )
        return "True"
    except:
        return "False"


@app.route("/add_new_job", methods=["GET"])
def add_new_job():
    try:
        data = request.get_json()
        database["jobs"].insert_one(
            {
                "title": data["title"],
                "location": data["location"],
                "isShortlisted": data["isShortlisted"],
                "lastdate": data["lastdate"],
                "description": data["description"],
                "type": data["type"],
                "file": data["file"],
            }
        )
        return "True"
    except:
        return "False"


@app.route("/verify_user", methods=["GET"])
def admin_verification():
    try:
        data = request.get_json()

        if data["is_candidate"]:
            user = database["candidate"].find_one({"_id": data["email_id"]})
        else:
            user = database["admin"].find_one({"_id": data["email_id"]})

        if user:
            return str(user["password"] == data["pass"])
        else:
            return "None"
    except:
        return "Error"


@app.route("/add_admin", methods=["GET"])
def add_admin():
    try:
        data = request.get_json()
        database["admin"].insert_one(
            {
                "_id": data["credentials"][0],
                "password": data["credentials"][1],
            }
        )
        return "True"
    except:
        return "False"


@app.route("/get_personality_questions", methods=["GET"])
def get_personality_questions():
    return [
        {"type": question["type"], "ispositive": question["ispositive"], "question": question["question"]}
        for question in database["personality"].find()
    ]


@app.route("/get_aptitude_questions", methods=["GET"])
def get_aptitude_questions():
    return [{
        "question": question["question"],
        'correct_option': question['correct_option'],
        'option_1': question['option_1'],
        'option_2': question['option_2'],
        'option_3': question['option_3'],
        'option_4': question['option_4']
    } for question in database["aptitude"].find()]


@app.route("/candidate_count", methods=["GET"])
def candidate_count():
    try:
        return {"count": database["candidate"].count_documents(
            {"title": request.get_json()["title"]}
        )}
    except Exception as e:
        return {"count": 0, "error": str(e)}


@app.route("/register", methods=["GET"])
def candidate_register():
    try:
        database["candidate"].insert_one(request.get_json())
        return "True"
    except:
        return "Error"


@app.route("/report_score", methods=["GET"])
def report_candidate_test_score():
    try:
        request_data = request.get_json()

        if request_data["type"] == "aptitude":
            score_data = {
                "$set": {
                    "aptitude_score": {
                        "score": request_data["score"],
                        "noofquest": request_data["cursor_len"]
                    }
                }
            }
        elif request_data["type"] == "personality":
            score_data = {
                "$set": {
                    "personality_score": {
                        "extraversion": request_data["extraversion"],
                        "neuroticism": request_data["neuroticism"],
                        "conscientiousness": request_data["conscientiousness"],
                        "agreeableness": request_data["agreeableness"],
                        "openness": request_data["openness"],
                    }
                }
            }

        else:
            raise Exception

        database["candidate"].update_one(
            {"_id": request_data["user_id"]},
            score_data
        )

        return "True"
    except:
        return "Error"


if __name__ == "__main__":
    app.run(port=6174)
