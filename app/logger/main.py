"""
Error Logger Module
"""

# build-in imports
import traceback
from datetime import datetime

# external imports
from fastapi import HTTPException

# module imports
from mails.sender import EmailSender
from config import settings


###########################################
##          Error Logger Class           ##
###########################################


class ErrorLogger:
    """
    Error logger implementation
    """

    def __init__(self, get_collection):
        self.sender = EmailSender()
        self.collection = get_collection("errors")

    async def register(self, _exception):
        """
        Create a complete report for exception.
        """
        # Transfor exception to string
        error_dict = self._format_db(_exception)
        # Notify the admin
        self._send_email_to_admin(error_dict)
        # Save on db
        await self.collection.insert_one(error_dict)
        # Notify the client the error
        raise HTTPException(status_code=500, detail="Server Error")

    def _format_db(self, _exception):
        """
        Add the error on db
        """
        date = datetime.now()
        filename = __name__
        error_to_str = self._exception_to_string(_exception)
        error = {
            "date": date,
            "filename": filename,
            "exception": error_to_str
        }
        return error

    def _send_email_to_admin(self, dict_error: dict) -> None:
        """
        Send a email to admin of the error.
        """
        message = self._generate_message(dict_error)
        to_list = [settings.EMAIL_ADMIN]

        email = self.sender.create_email(
            to_list=to_list,
            subject="UNU API ERROR",
            html_content=message)

        self.sender.send_email(email)

    def _exception_to_string(self, excp):
        """
        Transform a exception to string.
        """
        stack = traceback.extract_stack(
        )[:-3] + traceback.extract_tb(excp.__traceback__)
        pretty = traceback.format_list(stack)
        return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)

    def _generate_message(self, dict_error: dict) -> str:
        """
        Generates a message from error dict.
        """
        return f"""
        <h2>A error was occur in UNU-API.</h2>
        <ul>
          <li><h4>File: {dict_error["filename"]}</h4></li>
          <li><h4>Date: {dict_error["date"]}</h4></li>
          <li><h4>Error: {dict_error["exception"]}</h4></li>
        </ul>
        """
