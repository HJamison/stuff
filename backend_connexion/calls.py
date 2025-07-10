import os
import json
import logging
import requests 
from flask import Response
import flask

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
if not API_URL:
    raise RuntimeError("API_URL environment variable not set")
#API_URL = API_URL.rstrip("/")
n_chunks = 5
develop_mode = False

def call_semantic_query(query, document_ids=None):
    params = {
        'query': query,
        'n_chunks_to_return': n_chunks
    }
    if document_ids is not None:
        params['document_ids'] = document_ids
    headers = {'x-api-key': API_KEY}
    response = requests.get(f"{API_URL}/semantic_query", params=params, headers=headers, verify=False)
    return response

# contextual search endpoint

def contextsearch(body):
    query = body.get('query')
    chat_history = body.get('chat_history', None)
    if not query:
        return Response(json.dumps({"error": "Query is required"}), status=400, mimetype="application/json")
    
    response = call_llm_contextual_search(query, chat_history)
    
    if response.status_code == 200:
        return Response(response.content, status=200, mimetype="application/json")
    else:
        return Response(response.content, status=response.status_code, mimetype="application/json")
    
def call_llm_contextual_search(query, document_ids=None, chat_history=None):
    params = {
        'query': query,
        'n_chunks_to_return': n_chunks,
        'develop_mode': develop_mode
    }
    if document_ids is not None:
        params['document_ids'] = document_ids
    headers = {'x-api-key': API_KEY}
    data = {'chat_history': chat_history} if chat_history is not None else None
    response = requests.post(f"{API_URL}/llm_contextual_search", params=params, json=data, headers=headers, verify=False)
    return response

# This function is used to call the LLM with a regular question without any context

def question(body):
    query = body.get('query')
    chat_history = body.get('chat_history', None)
    if not query:
        return Response(json.dumps({"error": "Query is required"}), status=400, mimetype="application/json")
    
    response = call_llm_regular_question(query, chat_history)
    
    if response.status_code == 200:
        return Response(response.content, status=200, mimetype="application/json")
    else:
        return Response(response.content, status=response.status_code, mimetype="application/json")
    
def call_llm_regular_question(query, chat_history=None):
    params = {
        'query': query,
        'develop_mode': develop_mode
    }
    headers = {'x-api-key': API_KEY}
    data = {'chat_history': chat_history} if chat_history is not None else None
    response = requests.post(f"{API_URL}/llm_regular_question", params=params, json=data, headers=headers, verify=False)
    return response

def call_get_all_document_info():
    headers = {'x-api-key': API_KEY}
    response = requests.get(f"{API_URL}/get_all_document_info", headers=headers, verify=False)
    return response

# for Api calls counter 
def call_n_api_calls_left():
    headers = {'x-api-key': API_KEY}
    response = requests.get(f"{API_URL}/n_api_calls_left", headers=headers, verify=False)
    return response

def apiCallsLeft():
    response = call_n_api_calls_left()
    if response.status_code == 200:
        data = response.json()
        logging.info(data)
        return {"calls_left": data.get('calls_left')}
    else:
        logging.error(f"Failed to fetch API calls left: {response.status_code}")
        return {"calls_left": 0}

# for LLM calls counter
def call_n_llm_calls_left():
    headers = {'x-api-key': API_KEY}
    response = requests.get(f"{API_URL}/n_llm_calls_left", headers=headers, verify=False)
    return response

def llmCallsLeft():
    response = call_n_llm_calls_left()
    if response.status_code == 200:
        data = response.json()
        logging.info(data)
        return {"calls_left": data.get('calls_left')}
    else:
        logging.error(f"Failed to fetch LLM calls left: {response.status_code}")
        return {"calls_left": 0}

# Add this function to your calls.py
def options_handler():
    return {}, 200

# Add these functions to your calls.py
def options_handler_api_calls():
    return {}, 200

def options_handler_llm_calls():
    return {}, 200

def options_handler_question():
    return {}, 200

def options_handler_contextsearch():
    return {}, 200

def options_handler_settings():
    return {}, 200

# Add or update these functions
def get_settings():
    global n_chunks, develop_mode
    return {"n_chunks": n_chunks, "developer": develop_mode}

def update_settings(body):
    global n_chunks, develop_mode
    if 'n_chunks' in body and body['n_chunks'] is not None and (body['n_chunks'] <= 10):
        n_chunks = body['n_chunks']
    if 'developer' in body and body['developer'] is not None:
        develop_mode = body['developer']
    return {"n_chunks": n_chunks, "developer": develop_mode}