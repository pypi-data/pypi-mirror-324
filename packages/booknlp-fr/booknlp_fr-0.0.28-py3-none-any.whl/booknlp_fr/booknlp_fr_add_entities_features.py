from .booknlp_fr_number import assign_number_to_PER_entities
from .booknlp_fr_gender import assign_gender_to_PER_entities

import pkg_resources
import numpy as np
from tqdm.auto import tqdm
import pandas as pd
from collections import Counter

def add_mention_number_and_gender_infos(entities_df):
    # Locate the CSV file within the package
    insee_path = pkg_resources.resource_filename('booknlp_fr', 'data/insee_names_fr_1900_2023.csv')
    # print("Insee_data Loaded successfully.")

    entities_df['number'] = assign_number_to_PER_entities(entities_df)['number']
    entities_df['gender'] = assign_gender_to_PER_entities(entities_df, insee_path=insee_path)['gender']

    not_PER_entities = entities_df[entities_df['cat'] != "PER"].copy()
    entities_df.loc[not_PER_entities.index, 'number'] = 'Not_Assigned'
    entities_df.loc[not_PER_entities.index, 'gender'] = 'Not_Assigned'

    return entities_df

## General entities_df functions
def add_mention_paragraphe_and_sentence_infos(entities_df, tokens_df):
    start_token_ids = entities_df['start_token'].tolist()
    entities_df['paragraph_ID'] = tokens_df.loc[start_token_ids, 'paragraph_ID'].tolist()
    entities_df['sentence_ID'] = tokens_df.loc[start_token_ids, 'sentence_ID'].tolist()
    entities_df['start_token_ID_within_sentence'] = tokens_df.loc[start_token_ids, 'token_ID_within_sentence'].tolist()
    return entities_df
def get_outer_to_inner_nesting_level(entities_df):
    # Step 1: Sort entities by start_token ascending, then by end_token descending
    entities_df = entities_df.sort_values(by=['start_token', 'end_token'], ascending=[True, False]).reset_index(drop=True)

    # Step 2: Initialize nested levels
    nested_levels = np.zeros(len(entities_df), dtype=int)

    # Step 3: Track active ranges (sorted by end_token)
    active_ranges = []

    for i, (start, end) in enumerate(zip(entities_df['start_token'], entities_df['end_token'])):
        # Remove ranges from active_ranges that are no longer active (end < start of the current mention)
        active_ranges = [ar for ar in active_ranges if ar[1] >= start]

        # The current level is the size of active_ranges
        nested_levels[i] = len(active_ranges)

        # Add the current range to active_ranges
        active_ranges.append((start, end))

    # Step 4: Assign the calculated nested levels back to the DataFrame
    entities_df['out_to_in_nested_level'] = nested_levels

    return entities_df
def get_inner_to_outer_nesting_level(entities_df):
    # Step 1: Initialize levels to 0
    entities_df["in_to_out_nested_level"] = 0

    # Step 2: Filter non-monogram entities and sort by mention length (ascending)
    non_monogram_entities = entities_df[entities_df["mention_len"] > 1].sort_values("mention_len", ascending=True)
    non_monogram_entities["temp_index"] = non_monogram_entities.index

    # Step 3: Convert DataFrame columns to NumPy arrays for faster indexing
    start_tokens = entities_df["start_token"].values
    end_tokens = entities_df["end_token"].values
    mention_lengths = entities_df["mention_len"].values
    nested_levels = entities_df["in_to_out_nested_level"].values

    # Step 4: Iterate over non-monogram entities
    for temp_index, start_token, end_token, mention_len in non_monogram_entities[["temp_index", "start_token", "end_token", "mention_len"]].values:
        # Step 5: Filter candidates for potential nesting
        candidates_mask = (mention_lengths < mention_len) & \
                          (start_tokens >= start_token) & \
                          (end_tokens <= end_token)

        # Step 6: Update nesting level if candidates exist
        if candidates_mask.any():
            max_nested_level = nested_levels[candidates_mask].max() + 1
            nested_levels[temp_index] = max_nested_level

    # Step 7: Assign the updated levels back to the DataFrame
    entities_df["in_to_out_nested_level"] = nested_levels

    return entities_df
