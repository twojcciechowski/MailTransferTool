import imaplib
import email
import os


SOURCE_HOST=os.getenv("SOURCE_HOST")
SOURCE_PORT=os.getenv("SOURCE_PORT")
SOURCE_USER = os.getenv("SOURCE_USER")
SOURCE_PASSWORD = os.getenv("SOURCE_PASSWORD")

TARGET_HOST=os.getenv("TARGET_HOST")
TARGET_PORT=os.getenv("TARGET_PORT")
TARGET_USER = os.getenv("TARGET_USER")
TARGET_PASSWORD = os.getenv("TARGET_PASSWORD")

print("SOURCE:")
print("- Host: {}".format(SOURCE_HOST))
print("- Port: {}".format(SOURCE_PORT))
print("- Username: {}".format(SOURCE_USER))
print("- Password: {}".format(SOURCE_PASSWORD))

print("TARGET:")
print("- Host: {}".format(TARGET_HOST))
print("- Port: {}".format(TARGET_PORT))
print("- Username: {}".format(TARGET_USER))
print("- Password: {}".format(TARGET_PASSWORD))


def parseBoxName(box):
    return "/".join(box.decode('utf-8').replace('"', '').split("/ ")[1:])

def transfer_messages(folder):
    print("Transfering emails from folder: " + folder)

    read_folder='"{}"'.format(folder)
    response,data=read_connection.select(read_folder,True)
    if "NO" == response:
        print("Nothing to transfer from: {}".format(folder))
        return

    typ, data = read_connection.uid('search', None, "ALL")

    write_connection.create("upload-test/")
    write_folder='"upload-test/{}"'.format(folder)
    write_connection.create(write_folder)

    uids = [s for s in data[0].split()]
    for uid in uids:
        typ, data = read_connection.uid("fetch", uid, '(RFC822)')

        tuple_idx=0
        for idx,d in enumerate(data):
            if type(d) is tuple:
                tuple_idx=idx
                break

        msg_bytes=data[tuple_idx][1]

        if len(msg_bytes)>0 :
            msg = email.message_from_bytes(msg_bytes)
            received = msg.get('Date')
            write_connection.append(
                write_folder,
                None,
                email.utils.parsedate(received),
                msg_bytes)

read_connection = imaplib.IMAP4_SSL(host=SOURCE_HOST, port=SOURCE_PORT)
read_connection.login(user=SOURCE_USER, password=SOURCE_PASSWORD)

write_connection = imaplib.IMAP4_SSL(host=TARGET_HOST, port=TARGET_PORT)
write_connection.login(user=TARGET_USER, password=TARGET_PASSWORD)

_, boxes = read_connection.list()

for box in boxes:
    transfer_messages(parseBoxName(box))

