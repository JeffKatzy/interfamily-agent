from langchain_core.chat_history import BaseChatMessageHistory

store = {}
clients = {}
def get_session(user_id: str, session_id: str = '') -> dict or None:
    if user_id and session_id:
        return store.get(user_id, {}).get(session_id, None)
    if user_id in store:
        return list(store[user_id].values())[-1] # last session

def add_session_to_store(session):
    if session.user_id not in store:
        store[session.user_id] = {}
    store[session.user_id][session.session_id] = session

def get_session_history(user_id: str, session_id: str = '') -> BaseChatMessageHistory:
    return store.get(user_id, {}).get(session_id, {}).get('history', None)
    
