
examples = [
    {
        "inputs": {
            "input": "Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
            "messages": messages,
        },
        "outputs": {
            "answer": """Hello! I'm here to help you practice Internal Family Systems (IFS) therapy.
            Do you have any questions about IFS, or would you like to start a session?""",
        },
    },
    {
        "inputs": {
            "input": "Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
            "messages": [{"role": "user",
            "content": "Hello"}]
        },
        "outputs": {
            "answer": """Hello! I'm here to help you practice Internal Family Systems (IFS) therapy.
            Do you have any questions about IFS, or would you like to start a session?""",
        },
    },
    {
        "inputs": {
            "input": "Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
            "messages": [{"role": "user",
            "content": "Hey, what's up?"}]
        },
        "outputs": {
            "answer": """Hello! I'm here to help you practice Internal Family Systems (IFS) therapy.
            Do you have any questions about IFS, or would you like to start a session?""",
        },
    },
    {
        "inputs": {
            "input": "Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.",
            "messages": [{"role": "user",
            "content": "Hi??"}]
        },
        "outputs": {
            "answer": """Hello! I'm here to help you practice Internal Family Systems (IFS) therapy.
            Do you have any questions about IFS, or would you like to start a session?""",
        },
    }

]

multiturn_examples = [
    {
        "inputs": {
            "input": "Hi.",
        },
        "outputs": {
            "answer": """Hello! I'm here to help you practice Internal Family Systems (IFS) therapy.
            Do you have any questions about IFS, or would you like to start a session?""",
        },
    },
    {
        "inputs": {
            "input": "What did I just say?",
        },
        "outputs": {
            "answer": """You just said 'Hi.'""",
        },
    }
]

messages = [{'content': """Your job is to help people practice IFS.
  Don't respond with numbered instructions.\nPlease follow the following steps:\n\n0. Introduce yourself and your role. Ask if they have questions about IFS or want to start a session.\n1. Ask if there's a feeling, struggle, thought pattern, or part they need help with.\n2. Thank them, mirror using parts language, and confirm understanding.\n3. Ask if they're aware of this part, and if they can feel it in their body.\n4. Ask how they feel toward the target part.\n5. If the user feels negative qualities, help them unblend.\n6. If the user confirms the feelings are from Self and they feel positively toward the part, ask them to share their feelings.\n7. Ask how the part received the shared feelings.\n""",
   'type': 'system'},
 {'content': 'Hi', 'type': 'human'},
  {'content': 'Introduce yourself and your role as an IFS coach. Ask if they have questions about IFS or want to start a session.', 'type': 'human'},
 {'content': 'Lets start a session', 'type': 'human'},
 {'content': "Ask if there's a feeling, struggle, thought pattern, or part they need help with.", 'type': 'human'},
  {'content': 'Yes, I feel some anxiety in the back of my neck', 'type': 'human'},
   {'content': 'suggested next question: Ask how they feels towards the target part.  For example, are they ok with the part being there?', 'type': 'human'}
]