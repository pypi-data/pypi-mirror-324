import requests
from datetime import datetime, timezone

class MailerHelper:
    def __init__(self, env, daakiya_url, bundle_uuid, sender_email_id, recipient_emails):
        self.env = env
        self.daakiya_url = daakiya_url 
        self.bundle_uuid = bundle_uuid  
        self.sender_email_id = sender_email_id
        self.recipient_emails = recipient_emails

    def send_email_daakiya(self, bucket_name, object_key, subject, body):
        try:
            url = self.daakiya_url
            headers = {"Content-Type": "application/json"}
            payload = {
                "event_type": "publish_event",
                "bundle": {
                    "bundle_type": "direct_bundle",
                    "bundle_uuid": self.bundle_uuid,
                    "request_ts": int(datetime.now(timezone.utc).timestamp() * 1000),
                    "mail_packet": {
                        "packet_type": "solo_packet",
                        "sender_mail_id": self.sender_email_id,
                        "receivers_mail_id_info": {
                            "to": self.recipient_emails,
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
            print(f"Failed to send email: {req_error}")
            print(f"Response content: {req_error.response.text if hasattr(req_error, 'response') else 'No response content'}")
            raise RuntimeError(f"Error sending email: {req_error}")