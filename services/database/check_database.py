from database.config import Mongo

mongo = Mongo()

if __name__ == "__main__":
    try:
        mongo.connect()
        mongo.disconnect()
        exit(1)
    except Exception as e:
        print("Error! {}".format(e))
        exit(0)
