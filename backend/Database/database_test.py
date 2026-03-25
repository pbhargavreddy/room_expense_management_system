from backend.Database.database import engine

try:
    conn = engine.connect()
    print("Connected succesfully")
    conn.close()
except Exception as e:
    print('Failed to connect: ',e)
