import pickle
from pathlib import Path

# Fix framework BM25 files with correct structure
data = {'bm25': None, 'chunk_ids': [], 'tokenized_corpus': []}
fw_dir = Path('api/indexes/framework')

for f in ['naac_metric_bm25.pkl', 'naac_policy_bm25.pkl', 'nba_metric_bm25.pkl', 'nba_policy_bm25.pkl', 'nba_prequalifier_bm25.pkl']:
    with open(fw_dir / f, 'wb') as file:
        pickle.dump(data, file)
    print(f'Fixed {f}')

print('All framework BM25 files fixed!')