def get_nested_entities_count(entities_df):
    # Step 1: Initialize count column
    entities_df["nested_entities_count"] = 0
    entities_df["temp_index"] = entities_df.index

    # Step 2: Extract values as NumPy arrays for speed
    start_tokens = entities_df["start_token"].values
    end_tokens = entities_df["end_token"].values
    mention_lengths = entities_df["mention_len"].values
    nested_counts = np.zeros(len(entities_df), dtype=int)

    # Step 3: Filter outer entities (which contain other entities)
    outer_mask = entities_df["in_to_out_nested_level"].values > 0
    outer_indices = np.where(outer_mask)[0]

    # Step 4: Iterate efficiently over outer entities
    for idx in outer_indices:
        start_token, end_token, mention_len = start_tokens[idx], end_tokens[idx], mention_lengths[idx]

        # Vectorized filtering for inner mentions
        inside_mask = (mention_lengths < mention_len) & \
                      (start_tokens >= start_token) & \
                      (end_tokens <= end_token)

        # Store the count of nested entities
        nested_counts[idx] = np.sum(inside_mask)

    # Step 5: Assign results back to DataFrame
    entities_df["nested_entities_count"] = nested_counts

    return entities_df
def assign_mention_head_id(entities_df, tokens_df):
    entities_df['head_id'] = entities_df['start_token']
    filtered_entities_df = entities_df[entities_df['mention_len'] != 1]

    # Prepare a dictionary to store the results
    mention_head_ids = []

    # Iterate over each entity in entities_df
    for start_token, end_token in tqdm(zip(filtered_entities_df['start_token'], filtered_entities_df['end_token']),
                                       total=len(filtered_entities_df), desc="Extracting Mention Head Infos",
                                       leave=False):
        # Get a subset of tokens_df directly for the token range
        mention_token_df = tokens_df.loc[start_token:end_token].copy()

        # Identify if the head is inside the mention
        mention_token_df['head_is_inside_mention'] = mention_token_df['syntactic_head_ID'].isin(
            mention_token_df['token_ID_within_document'])
        mention_token_df = mention_token_df.sort_values(by=['head_is_inside_mention'], ascending=[True])

        if np.array_equal(mention_token_df['head_is_inside_mention'].values[:2], [False, True]):
            pass

        else:
            # Calculate the count of each head ID directly using numpy
            head_id_counts = np.bincount(
                mention_token_df['syntactic_head_ID'].values, minlength=tokens_df['token_ID_within_document'].max() + 1
            )
            mention_token_df['head_count'] = mention_token_df['syntactic_head_ID'].map(lambda x: head_id_counts[x])

            # Sort based on 'head_is_inside_mention' and 'head_count'
            mention_token_df = mention_token_df.sort_values(by=['head_is_inside_mention', 'head_count'],
                                                            ascending=[True, False])

        # Get the head ID for the mention
        mention_head_id = mention_token_df.index[0]
        mention_head_ids.append(mention_head_id)

    entities_df.loc[filtered_entities_df.index, "head_id"] = mention_head_ids

    return entities_df
def mention_head_syntactic_infos(entities_df, tokens_df):
    head_token_ids = entities_df['head_id'].tolist()
    head_tokens_rows = tokens_df.loc[head_token_ids, ['word', 'dependency_relation', 'syntactic_head_ID']]
    entities_df[['head_word', 'head_dependency_relation', 'head_syntactic_head_ID']] = head_tokens_rows.values.tolist()
    return entities_df
