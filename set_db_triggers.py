#
# RUN THIS SCRIPT AS ADMIN AFTER INITIAL MIGRATION TO SET PG_NOTIFY TRIGGERS
# FOR MANAGE MESSAGES FROM DB TO USERS VIA MQ

from sqlalchemy import text
from api import db

with db.engine.connect() as connection:
    connection.execute(text(
        "create or replace function send_message() returns trigger "
        "language plpgsql "
        "as "
        "$$"
        "DECLARE "
        "payload text;"
        "BEGIN payload := json_build_object('project_id',NEW.project_id, 'doc_id', NEW.doc_id,"
        "'sender_id', NEW.sender_id,'ntfcn_id', NEW.ntfcn_id, 'comments', NEW.comments,"
        "'receive_status', NEW.receive_status, 'type', NEW.type, 'time_send', NEW.time_send,"
        "'time_limit', NEW.time_limit, 'text', NEW.text, 'doc_type',"
        "NEW.doc_type, 'place_id', NEW.place_id, 'read_status', NEW.read_status,"
        "'receiver_channel', NEW.receiver_channel, 'receiver_id', NEW.receiver_id);"
        "PERFORM pg_notify('new_message', payload);"
        "RETURN NEW;"
        "END;"
        "$$;"
    ))
    connection.execute(text(
        "create or replace function new_channel() returns trigger "
        "language plpgsql "
        "as "
        "$$ "
        "DECLARE "
        "payload text;"
        "BEGIN payload := json_build_object('new_channel',NEW.ntfcn_channel);"
        "PERFORM pg_notify('new_channel', payload);"
        "RETURN NEW;"
        "END;"
        "$$; "

        "CREATE TRIGGER new_channel "
        "AFTER INSERT ON user_model "
        "EXECUTE PROCEDURE new_channel()"
    ))
