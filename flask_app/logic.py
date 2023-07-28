import nltk
import numpy as np
import pandas as pd
import unidecode
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from flask_app_config import database


def create_jobs(skills_list):
    cols = ["File", "Category"]
    cols = cols.extend(skills_list)
    jobs = pd.DataFrame(columns=cols)
    jds = database["jobs"].find()

    count = 1
    for jd in jds:
        try:
            word_tokens = nltk.tokenize.word_tokenize(jd["description"])
            filtered_tokens = [
                w for w in word_tokens if w.isalpha()
            ]  # remove the punctuation
            ngrams = list(
                map(" ".join, nltk.everygrams(word_tokens, 2, 7))
            )  # generate ngrams (such as artificial intelligence)
            row = dict()
            row["File Name"] = jd["description"]
            row["Category"] = jd["title"]
            for token in filtered_tokens:
                if token in skills_list:
                    row[token] = row.get(token, 0) + 1
            for ngram in ngrams:
                if ngram in skills_list:
                    row[ngram] = row.get(ngram, 0) + 1
            jobs = jobs.append(row, ignore_index=True)
            print("appended {} with path {}".format(count, jd["title"]))
        except:
            print(
                "couldn't append {} execption occured; file path{}".format(
                    count, jd["title"]
                )
            )
        count += 1
    jobs.fillna(0, inplace=True)
    return jobs


def create_and_save_df(jobs):
    cols = jobs.columns.to_list()
    df = pd.DataFrame(columns=cols)
    filelist = database["candidate"].find()

    count = 1
    for i in filelist:
        try:
            input_text = i["file"]
            soup = BeautifulSoup(input_text, "html.parser")
            stripped_text = soup.get_text(separator=" ")
            input_text = unidecode.unidecode(stripped_text)
            input_text = input_text.replace("\n", " ")
            input_text = input_text.replace("/", " ").lower()
            stop_words = set(nltk.corpus.stopwords.words("english"))
            word_tokens = nltk.tokenize.word_tokenize(input_text)
            filtered_tokens = [
                w.lower() for w in word_tokens if w not in stop_words
            ]  # remove the stop words
            filtered_tokens = [
                w.lower() for w in word_tokens if w.isalpha()
            ]  # remove the punctuation
            ngrams = list(
                map(" ".join, nltk.everygrams(word_tokens, 2, 7))
            )  # generate ngrams (such as artificial intelligence)
            row = dict()
            row["File Name"] = i["_id"]
            row["Category"] = i["title"]
            for token in filtered_tokens:
                if token in cols:
                    row[token] = row.get(token, 0) + 1
            for ngram in ngrams:
                if ngram in cols:
                    row[ngram] = row.get(ngram, 0) + 1
            df = df.append(row, ignore_index=True)
            print("appended {} with path {}".format(count, i["_id"]))
        except:
            print(
                "couldn't append {} execption occured; file path{}".format(
                    count, i["_id"]
                )
            )
        count += 1

    df.fillna(0, inplace=True)
    df = df[jobs.columns]
    return df


def calculate_tf_idf_cf(df, jobs):
    candidate_data = df.loc[
        :, df.columns.difference(["File Name", "Category"])
    ].to_numpy()
    cat_list = df["Category"].to_list()
    unique_cat, unique_cat_doc_count = np.unique(
        df["Category"], return_counts=True
    )  # unique categories and their no of doc
    freq_skills_per_cat = (
        df.groupby(by=["Category"]).sum().to_numpy()
    )  # frequency of skills per category
    vector = candidate_data.sum(
        axis=1
    )  # total skills in per doc with shape = (no. of cv,)
    vector2 = candidate_data.sum(
        axis=0
    )  # total of doc per skill with shape = (no. of skills,)
    tf = np.divide(candidate_data.T, 1 + vector).T  # shape = (no.of cv, no. of skills)
    idf = np.log(
        np.divide(candidate_data.shape[0], (candidate_data != 0).sum(axis=0) + 1)
    )  # shape = (no. of skills,)
    cf = {
        unique_cat[idx]: np.divide(freq_skills_per_cat[idx], unique_cat_doc_count[idx])
        for idx in range(unique_cat.shape[0])
    }  # list of cf
    jobs_category_file = jobs[["Category", "File Name"]].to_numpy()
    jobs_tfidfcf = np.empty((0, tf.shape[1]), int)
    jobs.set_index("Category", inplace=True)

    for jcf in jobs_category_file:
        jobs_tfidfcf = np.append(
            jobs_tfidfcf,
            np.multiply(
                np.multiply(
                    jobs.loc[jcf[0], jobs.columns.difference(["File Name", "Category"])]
                    .to_numpy()
                    .reshape(-1),
                    idf,
                ),
                cf[jcf[0]],
            ).reshape(1, -1),
            axis=0,
        )
    jobs.reset_index(inplace=True)
    for index in range(df.shape[0]):
        class_freq_of_skills = cf[df["Category"][index]]
        tfidfcf = np.multiply(
            np.multiply(tf[index], idf), class_freq_of_skills
        ).reshape(1, -1)
        index_of_job_tfidfcf = jobs.index[
            (jobs["Category"] == df["Category"][index])
        ].to_list()[0]
        cs = cosine_similarity(
            jobs_tfidfcf[index_of_job_tfidfcf].reshape(1, -1), tfidfcf
        ).flatten()
        cs = np.round(cs * 100, 2)
        df.loc[index, "Score"] = cs
    for _, abcd in df.iterrows():
        database["candidate"].update_one(
            {"_id": abcd[1]}, {"$set": {"file_score": abcd[df.shape[1] - 1]}}
        )


def calculate_scores_util(job_title):
    print("Starting")
    database["jobs"].update_one(
        {"title": job_title},
        {"$set": {"isShortlisted": True, "current_status": "In Progress"}},
    )
    database["candidate"].update_many({}, {"$set": {"isShortlisted": False}})
    skills = database["skills"].find({}, {"skill_name": 1, "_id": 0})
    skill_list = []
    for skill in skills:
        skill_list.append(skill["skill_name"])
    print("List of skills created")
    jobs = create_jobs(skill_list)
    print("Collected key skills required for job")
    df = create_and_save_df(jobs)
    print("Collected key skills of each candidate")
    calculate_tf_idf_cf(df, jobs)
    database["jobs"].update_one(
        {"title": job_title},
        {"$set": {"current_status": "Successful"}},
    )
    print("Shortlisting Successful")
