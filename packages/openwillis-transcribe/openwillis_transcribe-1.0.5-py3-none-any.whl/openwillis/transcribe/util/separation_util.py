# author:    Vijay Yadav
# website:   http://www.bklynhlth.com

# import the required packages
import os
import tempfile
import pandas as pd
import numpy as np
import logging
import shutil

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pydub import AudioSegment
from ..commons import to_audio, from_audio, volume_normalization

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger()

def get_similarity_prob(sentence_embeddings):
    """
    ------------------------------------------------------------------------------------------------------

    This function takes in a list of sentence embeddings and computes the cosine similarity between them,
    and returns the similarity score as a float.

    Parameters:
    ...........
    sentence_embeddings : list
        a list of sentence embeddings as numpy arrays

    Returns:
    ...........
    prob : float
        a float value representing the cosine similarity between the two input sentence embeddings

    ------------------------------------------------------------------------------------------------------
    """
    pscore = cosine_similarity([sentence_embeddings[0]],[sentence_embeddings[1]])
    prob = pscore[0][0]
    return prob

def match_transcript(sigma_string, speech):
    """
    ------------------------------------------------------------------------------------------------------

    The function uses a pre-trained BERT-based sentence transformer model to compute the similarity between
    the speech and a list of pre-defined PANSS or MADRS script sentences. It
    returns the average similarity score of the top 5 matches.

    Parameters:
    ...........
    sigma_string : str
        a string of sigma script
    speech : str
        a string containing the speech to be matched with the PANSS or MADRS script sentences

    Returns:
    ...........
    match_score : float
        a float value representing the average similarity score of the top 5 matches

    ------------------------------------------------------------------------------------------------------
    """
    prob_list = []

    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    sigma_script = sigma_string.split(',')

    for script in sigma_script:
        sen_list = [script, speech]

        sentence_embeddings = model.encode(sen_list)
        prob = get_similarity_prob(sentence_embeddings)
        prob_list.append(prob)

    prob_list.sort(reverse=True)
    match_score = np.mean(prob_list[:5]) #top 5 probability score
    return match_score

def prepare_diart_interval(start_time, end_time, speaker_list):
    """
    ------------------------------------------------------------------------------------------------------

    The function checks for overlapping intervals and merges them if necessary.

    Parameters:
    ...........
    start_time : list
        a list of start times as floats
    end_time : list
        a list of end times as floats
    speaker_list : list
        a list of speaker names as strings

    Returns:
    ...........
    df : pandas dataframe
        a dataframe containing the start time, end time, interval, and speaker columns

    ------------------------------------------------------------------------------------------------------
    """
    df = pd.DataFrame(start_time, columns=['start_time'])

    df['end_time'] = end_time
    df['interval'] =df['end_time'] - df['start_time']
    
    df['speaker'] = speaker_list
    return df

def get_diart_interval(diarization):
    """
    ------------------------------------------------------------------------------------------------------

    This function takes in a pyannote.core.SegmentManification object representing the diarization results
    and returns a pandas dataframe with columns for start time, end time, interval, and speaker.

    Parameters:
    ...........
    diarization : pyannote.core.SegmentManification
        a diarization object representing the diarization results

    Returns:
    ...........
    df : pandas dataframe
        a dataframe containing the start time, end time, interval, and speaker columns

    ------------------------------------------------------------------------------------------------------
    """
    start_time = []
    end_time = []
    speaker_list = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        try:

            speaker_id = str(speaker).split('_')[1]
            speaker_id = int(speaker_id)
            start_time.append(turn.start)

            end_time.append(turn.end)
            speaker_list.append('speaker'+ str(speaker_id))

        except Exception as e:
            logger.info(f'Error in pyannote filtering: {e}')

    df = prepare_diart_interval(start_time, end_time, speaker_list)
    return df

