from confluent_kafka import Consumer
from fastapi import FastAPI
import musicanalizer


app = FastAPI(title="Kafka Consumer")

config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'stem-analyze',          
        'auto.offset.reset': 'earliest'
    }

@app.get("/")
def root(): 
    startStem()
    return {"message": "Successfully consumed"}        



def startStem():
    consumer = Consumer(config)
    consumer.subscribe(['my-topic'])
        
    while True:
        msg = consumer.poll(1.0)
        if msg is not None:
            print(f"Message: {msg.value()}")
            musicanalizer.separate_audio(msg.value().decode("utf-8"))
            consumer.commit(msg)  # Mark message as completed
        else:
            return "done"    
    