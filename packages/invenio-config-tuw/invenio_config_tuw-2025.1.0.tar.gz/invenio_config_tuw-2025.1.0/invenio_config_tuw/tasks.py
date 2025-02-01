# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks running in the background."""

from typing import Optional

from celery import shared_task
from flask import current_app, render_template
from invenio_access.permissions import system_identity
from invenio_accounts.proxies import current_datastore
from invenio_mail.tasks import send_email
from invenio_rdm_records.proxies import current_rdm_records_service as records_service


@shared_task(ignore_result=True)
def send_publication_notification_email(recid: str, user_id: Optional[str] = None):
    """Send the record uploader an email about the publication of their record."""
    record = records_service.read(identity=system_identity, id_=recid)
    if user_id is not None:
        user = current_datastore.get_user(user_id)
    else:
        owner = record._obj.parent.access.owner
        if owner is not None and owner.owner_type == "user":
            user = owner.resolve()
        else:
            current_app.logger.warn(
                f"Couldn't find owner of record '{recid}' for sending email!"
            )
            return

    html_message = render_template(
        [
            "invenio_theme_tuw/mails/record_published.html",
            "mails/record_published.html",
        ],
        uploader=user,
        record=record,
        app=current_app,
    )
    message = render_template(
        [
            "invenio_theme_tuw/mails/record_published.txt",
            "mails/record_published.txt",
        ],
        uploader=user,
        record=record,
        app=current_app,
    )

    record_title = record["metadata"]["title"]
    send_email(
        {
            "subject": f'Your record "{record_title}" was published',
            "html": html_message,
            "body": message,
            "recipients": [user.email],
        }
    )
