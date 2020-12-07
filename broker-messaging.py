import argparse
from message import Message

version = "broker-messagin v0.1"

desc = "Process a list of messages and returns the valid ones"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("file", help="file containing messages")


def process_message(line):
    """ Prints the ID and the Broker number if a message is valid """
    try:
        msg = Message.from_string(line)

        valid = msg.validate_message()
        if valid:
            print(msg.msg_id + ';' + str(msg.broker()))
    except:
        print("ERROR: Invalid message format")

if __name__ == "__main__":
    args = parser.parse_args()

    # opens the file and read it line by line
    with open(args.file, 'r') as f:
        while True:
            line = f.readline()
            if line:
                process_message(line)
            else:
                break
