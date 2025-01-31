"""Miscellaneous ImageJ related functions, mostly convenience wrappers."""

import sys
import time
import smtplib
import os

from ij import IJ  # pylint: disable-msg=import-error

from . import prefs
from ..log import LOG as log


def show_status(msg):
    """Wrapper to update the ImageJ status bar and the log simultaneously."""
    log.info(msg)
    IJ.showStatus(msg)


def show_progress(cur, final):
    """Wrapper to update the progress bar and issue a log message."""
    # ij.IJ.showProgress is adding 1 to the value given as first parameter...
    log.info("Progress: %s / %s (%s)", cur + 1, final, (1.0 + cur) / final)
    IJ.showProgress(cur, final)


def error_exit(msg):
    """Convenience wrapper to log an error and exit then."""
    log.error(msg)
    sys.exit(msg)


def elapsed_time_since(start, end=None):
    """Generate a string with the time elapsed between the two timepoints.

    Parameters
    ----------
    start : time.time
        Start time.
    end : time.time, optional
        End time. If skipped the current time will be used.

    Returns
    -------
    str
    """

    if not end:
        end = time.time()

    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def percentage(part, whole):
    """Calculate the percentage of a value based on total.

    Parameters
    ----------
    part : float
        Part.
    whole : float
        Complete size.

    Returns
    -------
    float
    """
    return 100 * float(part) / float(whole)


def calculate_mean_and_stdv(float_values):
    """Calculate mean and standard deviation from a list of floats.

    Parameters
    ----------
    float_values : list(float)
        List containing float numbers.

    Returns
    -------
    [float, float]
        Mean (1st item) and standard deviation (2nd item) of the list.
    """
    mean = sum(float_values) / len(float_values)
    tot = 0.0
    for x in float_values:
        tot = tot + (x - mean) ** 2
    return [mean, (tot / (len(float_values))) ** 0.5]


def find_focus(imp):
    """Find the slice of a stack that seems to bet the best focused one.

    NOTE: currently only single-channel stacks are supported.

    FIXME: explain what the function is actually doing, i.e. how does it decide
    what "the best focused one" is?

    Parameters
    ----------
    imp : ij.ImagePlus
        A single-channel ImagePlus.

    Returns
    -------
    int
    """

    imp_dimensions = imp.getDimensions()

    # Check if more than 1 channel
    # FUTURE Could be improved for multi channel
    if imp_dimensions[2] != 1:
        sys.exit("Image has more than one channel, please reduce dimensionality")

    # Loop through each time points
    for plane in range(1, imp_dimensions[4] + 1):
        focused_slice = 0
        norm_var = 0
        imp.setT(plane)
        # Loop through each z plane
        for current_z in range(1, imp_dimensions[3] + 1):
            imp.setZ(current_z)
            pix_array = imp.getProcessor().getPixels()
            mean = (sum(pix_array)) / len(pix_array)
            pix_array = [(x - mean) * (x - mean) for x in pix_array]
            # pix_array = pix_array*pix_array

            sumpix_array = sum(pix_array)
            var = sumpix_array / (imp_dimensions[0] * imp_dimensions[1] * mean)

            if var > norm_var:
                norm_var = var
                focused_slice = current_z

    return focused_slice


