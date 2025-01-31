import requests
from datetime import datetime, timezone
import os

class MailerHelper:
    def __init__(self, env):
        self.env = env

    def send_email_daakiya(self, bucket_name, object_key, recipient_emails, subject, body):
        try:
            url = "https://daakiya-ktor.staging-internal.porter.in/mails/bundles/process"
            headers = {"Content-Type": "application/json"}

            payload = {
                "event_type": "publish_event",
                "bundle": {
                    "bundle_type": "direct_bundle",
                    "bundle_uuid": "3b57e664-5767-495f-bdf7-5dd28919079d",
                    "request_ts": int(datetime.now(timezone.utc).timestamp() * 1000),
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

    def send_failure_notification(self, bucket_name, object_key, recipient_emails, missing_mappings, posting_period_val, business_unit):
        subject = f"{business_unit} {self.env.capitalize()} Missing Mappings Notification - {posting_period_val}"

        body = f"""\
        <html>
          <body style="font-family: Roboto, sans-serif; color: #333;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="padding: 20px;">
                  <p>Dear Team,</p>

                  <p>We have identified that some records are missing in the system for the specified period ({posting_period_val}). Below is the list of missing mappings:</p>

                  <table width="100%" cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #f2f2f2;">
                      <th align="left">Field</th>
                      <th align="left">Missing Value</th>
                    </tr>"""

        for field, values in missing_mappings.items():
            for value in values:
                body += f"""\
                    <tr>
                      <td>{field}</td>
                      <td>{value}</td>
                    </tr>"""

        body += f"""\
                  </table>

                  <p>We kindly request you to update the missing fields in the records as soon as possible. 
                  Once the updates are completed, please inform us so that we can manually rerun the workflow to process the updated records for {posting_period_val}.</p>

                  <p>Should you require any assistance or have any questions, feel free to reach out to our team.</p>

                  <p>Thank you for your prompt attention to this matter.</p>

                  <p>Best regards,<br/>Revenue Assurance Team</p>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """

        try:
            self.send_email_daakiya(bucket_name, object_key, recipient_emails, subject, body)
            print("Failure notification sent successfully via Daakiya!")
        except Exception as e:
            print(f"Failed to send failure notification via Daakiya: {e}")
            raise RuntimeError(f"Error sending failure notification via Daakiya: {e}")