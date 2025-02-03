async def handle_decoded_packet(final_response, packet):
    try:
        res = {}
        for i in range(len(packet)):
            if not packet[i][0].isupper():
                res[packet[i-1].split(':')[0]] = packet[i-1].split(':')[1] + " " + packet[i]
            else:
                res[packet[i].split(':')[0]] = packet[i].split(':')[1]
        final_response['response'] = res
        
        return final_response
    
    except Exception as e:
        return {"response" : " ".join(packet).strip('{}')}