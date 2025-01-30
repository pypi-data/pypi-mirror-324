import requests
from datetime import datetime, UTC

class MailerHelper:
    def send_email_daakiya(self, bucket_name, object_key, recipient_emails, subject, body):
        try:
            url = "https://daakiya-ktor.staging-internal.porter.in/mails/bundles/process"
            headers = {"Content-Type": "application/json"}

            payload = {
                "event_type": "publish_event",
                "bundle": {
                    "bundle_type": "direct_bundle",
                    "bundle_uuid": "3b57e664-5767-495f-bdf7-5dd28919079d",
                    "request_ts": int(datetime.now(UTC).timestamp() * 1000),
                    "mail_packet": {
                        "packet_type": "solo_packet",
                        "sender_mail_id": "noreply@theporter.in",
                        "receivers_mail_id_info": {
                            "to": recipient_emails,
                            "cc": [],
                            "bcc": []
                        },
                        "subject": subject,
                        "body": {
                            "body_type": "file_attachment_body",
                            "content": {
                                "content_type": "html",
                                "html_content": body
                            }
                        }
                    }
                }
            }

            if bucket_name and object_key:
                payload["bundle"]["mail_packet"]["body"]["attachments"] = [
                    {
                        "location": {
                            "storage_provider": "GCS",
                            "bucket": bucket_name,
                            "key": object_key
                        }
                    }
                ]

            response = requests.post(url, headers=headers, json=payload)

            if not response.ok:
                print(f"Error response from server: {response.text}")

            response.raise_for_status()
            print(f"Email sent successfully: {response.text}")

        except requests.exceptions.RequestException as req_error:
            print(f"Failed to send email via Daakiya: {req_error}")
            print(f"Response content: {req_error.response.text if hasattr(req_error, 'response') else 'No response content'}")
            raise RuntimeError(f"Error sending email: {req_error}")