def get_patient_rater_label(df, measures, scale, signal):
    """
    ------------------------------------------------------------------------------------------------------

    This function takes in a pandas dataframe 'df' containing diarization results and returns a dictionary
    signal_label with the labels assigned to the speakers based on the comparison of their scores.

    Parameters:
    ----------
    df : pandas DataFrame
        A dataframe containing the diarization results
    measures : dict
        A dictionary with config values.
    scale : str
        A clinical scale.
    signal : list
        A list of audio signals.

    Returns:
    -------
    signal_label : dict
        A dictionary with the assigned labels for the speakers.

    ------------------------------------------------------------------------------------------------------
    """
    signal_label = {}
    spk1_txt = ' '.join(df[df['speaker_label'] == 'speaker0'].reset_index(drop=True)['content'])
    spk2_txt = ' '.join(df[df['speaker_label'] == 'speaker1'].reset_index(drop=True)['content'])

    if scale.lower() not in measures['scale'].split(","):
        return signal

    elif spk1_txt == '' and spk2_txt == '': #Check empty text
        return signal
    
    score_string = scale.lower()+'_string'
    spk1_score = match_transcript(measures[score_string], spk1_txt)
    
    spk2_score = match_transcript(measures[score_string], spk2_txt)
    signal_label = {'clinician': signal['speaker1'], 'participant':signal['speaker0']}

    if spk1_score > spk2_score:
        signal_label = {'clinician': signal['speaker0'], 'participant':signal['speaker1']}
    return signal_label

def get_segment_signal(audio_signal, df):
    """
    ------------------------------------------------------------------------------------------------------

    Extracts speaker-specific segments from an audio signal based on a dataframe.

    Parameters:
    ----------
    audio_signal : AudioSignal
        The audio signal.
    df : pandas DataFrame
        The dataframe containing speaker information.

    Returns:
    -------
    signal_dict: dict
        A dictionary with key as labled speaker and value as a List of numpy arrays representing the audio segments
        of that speaker.

    ------------------------------------------------------------------------------------------------------
    """
    signal_dict = {}

    for index, row in df.iterrows():
        start_time = row['start_time']

        end_time = row['end_time']
        speaker_label = row['speaker_label']

        speaker_audio = audio_signal[start_time:end_time]
        speaker_array = np.array(speaker_audio.get_array_of_samples())

        if speaker_label in ['speaker0', 'speaker1', 'clinician', 'participant']:
            signal_dict.setdefault(speaker_label, []).append(speaker_array)

    return signal_dict

def generate_audio_signal(df, audio_signal, scale, measures):
    """
    ------------------------------------------------------------------------------------------------------

    Generates a labeled audio signal based on the given DataFrame, audio signal, scale, and measures (common function).

    Parameters:
    ----------
    df : pandas DataFrame
        The DataFrame containing the start and end times of segments.
    audio_signal : AudioSignal
        The original audio signal.
    scale : str
        A clinical scale
    measures : dict
        A config dictionary.

    Returns:
    -------
    signal_label: dict
        A dictionary with the assigned labels for the speakers and audio signals.

    ------------------------------------------------------------------------------------------------------
    """
    df['start_time'] = df['start_time'].astype(float) *1000
    df['end_time'] = df['end_time'].astype(float)*1000

    signal_dict = get_segment_signal(audio_signal, df)
    signal_dict = {key: np.concatenate(value) for key, value in signal_dict.items()}

    signal_label = get_patient_rater_label(df, measures, scale, signal_dict)
    return signal_label

