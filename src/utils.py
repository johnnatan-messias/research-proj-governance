from tqdm import tqdm
import os
import pandas as pd


def parse_common_attributes(event):
    data = dict()
    data['blockNumber'] = event['blockNumber']
    data['transactionHash'] = event['transactionHash'].hex().lower()
    data['blockHash'] = event['blockHash'].hex().lower()
    data['address'] = event['address'].lower()
    data['transactionIndex'] = event['transactionIndex']
    data['logIndex'] = event['logIndex']
    data['event'] = event['event']
    return data


def approval_to_dataframe(events, decimals=1e18):
    # Convert Approval events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading Approval events'):
        data = parse_common_attributes(event)

        data['owner'] = event['args']['owner'].lower()
        data['spender'] = event['args']['spender'].lower()
        data['amount'] = event['args']['amount'] / decimals
        df.append(data)
    return pd.DataFrame(df)


def new_implementation_to_dataframe(events):
    # Convert NewImplementation events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading NewImplementation events'):
        data = parse_common_attributes(event)

        data['oldImplementation'] = event['args']['oldImplementation'].lower()
        data['newImplementation'] = event['args']['newImplementation'].lower()
        df.append(data)
    return pd.DataFrame(df)


def proposal_threshold_set_to_dataframe(events, decimals=1e18):
    # Convert ProposalThresholdSet events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalThresholdSet events'):
        data = parse_common_attributes(event)

        data['oldProposalThreshold'] = event['args']['oldProposalThreshold'] / decimals
        data['newProposalThreshold'] = event['args']['newProposalThreshold'] / decimals
        df.append(data)
    return pd.DataFrame(df)


def voting_delay_set_to_dataframe(events):
    # Convert VotingDelaySet events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading VotingDelaySet events'):
        data = parse_common_attributes(event)

        data['oldVotingDelay'] = event['args']['oldVotingDelay']
        data['newVotingDelay'] = event['args']['newVotingDelay']
        df.append(data)
    return pd.DataFrame(df)


def delegate_changed_to_dataframe(events):
    # Convert DelegateChanged events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading DelegateChanged events'):
        data = parse_common_attributes(event)

        data['delegator'] = event['args']['delegator'].lower()
        data['fromDelegate'] = event['args']['fromDelegate'].lower()
        data['toDelegate'] = event['args']['toDelegate'].lower()
        df.append(data)
    return pd.DataFrame(df)


def delegate_votes_changed_to_dataframe(events, decimals=1e18):
    # Convert DelegateVotesChanged events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading DelegateVotesChanged events'):
        data = parse_common_attributes(event)

        data['delegate'] = event['args']['delegate'].lower()
        data['previousBalance'] = event['args']['previousBalance'] / decimals
        data['newBalance'] = event['args']['newBalance'] / decimals
        df.append(data)
    return pd.DataFrame(df)


def minter_changed_to_dataframe(events):
    # Convert MinterChanged events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading MinterChanged events'):
        data = parse_common_attributes(event)
        data['minter'] = event['args']['minter'].lower()
        data['newMinter'] = event['args']['newMinter'].lower()
        df.append(data)
    return pd.DataFrame(df)


def transfer_to_dataframe(events, decimals=1e18):
    # Convert Transfer events data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading Transfer events'):
        data = parse_common_attributes(event)

        data['from'] = event['args']['from'].lower()
        data['to'] = event['args']['to'].lower()
        data['amount'] = event['args']['amount'] / decimals
        df.append(data)
    return pd.DataFrame(df)


# def parse_common_attributes(event):
#     data = dict()
#     data['blockNumber'] = event['blockNumber']
#     try:
#         data['transactionHash'] = event['transactionHash'].hex().lower()
#     except AttributeError:
#         data['transactionHash'] = event['transactionHash'].lower()
#     try:
#         data['blockHash'] = event['blockHash'].hex().lower()
#     except AttributeError:
#         data['blockHash'] = event['blockHash'].lower()
#     data['address'] = event['address'].lower()
#     data['transactionIndex'] = event['transactionIndex']
#     data['logIndex'] = event['logIndex']
#     data['event'] = event['event']
#     return data


def vote_cast_to_dataframe(events, decimals=1e18):
    # Convert vote cast data to dataframe
    df = list()
    for event in tqdm(events, desc='Loading VoteCast events'):
        data = dict()
        data = parse_common_attributes(event)
        data['proposalId'] = event['args']['proposalId']
        data['support'] = event['args']['support']
        data['votes'] = event['args']['votes'] / decimals
        data['voter'] = event['args']['voter'].lower()
        if 'reason' in event['args']:
            data['reason'] = event['args']['reason']
        df.append(data)
    return pd.DataFrame(df)


def proposal_created_to_dataframe(events):
    # Convert the proposal created data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalCreated events'):
        data = dict()
        data = parse_common_attributes(event)
        data['proposalId'] = event['args']['id']
        data['startBlock'] = event['args']['startBlock']
        data['endBlock'] = event['args']['endBlock']
        data['proposer'] = event['args']['proposer'].lower()
        data['targets'] = ','.join(event['args']['targets']).lower()
        data['values'] = ','.join(map(str, event['args']['values']))
        data['signatures'] = ','.join(event['args']['signatures'])
        data['description'] = event['args']['description']
        df.append(data)
    return pd.DataFrame(df)


def proposal_cancelled_to_dataframe(events):
    # Convert the proposal cancelled data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalCancelled events'):
        data = dict()
        data = parse_common_attributes(event)
        data['proposalId'] = event['args']['id']
        df.append(data)
    return pd.DataFrame(df)


def proposal_queued_to_dataframe(events):
    # Convert the proposal queued data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalQueued events'):
        data = dict()
        data = parse_common_attributes(event)
        data['proposalId'] = event['args']['id']
        data['eta'] = pd.to_datetime(event['args']['eta'], unit='s')
        df.append(data)
    return pd.DataFrame(df)


def proposal_executed_to_dataframe(events):
    # Convert the proposal executed data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalExecuted events'):
        data = dict()
        data = parse_common_attributes(event)
        data['proposalId'] = event['args']['id']
        df.append(data)
    return pd.DataFrame(df)


def proposal_voting_delay_to_dataframe(events):
    # Convert the proposal voting delay data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading ProposalVotingDelaySet events'):
        data = dict()
        data = parse_common_attributes(event)
        data['oldVotingDelay'] = event['args']['oldVotingDelay']
        data['newVotingDelay'] = event['args']['newVotingDelay']
        df.append(data)
    return pd.DataFrame(df)


def voting_period_set_to_dataframe(events):
    # Convert the VotingPeriodSet data to a dataframe
    df = list()
    for event in tqdm(events, desc='Loading VotingPeriodSet events'):
        data = dict()
        data = parse_common_attributes(event)
        data['oldVotingPeriod'] = event['args']['oldVotingPeriod']
        data['newVotingPeriod'] = event['args']['newVotingPeriod']
        df.append(data)
    return pd.DataFrame(df)


def load_dataframes(path_dir):
    filenames = [filename for filename in os.listdir(
        path_dir) if filename.endswith('.csv.gz')]
    dfs = dict()

    for filename in tqdm(filenames, desc="Loading dataframes"):
        df = pd.read_csv(path_dir + filename)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        dfs[filename.split('.')[0]] = df
    return dfs

