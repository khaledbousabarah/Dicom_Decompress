import pydicom
import subprocess


def run(file):
    if _is_compressed(file):
        _decompress_dicom(dicom_file=file, output_file=file)


def _get_gdcmconv():
    """
    Get the full path to gdcmconv.
    If not found raise error
    """
    gdcmconv_executable = settings.gdcmconv_path
    if gdcmconv_executable is None:
        gdcmconv_executable = _which('gdcmconv')
    if gdcmconv_executable is None:
        gdcmconv_executable = _which('gdcmconv.exe')

    if gdcmconv_executable is None:
        raise ConversionError('GDCMCONV_NOT_FOUND')

    return gdcmconv_executable


def _is_compressed(dicom_file, force=False):
    """
    Check if dicoms are compressed or not
    """
    header = pydicom.read_file(dicom_file,
                               defer_size="1 KB",
                               stop_before_pixels=True,
                               force=force)

    uncompressed_types = ["1.2.840.10008.1.2",
                          "1.2.840.10008.1.2.1",
                          "1.2.840.10008.1.2.1.99",
                          "1.2.840.10008.1.2.2"]

    if 'TransferSyntaxUID' in header.file_meta and header.file_meta.TransferSyntaxUID in uncompressed_types:
        return False
    return True


def _decompress_dicom(dicom_file, output_file):
    """
    This function can be used to convert a jpeg compressed image to an uncompressed one for further conversion

    :param input_file: single dicom file to decompress
    """
    gdcmconv_executable = _get_gdcmconv()

    subprocess.check_output([gdcmconv_executable, '-w', dicom_file, output_file])


class ConversionError(Exception):
    """
    Custom error type to distinguish between know validations and script errors
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ConversionError, self).__init__(message)


def _which(program):
    import os

    def is_exe(executable_file):
        return os.path.isfile(executable_file) and os.access(executable_file, os.X_OK)

    file_path, file_name = os.path.split(program)
    if file_path:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