def get_speaker_identification(df1, df2):
    """
    ------------------------------------------------------------------------------------------------------

    Identifies speakers from two dataframes based on time intervals (common function).

    Parameters:
    ----------
    df1 : pandas DataFrame
        First dataframe containing speaker information.
    df2 : pandas.DataFrame
        Second dataframe containing time interval information.

    Returns:
    -------
    grouped_df : pandas.DataFrame
        A dataframe with aggregated speaker information.
    speaker_count : int
        The number of unique speaker labels identified.

    ------------------------------------------------------------------------------------------------------
    """
    # Merge the dataframes based on overlapping time intervals
    merged_df = pd.merge(df1, df2, how='cross')

    # Filter the merged dataframe based on overlapping intervals
    filtered_df = merged_df[ (merged_df['start'] >= merged_df['start_time']) &
                            (merged_df['end'] <= merged_df['end_time'])]

    # Groupby and aggregate word and conf
    filtered_df = filtered_df.rename(columns={'conf': 'confidence', 'speaker': 'speaker_label', 'word': 'content', 'start': 'start_time', 'end': 'end_time'}).iloc[:, 2:]

    filtered_df = filtered_df[["start_time", "end_time", "confidence", "speaker_label", "content"]]
    speaker_count = filtered_df['speaker_label'].nunique()
    return filtered_df, speaker_count

def transcribe_response_to_dataframe(response):
    """
    ------------------------------------------------------------------------------------------------------

    Transcribes(cloud:AWS) a response from a speech-to-text service into a pandas DataFrame.

    Parameters:
    ----------
    response : dict
        The response object containing the transcribed data.

    Returns:
    -------
    df : pandas DataFrame
        The transcribed data in a DataFrame.
    speakers: int
        The number of speakers detected in the transcription.

    ------------------------------------------------------------------------------------------------------
    """
    speakers = 0
    df = pd.DataFrame()

    if 'results' in response:
        if 'speaker_labels' in response['results']:

            if 'speakers' in response['results']['speaker_labels']:
                speakers = response['results']['speaker_labels']["speakers"]

            if 'items' in response['results']:
                items = response['results']["items"]
                df = pd.DataFrame(items)

                df["confidence"] = df["alternatives"].apply(lambda x: x[0]["confidence"])
                df["content"] = df["alternatives"].apply(lambda x: x[0]["content"])
                df["confidence"] = df["confidence"].astype(float)

                df = df[df["confidence"] > 0].reset_index(drop=True)
                df = df[["start_time", "end_time", "confidence", "speaker_label", "content"]]
                
    return df, speakers

def adjust_volume(audio_path, signal_label, volume_level):
    """
    ------------------------------------------------------------------------------------------------------

    This function adjusts the volume level of the audio signal.

    Parameters:
    ...........
    audio_path : str
        Path to the input audio file.
    signal_label : pandas.DataFrame
        A pandas dataframe containing the speaker diarization information.
    volume_level : int
        The volume normalization level.

    Returns:
    ...........
    signal_label : pandas.DataFrame
        A pandas dataframe containing the speaker diarization information.

    ------------------------------------------------------------------------------------------------------
    """
    temp_dir = tempfile.mkdtemp()
    to_audio(audio_path, signal_label, temp_dir)
    for file in os.listdir(temp_dir):
        try:
            # standardize volume level
            audio_signal = AudioSegment.from_file(file = os.path.join(temp_dir, file), format = "wav")
            audio_signal = volume_normalization(audio_signal, volume_level)
            audio_signal.export(os.path.join(temp_dir, file), format="wav")
        except Exception as e:
            logger.info(f'Error in adjusting volume for file: {file}, error: {e}')

    signal_label = from_audio(temp_dir)

    # clear the temp directory
    shutil.rmtree(temp_dir)

    return signal_label

def combine_turns(df):
    """
    ------------------------------------------------------------------------------------------------------

    Combines consecutive words of the same speaker into a single turn.

    Parameters:
    ...........
    df : pandas.DataFrame
        The dataframe containing the speaker diarization information.

    Returns:
    ...........
    combined_df : pandas.DataFrame
        The dataframe with combined turns.

    ------------------------------------------------------------------------------------------------------
    """
    change_mask = df['speaker_label'] != df['speaker_label'].shift()
    
    groups = np.cumsum(change_mask)
    
    combined_df = df.groupby(groups).agg({
        'start_time': 'first',
        'end_time': 'last',
        'confidence': 'mean',
        'speaker_label': 'first',
        'content': ' '.join
    }).reset_index(drop=True)
    
    return combined_df
