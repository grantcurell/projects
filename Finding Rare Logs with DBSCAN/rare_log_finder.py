import argparse
import string
import webbrowser
from datetime import datetime

import jinja2
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import xmltodict
from jinja2 import Template
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class LogViewer:
    def __init__(self, rare_messages, severities, message_ids, timestamps):
        # Generate the logs
        logs = []
        for message, severity, message_id, timestamp in zip(rare_messages, severities, message_ids, timestamps):
            logs.append((message, severity, message_id, timestamp))

        # Render the logs into the HTML template
        with open("report_template.html") as f:
            template = Template(f.read())
        html = template.render(logs=logs)

        # Save the HTML to a file
        with open("log_viewer_output.html", "w") as f:
            f.write(html)

        # Open the HTML file in the default web browser
        webbrowser.open("log_viewer_output.html")


if __name__ == '__main__':

    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--stemming', action='store_true', help='Use stemming instead of lemmatizing')
    parser.add_argument('--n_features', type=int,
                        help='Number of features to use in FeatureHasher. Defaults to 10x the number of unique features if left unset.')
    parser.add_argument('--epsilon', type=float,
                        help='The value of epsilon to use for DBSCAN. If specified will override the algorithm for finding it automatically.')
    parser.add_argument('--min_samples', type=int,
                        help='The value of min_samples to use for DBSCAN. If specified will override the algorithm for finding it automatically.')
    parser.add_argument('--xml_files', type=lambda s: s.split(','), help='List of XML files to use as input. Comma separated.')
    args = parser.parse_args()


    # Define a function to clean up punctuation and escapes from a string
    def clean_string(s):
        s = s.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        s = s.replace("\\", "")  # Remove escapes
        return s


    # TODO - need to make it so I can easily disable or enable features

    ########################################
    # Read the XML
    ########################################

    # Combine all XML files into one dictionary
    result_dict = {}
    for xml_file in args.xml_files:
        with open(xml_file, 'r') as file:
            xml_dict = xmltodict.parse(file.read())
            for event in xml_dict['LCLogEvents']['Event']:
                result_dict.setdefault('LCLogEvents', {}).setdefault('Event', []).append(event)

    ########################################
    # One Hot Encode Severity and Standardize
    ########################################

    # Create a dataframe with severity levels
    severities = [event.get('@Severity') for event in result_dict['LCLogEvents']['Event']]
    severity_df = pd.DataFrame(severities, columns=['severity'])

    # Instantiate the OneHotEncoder
    encoder = OneHotEncoder(sparse=False)

    # Fit and transform the severity column using the OneHotEncoder
    one_hot = encoder.fit_transform(severity_df[['severity']])

    # Convert the one-hot encoded array to a dataframe with column names
    one_hot_df = pd.DataFrame(one_hot, columns=encoder.get_feature_names_out(['severity']))

    # Join the one-hot encoded dataframe with the original dataframe
    severity_df = pd.concat([severity_df, one_hot_df], axis=1)

    # Standardize the one-hot encoded features
    scaler = StandardScaler()
    severity_df_scaled = scaler.fit_transform(severity_df.iloc[:, 1:])

    # Print the standardized features
    print(severity_df_scaled)

    ########################################
    # One Hot Encode Message ID and Standardize
    ########################################

    # Example message IDs
    message_ids = [event.get('MessageID') for event in result_dict['LCLogEvents']['Event']]
    df = pd.DataFrame({'message_id': message_ids})

    # One-hot encode the message IDs
    encoder = OneHotEncoder()
    message_id_encoded = encoder.fit_transform(df[['message_id']])
    message_id_encoded_df = pd.DataFrame(message_id_encoded.toarray(),
                                         columns=encoder.get_feature_names_out(['message_id']))

    # Standardize the one-hot encoded features
    scaler = StandardScaler()
    message_id_encoded_df_scaled = scaler.fit_transform(message_id_encoded_df)

    # Print the standardized features
    print(message_id_encoded_df_scaled)

    ########################################
    # One Hot Encode the Arg Field and Standardize
    ########################################

    # Example data
    data = [event.get('MessageArgs') for event in result_dict['LCLogEvents']['Event']]
    data = [str(x) for x in data]
    data = [clean_string(s) for s in data]
    unique_features = list(set(data))
    n_features = args.n_features if args.n_features else len(unique_features) * 10

    # Wrap each string in a list to create a list of lists
    data = [[s] for s in data]

    h = FeatureHasher(n_features=n_features, input_type='string')
    X = h.transform(data)

    # Convert the hashed features to a numpy array
    X_array = X.toarray()

    # Reshape the array to have 366 rows and 800 columns
    X_array_reshaped = X_array.reshape(len(data), n_features)

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_array_reshaped)

    # Print the standardized features
    print(X_scaled)

    ########################################
    # Encode the timestamp and standardize
    ########################################

    timestamps = [event['@Timestamp'] for event in result_dict['LCLogEvents']['Event']]

    # Parse the timestamp strings to datetime objects and convert to Unix timestamps
    timestamps_sec = [int(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').timestamp()) for timestamp in timestamps]

    # Standardize the timestamps
    scaler = StandardScaler()
    timestamps_scaled = scaler.fit_transform(np.array(timestamps_sec).reshape(-1, 1))

    # Print the standardized timestamps
    print(timestamps_scaled)

    ########################################
    # Use TF-IDF to encode log messages and Standardize
    ########################################

    # Get the log messages
    messages = [event['Message'] for event in result_dict['LCLogEvents']['Event']]

    # Define the stop words
    stop_words = set(stopwords.words('english'))

    # Tokenize and stem or lemmatize the log messages
    if args.stemming:
        stemmer = PorterStemmer()
        tokenized_messages = [
            [stemmer.stem(word.lower()) for word in word_tokenize(message) if word.lower() not in stop_words] for
            message in messages]
    else:
        lemmatizer = WordNetLemmatizer()
        tokenized_messages = [
            [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(message) if word.lower() not in stop_words]
            for message in messages]

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(min_df=1)

    # Fit the vectorizer to the tokenized messages
    X_tfidf = vectorizer.fit_transform([" ".join(tokens) for tokens in tokenized_messages])

    # Convert the TF-IDF features to a numpy array
    X_tfidf_array = X_tfidf.toarray()

    # Standardize the TF-IDF features
    scaler = StandardScaler()
    X_tfidf_scaled = scaler.fit_transform(X_tfidf_array)

    # Print the standardized features
    print(X_tfidf_scaled)

    ########################################
    # Calculate and plot min_samples and epsilon
    ########################################

    # Combine all the standardized features into a single numpy array
    X = np.concatenate((severity_df_scaled, message_id_encoded_df_scaled, X_scaled, timestamps_scaled, X_tfidf_scaled),
                       axis=1)

    # Compute the distance graph using the NearestNeighbors model
    nn = NearestNeighbors(n_neighbors=10)
    nn.fit(X)
    distances, _ = nn.kneighbors_graph(mode='distance').nonzero()

    # Compute the silhouette score for a range of epsilon values
    epsilon_range = np.linspace(0.1, 10, 100)
    silhouette_scores = []
    for epsilon in epsilon_range:
        dbscan = DBSCAN(eps=epsilon, min_samples=10)
        dbscan.fit(X)
        labels = dbscan.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # number of clusters, ignoring noise
        if n_clusters > 1:
            silhouette_scores.append(silhouette_score(X, labels))
        else:
            silhouette_scores.append(0)

    # Find the epsilon value with the highest silhouette score
    best_index = np.argmax(silhouette_scores)
    best_epsilon = epsilon_range[best_index]

    # Define range of values for min_samples
    min_samples_range = range(2, 11)

    # Calculate silhouette score for each value of min_samples
    silhouette_scores_min = []
    for min_samples in min_samples_range:
        dbscan = DBSCAN(eps=best_epsilon, min_samples=min_samples)
        dbscan.fit(X)
        labels = dbscan.labels_
        if len(set(labels)) > 1:
            score = silhouette_score(X, labels)
        else:
            score = -1
        silhouette_scores_min.append(score)

    # Find the value of min_samples that maximizes the silhouette score
    best_min_samples = min_samples_range[np.argmax(silhouette_scores_min)]

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot 1 - silhouette scores against epsilon
    ax1.plot(epsilon_range, silhouette_scores)
    ax1.set_xlabel('Epsilon')
    ax1.set_ylabel('Silhouette Score')
    ax1.axvline(x=best_epsilon, linestyle='--', color='red', label='Best Epsilon')
    ax1.legend()

    # Plot 2 - silhouette scores against min_samples
    ax2.plot(min_samples_range, silhouette_scores_min)
    ax2.set_xlabel('min_samples')
    ax2.set_ylabel('Silhouette Score')
    ax2.axvline(x=best_min_samples, linestyle='--', color='red', label='Best min_samples')
    ax2.legend()

    plt.show()

    print('Best epsilon:', best_epsilon)
    print("Best min_samples value:", best_min_samples)

    ########################################
    # Apply DBSCAN
    ########################################

    # Print the shapes of the data types
    print('\n'.join([f"{name}: {arr.shape}" for name, arr in
                     zip(['severity', 'message_id', 'args', 'timestamps', 'messages'],
                         [severity_df_scaled, message_id_encoded_df_scaled, X_scaled, timestamps_scaled,
                          X_tfidf_scaled])]))

    # Combine all the standardized features into a single numpy array
    X = np.concatenate((severity_df_scaled, message_id_encoded_df_scaled, X_scaled, timestamps_scaled, X_tfidf_scaled),
                       axis=1)

    # Set default values for epsilon and min_samples
    epsilon = args.epsilon if args.epsilon else best_epsilon
    min_samples = args.min_samples if args.min_samples else best_min_samples

    # Create DBSCAN object with the correct arguments
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)

    # Fit the model
    dbscan.fit(X)

    # Get the labels assigned by the model
    labels = dbscan.labels_

    # Print the number of clusters found by the model
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print("Number of clusters found: ", n_clusters)

    # Find the rare logs and print their messages
    rare_logs = X[labels == -1]
    rare_messages = [messages[i] for i, label in enumerate(labels) if label == -1]
    print("Messages of rare logs: ")
    print('\n'.join(rare_messages))

    # Create the HTML report using Jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('report_template.html')
    html_report = template.render(messages=rare_messages, severities=severities, message_ids=message_ids,
                                  timestamps=timestamps)

    # Write the HTML report to a file
    # Create a LogViewer object and pass the rare_messages, severities, message_ids, and timestamps as arguments
    log_viewer = LogViewer(rare_messages, severities, message_ids, timestamps)