def assign_mention_prop(entities_df, tokens_df):
    # Define the mapping dictionary
    mapping_dict = {
        'PROPN': 'PROP',
        'PRON': 'PRON',
        'DET': 'PRON',
        'ADP': 'PRON',
        'PUNCT': 'PRON',
        'NOUN': 'NOM',
    }
    default_value = "NOM"

    entities_df['POS_tag'] = pd.merge(entities_df['head_id'], tokens_df, left_on='head_id', right_index=True)['POS_tag']
    # Use map to apply the mapping dictionary, setting unmapped values to NaN

    # Apply the mapping dictionary to the 'POS_tag' column
    entities_df['prop'] = entities_df['POS_tag'].map(mapping_dict).fillna(default_value)

    special_pronouns_tokens = ['moi', 'mien', 'miens', 'mienne', 'miennes', 'tien', 'tiens', 'tienne', 'tiennes',
                               'vôtre', 'vôtres', 'siens', 'siennes', 'sien']
    special_pronouns_tokens_id = list(tokens_df[tokens_df['word'].str.lower().isin(special_pronouns_tokens)].index)
    head_id_in_special_tokens = list(entities_df[entities_df['head_id'].isin(special_pronouns_tokens_id)].index)
    entities_df.loc[head_id_in_special_tokens, ['prop']] = "PRON"

    # Propagate PROP tag to all
    occurrence_treshold = 5
    proper_name_mentions = dict(Counter(entities_df[entities_df['prop'] == 'PROP']['text']))
    proper_name_mentions = [key for key in proper_name_mentions.keys() if
                            proper_name_mentions[key] >= occurrence_treshold]
    proper_rows = entities_df[entities_df['text'].isin(proper_name_mentions)]
    entities_df.loc[proper_rows.index, 'prop'] = 'PROP'

    always_pronouns_mentions = ['je', 'me', 'moi', "j'", "m'", 'mon', 'ma', 'mes', 'nous', 'notre', 'nos', 'moi - même', 'moi-même', 'mien', 'miens', 'mienne',
                                'miennes', 'nôtre', 'nous-mêmes', 'nous - mêmes', 'tu', 'toi', 'te', "t'", 'ton', 'ta', 'tes', 'vous', 'vôtre', 'vos', 'votre',
                                'tien', 'tiens', 'tienne', 'tiennes', 'vous - même', 'vous-même', 'toi-même', 'toi - même', 'vous-mêmes', 'vous - mêmes', 'il',
                                'elle', 'lui', 'son', 'sa', "l'", 'ses', 'le', 'la', 'se', 'ils', 'elles', 'leur', 'les', 'leurs', 'eux', "s'", 'elle-même',
                                'lui-même', 'sienne', 'sien', 'sienne', 'siennes','un', 'une', "l' autre", 'tous', 'celui-ci', 'duquel', 'celle', 'celui', 'qui',
                                'que', 'dont', "qu'", "eux - mêmes", "eux-mêmes", "elles - mêmes", "elles-mêmes"]
    pronoun_rows = entities_df[entities_df['text'].isin(always_pronouns_mentions)]
    entities_df.loc[pronoun_rows.index, 'prop'] = 'PRON'

    always_noun_mentions = ['madame', 'mademoiselle', "monsieur", "papa", "maman"]
    noun_rows = entities_df[entities_df['text'].isin(always_noun_mentions)]
    entities_df.loc[noun_rows.index, 'prop'] = 'NOM'

    return entities_df
def assign_grammatical_person(entities_df):
    grammatical_person_dict = {"1": ['je', 'me', 'moi', "j'", "m'", 'mon', 'ma', 'mes', 'nous', 'notre', 'nos', 'moi - même', 'moi-même', 'mien', 'miens', 'mienne','miennes', 'nôtre', 'nous-mêmes', 'nous - mêmes'],
                               "2": ['tu', 'toi', 'te', "t'", 'ton', 'ta', 'tes', 'vous', 'vôtre', 'vos', 'votre', 'tien', 'tiens', 'tienne', 'tiennes', 'vous - même', 'vous-même', 'toi-même', 'toi - même', 'vous-mêmes', 'vous - mêmes'],
                               "3": ['il', 'elle', 'lui', 'son', 'sa', "l'", 'ses', 'le', 'la', 'se', 'ils', 'elles', 'leur', 'les', 'leurs', 'eux', "s'", 'elle-même', 'lui-même', 'sienne', 'sien', 'sienne', 'siennes','un', 'une', "l' autre", 'tous', 'celui-ci', 'duquel', 'celle', 'celui'],
                               "4": ['qui', 'que', 'dont', "qu'"]}

    # Reverse the dictionary to map each word to its grammatical person
    word_to_person = {word: person for person, words in grammatical_person_dict.items() for word in words}

    # Map entities_df['text'].str.lower() to grammatical persons
    entities_df['grammatical_person'] = entities_df['text'].str.lower().map(word_to_person).fillna("3").astype(int)
    return entities_df

def add_features_to_entities(entities_df, tokens_df):
    entities_df['mention_len'] = entities_df['end_token'] + 1 - entities_df['start_token']
    entities_df = add_mention_paragraphe_and_sentence_infos(entities_df, tokens_df)
    entities_df = get_outer_to_inner_nesting_level(entities_df)
    entities_df = get_inner_to_outer_nesting_level(entities_df)
    entities_df = get_nested_entities_count(entities_df)
    entities_df = assign_mention_head_id(entities_df, tokens_df)
    entities_df = mention_head_syntactic_infos(entities_df, tokens_df)
    entities_df = assign_mention_prop(entities_df, tokens_df)
    entities_df = add_mention_number_and_gender_infos(entities_df)
    entities_df = assign_grammatical_person(entities_df)
    return entities_df