def send_mail(job_name, recipient, filename, total_execution_time):
    """Send an email using the SMTP server and sender email configured in ImageJ's Preferences.

    Parameters
    ----------
    job_name : string
        Job name to display in the email.
    recipient : string
        Recipient's email address.
    filename : string
        The name of the file to be passed in the email.
    total_execution_time : str
        The time it took to process the file in the format [HH:MM:SS:ss].
    """
    # Retrieve sender email and SMTP server from preferences
    sender = prefs.Prefs.get("imcf.sender_email", "").strip()
    server = prefs.Prefs.get("imcf.smtpserver", "").strip()

    # Ensure the sender and server are configured from Prefs
    if not sender:
        log.info("Sender email is not configured. Please check IJ_Prefs.txt.")
        return
    if not server:
        log.info("SMTP server is not configured. Please check IJ_Prefs.txt.")
        return

    # Ensure the recipient is provided
    if not recipient.strip():
        log.info("Recipient email is required.")
        return

    # Form the email subject and body
    subject = "Your {0} job finished successfully".format(job_name)
    body = (
        "Dear recipient,\n\n"
        "This is an automated message.\n"
        "Your dataset '{0}' has been successfully processed "
        "({1} [HH:MM:SS:ss]).\n\n"
        "Kind regards,\n"
        "The IMCF-team"
    ).format(filename, total_execution_time)

    # Form the complete message
    message = ("From: {0}\nTo: {1}\nSubject: {2}\n\n{3}").format(
        sender, recipient, subject, body
    )

    # Try sending the email, print error message if it wasn't possible
    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.sendmail(sender, recipient, message)
        log.debug("Successfully sent email")
    except smtplib.SMTPException as err:
        log.warning("Error: Unable to send email: %s", err)
    return


def progressbar(progress, total, line_number, prefix=""):
    """Progress bar for the IJ log window.

    Show a progress bar in the log window of Fiji at a specific line independent
    of the main Fiji progress bar.

    Parameters
    ----------
    progress : int
        Current step of the loop.
    total : int
        Total number of steps for the loop.
    line_number : int
        Number of the line to be updated.
    prefix : str, optional
        Text to use before the progress bar, by default ''.
    """

    size = 20
    x = int(size * progress / total)
    IJ.log(
        "\\Update%i:%s[%s%s] %i/%i\r"
        % (
            line_number,
            timed_log(prefix, True),
            "#" * x,
            "." * (size - x),
            progress,
            total,
        )
    )


def timed_log(message, as_string=False):
    """Print a message to the ImageJ log window with a timestamp added.

    Parameters
    ----------
    message : str
        Message to print
    """
    if as_string:
        return time.strftime("%H:%M:%S", time.localtime()) + ": " + message + " "
    IJ.log(time.strftime("%H:%M:%S", time.localtime()) + ": " + message + " ")


def get_free_memory():
    """Get the free memory thats available to ImageJ.

    Returns
    -------
    free_memory : int
        The free memory in bytes.
    """
    max_memory = int(IJ.maxMemory())
    used_memory = int(IJ.currentMemory())
    free_memory = max_memory - used_memory

    return free_memory


def setup_clean_ij_environment(rm=None, rt=None):  # pylint: disable-msg=unused-argument
    """Set up a clean and defined ImageJ environment.

    Clean active results table, roi manager and log, close any open image.

    "Fresh Start" is described in the ImageJ release notes [1] following a
    suggestion by Robert Haase in the Image.sc Forum [2].

    [1]: https://imagej.nih.gov/ij/notes.html
    [2]: https://forum.image.sc/t/fresh-start-macro-command-in-imagej-fiji/43102

    Parameters
    ----------
    rm : RoiManager, optional
        Will be ignored (kept for keeping API compatibility).
    rt : ResultsTable, optional
        Will be ignored (kept for keeping API compatibility).
    """

    IJ.run("Fresh Start", "")
    IJ.log("\\Clear")

    prefs.fix_ij_options()


def sanitize_image_title(imp):
    """Remove special chars and various suffixes from an open ImagePlus.

    Parameters
    ----------
    imp : ImagePlus
        The ImagePlus to be renamed.
    """
    # sometimes (unclear when) the title contains the full path, therefore we
    # simply call `os.path.basename()` on it to remove all up to the last "/":
    image_title = os.path.basename(imp.getTitle())
    image_title = image_title.replace(".czi", "")
    image_title = image_title.replace(" ", "_")
    image_title = image_title.replace("_-_", "")
    image_title = image_title.replace("__", "_")
    image_title = image_title.replace("#", "Series")

    imp.setTitle(image_title)
