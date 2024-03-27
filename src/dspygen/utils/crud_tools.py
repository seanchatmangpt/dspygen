import hashlib
import json
from datetime import datetime, timedelta

from contextlib import contextmanager

from dspygen.experiments.rfc5545.ical_db_session import get_session


def get_model(model_cls, model_id):
    session = get_session()
    model = session.get(model_cls, model_id)
    return model


def delete_model(model_cls, model_id):
    session = get_session()
    model = session.get(model_cls, model_id)
    if model:
        session.delete(model)

        # doc_id = hashlib.sha256(str(model_id).encode()).hexdigest()[:20]
        # get_mem_store().delete(
        #     collection_id=f"{model.__class__.__name__}_collection", doc_id=doc_id
        # )

        session.commit()


def add_model(model):
    session = get_session()  # Assuming you have a function to get a database session
    try:
        session.add(model)  # Add the provided model to the session
        session.commit()  # Commit changes on success
        session.refresh(model)  # Refresh the provided model

        # get_mem_store().add(
        #     collection_id=f"{model.__class__.__name__}_collection",
        #     document=json.dumps(model.dict(), default=str),
        #     metadatas={"model_id": model.id},
        # )
    except Exception as e:
        session.rollback()  # Rollback changes on failure
        raise e
    finally:
        session.close()


@contextmanager
def update_model(model_cls, model_id):
    session = get_session()  # Assuming you have a function to get a database session
    try:
        existing_model = session.query(model_cls).get(model_id)
        if existing_model is None:
            raise ValueError(f"{model_cls.__name__} with ID {model_id} not found")

        yield existing_model

        # doc_id = hashlib.sha256(str(model_id).encode()).hexdigest()[:20]
        # get_mem_store().update(
        #     collection_id=f"{model_cls.__name__}_collection",
        #     doc_ids=[doc_id],
        #     documents=[json.dumps(existing_model.dict(), default=str)],
        #     metadatas=[{"model_id": model_id}],
        # )

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
