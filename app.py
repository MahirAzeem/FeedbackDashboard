import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import numpy as np
import matplotlib.pyplot as plt


st.title('Feedback Channel of SPAVIS')

credpath = {
    "type": "service_account",
    "project_id": "radar-application-1488d",
    "private_key_id": "f6cb1dc14b3dc38046b0fb210b2dfd3d13a28492",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCXpLPG47dSuefI\nQilyR4oBYz5AxBbFhc4itQa4ybmcFF93+bs97ZUW/LM1YNCdb76Mlkgdtyfb3P4u\nbk9gZ6RAqQLnO90tw+bHtxX6Q29Rh1LuecgSqqZZrqdrSBcriBaVHzdBT1t914S4\nTcb2gpmUj+596z9S/SH3NC20KvNFo/Ai3/UmgwdcNIasKpBQrQASJfP7wU1gHf7T\nvnyZnexFUX2BmsmUEkq7RZfcii+98kQQ/zv+CgxU1SkSXFY3WCLag0XAlsGIxVyd\ncLOSs9PnEzi08m5LYIPsnfzqa6KnYv34qnXoOGRTSk5ZdPRrzLxvNBJNRuSN0wOk\n9M39Dky/AgMBAAECggEAPSTK3EILNA8DlyqePZb83Uxf2It4RxKJqFLnr/Cep4FL\ncTu/tNusBsXDmJ094I0i/trFnz2vk6ZK0vvlg5CmmO/M3OG1b/OShSqccPlp1CzF\nUqTF+EjYpEaY+Nfrh8DqohwhEnNmB5qzyACMXe8Q7+cNGbaWJOcuH9fpKcE7r/Mn\nyQtzhRdKu+sUSr2+w1jJ66naKQvlfRkQZyAs1NE1lDTlGNmHKe9cMXV0iVuZyKRq\nbAiIxjyCB/NMObwq2trPJ0mhRQdc9d0PJFHMaOKBEhhS3YdDbgIMyj7rUMo4alI8\nNiawsskLq9D6DQNrzFdp33ewB21eNTshkhpXxwuQGQKBgQDVMI4jqliPFYpKmooO\n+Zx3ggLksslDmDxaIs2gjReuvvLXZYBbG7SKpMtUsWZPYs5C5p8nW7GRRfCArmVo\nUwXd0PZwt4sPg0HyoflAlliB/kecr1bVzWfH2ogTySguLW+tWV/zYRAMN2FoEPZR\ntkFwWHJyJduA5JvxAo+nMH4FvQKBgQC2GDw/b64edVyplNkJz6mgiTPjnQn+g5FC\nQua5/xPLaIbXMMzNlxTFXBZ6ZoPreao6dG3jOAxj4Wpd9XY2JKvD9MgWRrjEmbyG\nA93Snfgn9w/Iaa51TanjPExSUqWNNrh011X9ynYQn8YVOHxhUZ9FeSjYIQMTHGFf\nIvjuK48OKwKBgQCMz6hiqEYcI/cWtaJQp9AQI4BzvB8xlWDvjCNTUz38PsU5PiKc\nit0h4h0nEJFqB/ICwD8JCQhs0sw6wnXahVPPohDUfHbORT0O3Ks8XNGS8vgr5qgt\nSaGtoIrWvrvaXEpyLiExKMAnwYCF8wYvDHmGkfTtrlGgfd7+PlnR7Taf5QKBgBhZ\nzVS+Xo58K1QSL6P8PTbWojXB/mAmv/oYcDpXPhJpe/6y6/BiT8jEs8zSgLmwn28J\nutgz2pRQxKSj+pbq+H1P8qHn+zVvSaKySausrE7L3zRxzX6qUBmvKpWnr7PeqXQW\nh81Ukc1PUHHuB9QL0jy8IxYj9AFOPkc2qgtPj+XZAoGBAKqTRxgt8XKx7ewgq/c2\n/h38i3H/NCiLy3ETkMiOWJYYUApYfqdgeLyvXqVRR008xYTIGDqF63lmkut2leH1\nBneR3uOIBfxp/jIescqqayiQN1198e4anmxwOOJyEm8WNZ4B7aLJRsqVFoq9UPxC\nzDNN6bA/pCG7i+AwQ9479KAm\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-gh7k5@radar-application-1488d.iam.gserviceaccount.com",
    "client_id": "108252273274804916220",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gh7k5%40radar-application-1488d.iam.gserviceaccount.com"
}

if not firebase_admin._apps:
    login = credentials.Certificate(credpath)
    default_app = firebase_admin.initialize_app(login)

db = firestore.client()
feedbacks = db.collection("feedbacks").stream()
topics = db.collection("topics").stream()

# Printing all the sentences
sentences = []
for feedback in feedbacks:
    feedbackOnly = feedback.to_dict()
    sentences.append(feedbackOnly)
st.header('Feedback List')
st.dataframe(sentences)


every_topics = []
for topic in topics:
    topicOnly = topic.to_dict()
    every_topics.append(topicOnly)
st.header('Topic List')
st.dataframe(every_topics)


# Number of Positive Feedbacks
pos_feedback = []
aspect = db.collection("feedbacks").where(
    u"sentiment", u"==", u"Positive").stream()
for doc in aspect:
    aspects = doc.to_dict()
    pos_feedback.append(aspects)

pos_aspect_count = len(pos_feedback)

# Number of Negative Feedbacks
neg_feedback = []
aspect = db.collection("feedbacks").where(
    u"sentiment", u"==", u"Negative").stream()
for doc in aspect:
    aspects = doc.to_dict()
    neg_feedback.append(aspects)

neg_aspect_count = len(neg_feedback)

# Sum of feedbacks given upon the volunteer related aspect
# volunteer_aspect_feedback = []
# volunteer_aspect_count = db.collection("feedbacks").where(
#     u'aspect', u'array_contains_any', [u'volunteer', u'volunteer service', u'physical volunteer']).stream()
# for doc in volunteer_aspect_count:
#     aspects_to_doc = doc.to_dict()
#     volunteer_aspect_feedback.append(aspects_to_doc)
# volunteer_feedback_count = len(volunteer_aspect_feedback)
# st.markdown(volunteer_feedback_count)
# st.markdown(volunteer_aspect_feedback)


st.header('Total Positive and Negative Feedback')

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Positive', 'Negative'
sizes = [pos_aspect_count, neg_aspect_count]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, radius=800)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)


# query = db.collection("feedbacks").where(
#     u'aspect', u'==', u'volunteer').stream()
# for doc in query:
#     count = doc.size
# st.markdown(count)
