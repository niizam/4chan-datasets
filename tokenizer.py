import sys
import re
import json
import csv
from transformers import AutoTokenizer

def format_data(input_file):
    with open(input_file, 'r') as file:
        content = file.read()

    raw_posts = content.split('---')
    formatted_data = []
    for post in raw_posts:
        post = post.strip()
        if post:
            post_id_match = re.search(r'\d+', post)
            if post_id_match:
                post_id = post_id_match.group()
                post_text = post[len(post_id):].strip()
                token_length = len(post_text.split())
                formatted_data.append({
                    'id': len(formatted_data) + 1,
                    'author': post_id,
                    'text': post_text,
                    'token_length': token_length
                })

    return formatted_data

def save_data(tokenized_data, output_file, file_format='json'):
    if file_format == 'json':
        with open(output_file, 'w') as json_file:
            json.dump(tokenized_data, json_file, indent=2)
    elif file_format == 'csv':
        with open(output_file, 'w') as csv_file:
            fieldnames = ['id', 'author', 'text', 'token_length']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for post in tokenized_data:
                writer.writerow(post)
    else:
        raise ValueError('Invalid file format. Use "json" or "csv".')

def tokenize_posts(formatted_data, model_name='distilbert-base-uncased', max_length=2048):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenized_data = []

    for post in formatted_data:
        post['tokens'] = tokenizer.encode(post['text'], return_tensors='pt', truncation=True, max_length=max_length)
        post['token_length'] = len(post['tokens'][0])
        tokenized_data.append(post)

    return tokenized_data

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python transform.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    file_format = 'json' if output_file.endswith('.json') else 'csv'

    formatted_data = format_data(input_file)
    save_data(formatted_data, output_file, file_format=file_format)
