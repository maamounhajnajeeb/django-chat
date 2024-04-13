
def message_to_json(message):
    return {
        'author': message.author.username,
        'content': message.content,
        # 'timestamp': message.timestamp
    }

def messages_to_json(messages):
    result = list()

    for message in messages:
        result.append(message_to_json(message))
    
    return result
