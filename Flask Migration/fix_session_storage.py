#!/usr/bin/env python3
"""
Quick fix script to replace all session storage references with file-based storage.
"""

import re

def fix_session_storage():
    """Replace in-memory session storage with file-based storage."""
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Pattern to match analytics route data loading
    analytics_pattern = r'''    # Load results from server-side storage
    data_session_id = session\['data_session_id'\]
    stored_data = session_data_store\[data_session_id\]
    results = pd\.read_json\(StringIO\(stored_data\['results'\]\), orient='records'\)'''
    
    analytics_replacement = r'''    # Load results from file storage
    username = session.get('username', 'unknown')
    stored_data = load_session_data(username, session['data_session_id'])
    if not stored_data:
        flash('Session data expired. Please upload files again.', 'warning')
        return redirect(url_for('upload_files'))
    results = pd.read_json(StringIO(stored_data['results']), orient='records')'''
    
    content = re.sub(analytics_pattern, analytics_replacement, content)
    
    # Pattern for all session data checks
    check_pattern = r"if 'data_session_id' not in session or session\['data_session_id'\] not in session_data_store:"
    check_replacement = r"stored_data = None\n    if 'data_session_id' in session:\n        stored_data = load_session_data(session.get('username', 'unknown'), session['data_session_id'])\n    if not stored_data:"
    
    content = re.sub(check_pattern, check_replacement, content)
    
    # Pattern for all data retrieval from session_data_store
    retrieval_pattern = r'''        # Retrieve data from server-side storage
        data_session_id = session\['data_session_id'\]
        stored_data = session_data_store\[data_session_id\]
        results = pd\.read_json\(StringIO\(stored_data\['results'\]\), orient='records'\)'''
    
    retrieval_replacement = r'''        # Retrieve data from file storage
        username = session.get('username', 'unknown')
        stored_data = load_session_data(username, session['data_session_id'])
        if not stored_data:
            flash('Session data expired. Please upload files again.', 'warning')
            return redirect(url_for('upload_files'))
        results = pd.read_json(StringIO(stored_data['results']), orient='records')'''
    
    content = re.sub(retrieval_pattern, retrieval_replacement, content)
    
    # Simple replacements
    content = content.replace("session_data_store[data_session_id]", "stored_data")
    content = content.replace("session_data_store[session_id]", "stored_data")
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("Session storage patterns fixed!")

if __name__ == '__main__':
    fix_session_storage()